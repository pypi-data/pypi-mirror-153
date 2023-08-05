from nebula.graph import ttypes,GraphService
from nebula.ConnectionPool import ConnectionPool
from nebula.Client import GraphClient
from maintain_PlatoUtils.maintain_PlatoUtils import wrapNebula2Df
# from maintain_PlatoUtils import wrapNebula2Df
import tqdm
from typing import Callable, Any, Iterable
import traceback
from elasticsearch import Elasticsearch

class NodeInfo:
    def __init__(self,nodeType,nodeIdAttr,nodeIdVal="",nodeIdVal_fuzzy=""):
        self.nodeType=nodeType
        self.nodeIdAttr=nodeIdAttr
        self.nodeIdVal=nodeIdVal
        self.nodeIdVal_fuzzy=nodeIdVal_fuzzy
        self.nodeInfo=self.__dict__
        
        
class EdgeInfo:
    def __init__(self,edgeType,direct="",**edgeAttrKWargs):
        self.edgeType=edgeType
        self.edgeAttrDict=edgeAttrKWargs
        self.edgeInfo={
            "edgeType":edgeType,
            "direct":direct,
            **edgeAttrKWargs
        }
        
class RDFInfo:
    def __init__(self,head:NodeInfo,edge:EdgeInfo,tail:NodeInfo):
        self.head=head
        self.edge=edge
        self.tail=tail

class GraphWrapClient:
    
    def __init__(self,gClient,gDbName=""):
        '''初始化gClient'''
        self.gClient=gClient
        
        if len(gDbName)>0:
            self.gClient.execute_query("USE {}".format(gDbName))
            self.setGDbName(gDbName)
        
    def setGDbName(self,gDbName):
        '''设定图空间'''
        self.gClient.execute_query("USE {}".format(gDbName))
        self.gClient.set_space(gDbName)
        return self
        
    def execute_query(self,queryStr):
        '''query操作'''
        queryReq=self.gClient.execute_query(queryStr)
        reqDf=None
        if queryReq.error_code==0 and queryReq.rows is not None:
            reqDf=wrapNebula2Df(queryReq)
        return queryReq,reqDf
    
    def delVertex(self,sysIdList,delRel=True):
        '''（关联）删除节点'''
        errCode=0
        if delRel==True:
            showEdgeReq=self.gClient.execute_query("SHOW EDGES")
            errCode+=showEdgeReq.error_code
            
            relDf=wrapNebula2Df(showEdgeReq)
            if relDf.shape[0]>0:
                relList=relDf["Name"].values.flatten().tolist()
                for relItem in tqdm.tqdm(relList,desc="del edges with vertexes"):
                    for srcSysIdItem in tqdm.tqdm(sysIdList,desc="del srcs from edges with vertexes"):
                        relTailStr="GO FROM {srcSysId} OVER {edgeName} BIDIRECT YIELD {edgeName}._dst AS tgtSysId".format(
                            srcSysId=srcSysIdItem,
                            edgeName=relItem)
                        # print(relTailStr)
                        relTailReq=self.gClient.execute_query(relTailStr)
                        errCode+=relTailReq.error_code
                        relTailSysIdDf=wrapNebula2Df(relTailReq)
                        if relTailSysIdDf.shape[0]>0:
                            relTailSysIdList=relTailSysIdDf["tgtSysId"].values.flatten().tolist()
                            delOrderGroupStr=",".join(["{}->{}".format(srcSysIdItem,tailSysIdItem) for tailSysIdItem in relTailSysIdList])
                            delReverseGroupStr=",".join(["{}->{}".format(tailSysIdItem,srcSysIdItem) for tailSysIdItem in relTailSysIdList])
                            delGroupStr=",".join([delOrderGroupStr,delReverseGroupStr])
                            delStr="DELETE EDGE {} {}".format(relItem,delGroupStr)
                            # print(delStr)
                            delReq=self.gClient.execute_query(delStr)
                            errCode+=delReq.error_code
        return {"error_code":errCode}
        
        
class GraphWrapQuery:
    
    def __init__(self,esClient=None,esIndex=""):
        self.yieldAttrList=[]
        self.yieldSysIdList=[]
        self.esClient=esClient
        self.esIndex=esIndex
    
    def singleSearchFunc_wait(self,hetDict,head=True,singleYieldList={}):
        args=[hetDict]
        kwargs={
            "head":head,
            "singleYieldList":singleYieldList
        }
        return self.singleSearchFunc,args,kwargs
    
    def singleSearchFunc(self,hetDict,head=True,singleYieldList={}):
        '''
        direction: 默认单项
        '''
        
        singleQueryStrList=[]
        
        if type(hetDict)==dict:
            headInfo=hetDict.get("head",{})
            edgeInfo=hetDict.get("edge",{})
            tailInfo=hetDict.get("tail",{})
        elif type(hetDict)==RDFInfo:
            headInfo,edgeInfo,tailInfo=hetDict.head.nodeInfo,hetDict.edge.edgeInfo,hetDict.tail.nodeInfo
        elif type(hetDict)==NodeInfo:
            headInfo=hetDict.nodeInfo
            edgeInfo={}
            tailInfo={}
        
        headInfo["case_sensitive"]=headInfo.get("case_sensitive",False)
        
        if "direct" not in edgeInfo and len(edgeInfo)>0:
            edgeInfo["direct"]=""
        
        singleYieldDict={}
        if len(singleYieldList)>0:
            for yieldTypeAttrItem in singleYieldList:
                if "nodeType" in yieldTypeAttrItem:
                    if type(yieldTypeAttrItem["nodeAttr"])==str:
                        yieldTypeAttrItem["nodeAttr"]=yieldTypeAttrItem["nodeAttr"].strip()
                    nodeKey="node_{}".format(yieldTypeAttrItem["nodeType"])
                    singleYieldDict[nodeKey]=singleYieldDict.get(nodeKey,[])+[yieldTypeAttrItem["nodeAttr"]]
                elif "edgeType" in yieldTypeAttrItem:
                    if type(yieldTypeAttrItem["edgeAttr"])==str:
                        yieldTypeAttrItem["edgeAttr"]=yieldTypeAttrItem["edgeAttr"].strip()
                    edgeKey="edge_{}".format(yieldTypeAttrItem["edgeType"])
                    singleYieldDict[edgeKey]=singleYieldDict.get(edgeKey,[])+[yieldTypeAttrItem["edgeAttr"]]
                
            
        # LOOKUP语句构建
        if head==True:
            
            oriQueryName=headInfo.get("nodeIdVal_fuzzy","")
            queryName=headInfo["nodeIdVal_fuzzy"] if len(headInfo.get("nodeIdVal_fuzzy",""))>0 else headInfo["nodeIdVal"]
            if len(oriQueryName)==0:
                oriQueryName=queryName
            
            if len(headInfo.get("nodeIdVal_fuzzy",""))>0 and self.esClient!=None:
                qbody={
                        "query":{
                            "bool":{
                                "must":[
                                    {
                                        "bool":{
                                            "should":[
                                                {"match":{
                                                    "Name" if headInfo["case_sensitive"]==False else "Name.keyword": {
                                                        "query": oriQueryName,  
                                                        "fuzziness": "AUTO",
                                                        "prefix_length": 1,
                                                        "boost":10
                                                    }
                                                }},
                                                {"match": {
                                                    "AliasNames" if headInfo["case_sensitive"]==False else "AliasNames.keyword": {
                                                        "query": oriQueryName,
                                                        "fuzziness": "AUTO",
                                                        "prefix_length": 1,
                                                        "boost":1
                                                    }
                                                }}
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    }
                if len(headInfo.get("nodeType",""))>0:
                    nodeTypeESJudgeJson={
                        "bool":{
                            "must":{
                                "term":{
                                    "gTagName":headInfo["nodeType"]
                                }
                            }
                        }
                    }
                    qbody["query"]["bool"]["must"]=qbody["query"]["bool"]["must"]+[nodeTypeESJudgeJson]
                
                esResult=self.esClient.search(index=self.esIndex,body=qbody,timeout='60s')
                esResult=esResult["hits"]["hits"]
                if len(esResult)>0: # ES查询结果不为空
                    candidateList=[esResultItem["_source"]["Name"] for esResultItem in esResult[:50]]
                    rebuiltName=candidateList[0]
                    for candidateItem in candidateList:
                        if candidateItem==oriQueryName:
                            rebuiltName=oriQueryName
                            break
                elif len(oriQueryName)>0:
                    rebuiltName=oriQueryName
                else:
                    raise Exception("无法找到符合名称'{}'的'{}'类型节点".format(headInfo["nodeIdVal_fuzzy"],headInfo["nodeType"]))
                    
                headInfo["nodeIdVal"]=rebuiltName
                
                if len(esResult)>0:
                    for keyItem in esResult[0]["_source"]:
                        if esResult[0]["_source"][keyItem]==esResult[0]["_source"]["Name"] and keyItem!="Name":
                            headInfo["nodeType"]=esResult[0]["_source"]["gTagName"]
                            headInfo["nodeIdAttr"]=keyItem
                
            # 头节点其他属性查询
            otherAndWhereStrList=["{}.{}{}{}".format(headInfo["nodeType"],
                                            conditionItem[0],
                                            conditionItem[1],
                                            conditionItem[2]) for conditionItem in headInfo.get("where",{}).get("and",[])]
            otherAndWhereStr=" and ".join(otherAndWhereStrList)
            otherOrWhereStrList=["{}.{}{}{}".format(headInfo["nodeType"],
                                                    conditionItem[0],
                                                    conditionItem[1],
                                                    conditionItem[2]) for conditionItem in headInfo.get("where",{}).get("or",[])]
            otherOrWhereStr=" or ".join(otherOrWhereStrList)
            
            otherWhereStrList=[]
            if len(otherAndWhereStr)>0:
                otherWhereStrList.append("({})".format(otherAndWhereStr))
            if len(otherOrWhereStr)>0:
                otherWhereStrList.append("({})".format(otherOrWhereStr))
            
            otherWhereStr=" {} ".format(headInfo.get("where",{}).get("rootCondition","and")).join(otherWhereStrList)
            if len(otherWhereStr)>0:
                otherWhereStr=" and "+otherWhereStr
            
            if headInfo["nodeIdVal"]!="*":
                singleQueryStrList=["LOOKUP ON {nodeType} WHERE {nodeType}.{nodeIdAttr}=='{nodeIdVal}' {otherWhereStr}|\
                                            YIELD $-.VertexID AS src{nodeType}SysId".format(
                                                                                                nodeType=headInfo["nodeType"],
                                                                                                nodeIdAttr=headInfo["nodeIdAttr"],
                                                                                                nodeIdVal=headInfo["nodeIdVal"],
                                                                                                otherWhereStr=otherWhereStr
                                                                                            )]
                
            else:
                singleQueryStrList=["LOOKUP ON {nodeType} WHERE {nodeType}.{nodeIdAttr}!='不可能的名字' {otherWhereStr}|\
                                            YIELD $-.VertexID AS src{nodeType}SysId".format(
                                                                                                nodeType=headInfo["nodeType"],
                                                                                                nodeIdAttr=headInfo["nodeIdAttr"],
                                                                                                otherWhereStr=otherWhereStr
                                                                                            )]
                
            srcSysIdName="src{}SysId".format(headInfo["nodeType"])
            self.yieldSysIdList.append(srcSysIdName)
        
        # yield语句初始化
        yieldAttrList=[]
        pureAttrYieldList=[]
        for singleYieldTypeKey in singleYieldDict:
            nodeEdgeJudgeType=singleYieldTypeKey.split("_")[0]
            nodeEdgeRealType=singleYieldTypeKey.split("_")[1]
            if nodeEdgeJudgeType=="node":
                for singleYieldAttrVal in singleYieldDict[singleYieldTypeKey]:
                    
                    if len(headInfo)>0 and headInfo["nodeType"]==nodeEdgeRealType: # 头节点返回信息
                        
                        nodeType=nodeEdgeRealType
                        nodeAttr=singleYieldAttrVal
                        nodeTypeAttrName="{nodeType}{nodeAttr}".format(nodeType=nodeType,
                                                                    nodeAttr=nodeAttr)
                        
                        oriNodeTypeAttrName=nodeTypeAttrName
                        tmpNodeTypeAttrName=oriNodeTypeAttrName+"_0"
                        tailI=1
                        while tmpNodeTypeAttrName in self.yieldAttrList+pureAttrYieldList:
                            tmpNodeTypeAttrName=oriNodeTypeAttrName+"_"+str(tailI)
                            tailI+=1
                        nodeTypeAttrName=tmpNodeTypeAttrName
                        if head==True:
                            if len(tailInfo)>0:
                                yieldAttrList.append("$^.{nodeType}.{nodeAttr} AS {nodeTypeAttrName}".format(nodeType=nodeType,
                                                                                                                nodeAttr=nodeAttr,
                                                                                                            nodeTypeAttrName=nodeTypeAttrName))
                                if nodeTypeAttrName not in self.yieldAttrList+pureAttrYieldList:
                                    pureAttrYieldList.append(nodeTypeAttrName)
                            else:
                                yieldAttrList.append("{nodeType}.{nodeAttr} AS {nodeTypeAttrName}".format(nodeType=nodeType,
                                                                                                                nodeAttr=nodeAttr,
                                                                                                            nodeTypeAttrName=nodeTypeAttrName))
                                if nodeTypeAttrName not in self.yieldAttrList+pureAttrYieldList:
                                    pureAttrYieldList.append(nodeTypeAttrName)
                                
                    if len(edgeInfo)>0 and tailInfo["nodeType"]==nodeEdgeRealType: # 尾节点返回信息
                        nodeType=nodeEdgeRealType
                        nodeAttr=singleYieldAttrVal
                        nodeTypeAttrName="{nodeType}{nodeAttr}".format(nodeType=nodeType,
                                                                    nodeAttr=nodeAttr)
                        
                        oriNodeTypeAttrName=nodeTypeAttrName
                        tmpNodeTypeAttrName=oriNodeTypeAttrName+"_0"
                        tailI=1
                        while tmpNodeTypeAttrName in self.yieldAttrList+pureAttrYieldList:
                            tmpNodeTypeAttrName=oriNodeTypeAttrName+"_"+str(tailI)
                            tailI+=1
                        nodeTypeAttrName=tmpNodeTypeAttrName
                        
                        yieldAttrList.append("$$.{nodeType}.{nodeAttr} AS {nodeTypeAttrName}".format(nodeType=nodeType,
                                                                                                        nodeAttr=nodeAttr,
                                                                                                    nodeTypeAttrName=nodeTypeAttrName))
                        if nodeTypeAttrName not in self.yieldAttrList+pureAttrYieldList:
                            pureAttrYieldList.append(nodeTypeAttrName)
            elif nodeEdgeJudgeType=="edge":
                for singleYieldAttrVal in singleYieldDict[singleYieldTypeKey]:
                    edgeType=nodeEdgeRealType
                    edgeAttr=singleYieldAttrVal
                    edgeTypeAttrName="{edgeType}{edgeAttr}".format(edgeType=edgeType,
                                                                edgeAttr=edgeAttr)
                    
                    oriEdgeTypeAttrName=edgeTypeAttrName
                    tmpEdgeTypeAttrName=oriEdgeTypeAttrName+"_0"
                    tailI=1
                    while tmpEdgeTypeAttrName in self.yieldAttrList+pureAttrYieldList:
                        tmpEdgeTypeAttrName=oriEdgeTypeAttrName+"_"+str(tailI)
                        tailI+=1
                    edgeTypeAttrName=tmpEdgeTypeAttrName
                    
                    yieldAttrList.append("{edgeType}.{edgeAttr} AS {edgeTypeAttrName}".format(edgeType=edgeType,
                                                                                                    edgeAttr=edgeAttr,
                                                                                                edgeTypeAttrName=edgeTypeAttrName))
                    if edgeTypeAttrName not in self.yieldAttrList+pureAttrYieldList:
                        pureAttrYieldList.append(edgeTypeAttrName)
                        
        oldYieldAttrList=[]
        for yieldAttrItem in self.yieldAttrList:
            oldYieldAttrList.append("$-.{oldYieldAttr} AS {oldYieldAttr}".format(oldYieldAttr=yieldAttrItem))
        yieldAttrListStr=""
        if len(yieldAttrList)>0:
            yieldAttrListStr=","+",".join(oldYieldAttrList+yieldAttrList)

        yieldSysIdList=["$-.{yieldSysId} AS {yieldSysId}".format(yieldSysId=yieldSysIdItem) for yieldSysIdItem in self.yieldSysIdList]
        yieldSysIdListStr=""
        if len(yieldSysIdList)>0:
            yieldSysIdListStr=","+",".join(yieldSysIdList) 
        
        # GO语句构建-WHERE语句-tail
        tailOtherAndWhereStrList=["$$.{}.{}{}{}".format(tailInfo["nodeType"],
                                        conditionItem[0],
                                        conditionItem[1],
                                        conditionItem[2]) for conditionItem in tailInfo.get("where",{}).get("and",[])]
        tailOtherAndWhereStr=" and ".join(tailOtherAndWhereStrList)
        tailOtherOrWhereStrList=["$$.{}.{}{}{}".format(tailInfo["nodeType"],
                                                conditionItem[0],
                                                conditionItem[1],
                                                conditionItem[2]) for conditionItem in tailInfo.get("where",{}).get("or",[])]
        tailOtherOrWhereStr=" or ".join(tailOtherOrWhereStrList)
        
        tailOtherWhereStrList=[]
        if len(tailOtherAndWhereStr)>0:
            tailOtherWhereStrList.append("({})".format(tailOtherAndWhereStr))
        if len(tailOtherOrWhereStr)>0:
            tailOtherWhereStrList.append("({})".format(tailOtherOrWhereStr))
        
        tailOtherWhereStr=" {} ".format(tailInfo.get("where",{}).get("rootCondition","and")).join(tailOtherWhereStrList)
            
        # GO语句构建-WHERE语句-edge
        edgeOtherAndWhereStrList=["{}.{}{}{}".format(edgeInfo["edgeType"],
                                        conditionItem[0],
                                        conditionItem[1],
                                        conditionItem[2]) for conditionItem in edgeInfo.get("where",{}).get("and",[])]
        edgeOtherAndWhereStr=" and ".join(edgeOtherAndWhereStrList)
        edgeOtherOrWhereStrList=["{}.{}{}{}".format(edgeInfo["nodeType"],
                                                conditionItem[0],
                                                conditionItem[1],
                                                conditionItem[2]) for conditionItem in edgeInfo.get("where",{}).get("or",[])]
        edgeOtherOrWhereStr=" or ".join(edgeOtherOrWhereStrList)
        
        edgeOtherWhereStrList=[]
        if len(edgeOtherAndWhereStr)>0:
            edgeOtherWhereStrList.append("({})".format(edgeOtherAndWhereStr))
        if len(edgeOtherOrWhereStr)>0:
            edgeOtherWhereStrList.append("({})".format(edgeOtherOrWhereStr))
        
        edgeOtherWhereStr=" {} ".format(edgeInfo.get("where",{}).get("rootCondition","and")).join(edgeOtherWhereStrList)

        
        tailEdgeWhereStrList=[]
        if len(tailOtherWhereStr)>0:
            tailEdgeWhereStrList.append(tailOtherWhereStr)
        if len(edgeOtherWhereStr)>0:
            tailEdgeWhereStrList.append(edgeOtherWhereStr)
        tailEdgeWhereStr=" and ".join(tailEdgeWhereStrList)
        
        if len(tailEdgeWhereStr)>0:
            tailEdgeWhereStr=" where "+tailEdgeWhereStr
        
        # GO语句构建-完整化
        # RDF搜索
        if len(tailInfo)>0:
            tgtSysIdName="tgt{}SysId".format(tailInfo["nodeType"])
            oriTgtSysIdName=tgtSysIdName
            tmpTgtSysIdName=oriTgtSysIdName+"_0"
            tailI=1
            while tmpTgtSysIdName in self.yieldSysIdList:
                tmpTgtSysIdName=oriTgtSysIdName+"_"+str(tailI)
                tailI+=1
            tgtSysIdName=tmpTgtSysIdName
            
            if len(edgeInfo)>0:
                startSysId=self.yieldSysIdList[-1]
                singleQueryStrList.append("GO FROM $-.{startSysId} OVER {edgeType} {direct} {tailEdgeWhereStr} YIELD {edgeType}._dst AS {tgtSysIdName} {yieldList}{yieldAttrList}".format(
                                                        startSysId=startSysId,
                                                        edgeType=edgeInfo["edgeType"],
                                                        direct=edgeInfo["direct"],
                                                        tgtSysIdName=tgtSysIdName,
                                                        nodeType=tailInfo["nodeType"],
                                                        yieldList=yieldSysIdListStr,
                                                        yieldAttrList=yieldAttrListStr,
                                                        tailEdgeWhereStr=tailEdgeWhereStr
                                                    ))
            else:
                singleQueryStrList.append("GO FROM $-.VertexID OVER {edgeType} {direct} {tailEdgeWhereStr} YIELD {edgeType}._dst AS {tgtSysIdName} {yieldList}{yieldAttrList}".format(
                                                        edgeType=edgeInfo["edgeType"],
                                                        direct=edgeInfo["direct"],
                                                        tgtSysIdName=tgtSysIdName,
                                                        nodeType=tailInfo["nodeType"],
                                                        yieldList=yieldSysIdListStr,
                                                        yieldAttrList=yieldAttrListStr,
                                                        tailEdgeWhereStr=tailEdgeWhereStr
                                                    ))
        
            # 整理新的yield列表
            self.yieldSysIdList.append(tgtSysIdName)
            self.yieldAttrList+=pureAttrYieldList
            # self.yieldAttrList=list(set(self.yieldAttrList))
        else:
            # 单节点搜索
            fetchStr="FETCH PROP ON {nodeType} $-.{srcSysID} YIELD {yieldAttrList}".format(nodeType=headInfo["nodeType"],
                                                                                            srcSysID=srcSysIdName,
                                                                                            yieldAttrList=yieldAttrListStr[1:])
            # 整理新的yield列表
            self.yieldAttrList+=pureAttrYieldList
            singleQueryStrList.append(fetchStr)
            
        
        totalQuery="|".join(singleQueryStrList)
        
        return totalQuery
            
    def intersectSearchFunc_wait(self,*queryList):
        return self.intersectSearchFunc,queryList
        
    def intersectSearchFunc(self,*queryFuncList):
        tmpQueryStrList=[]
        for queryFuncGroupItem in queryFuncList:
            self.yieldSysIdList=[]
            self.yieldAttrList=[]
            if type(queryFuncGroupItem)==str:
                # 返回query
                queryItem=queryFuncGroupItem
            else:
                # 返回函数
                if len(queryFuncGroupItem)==3:
                    queryFunc,args,kwargs=queryFuncGroupItem
                    queryItem=queryFunc(*args,**kwargs)
                else:
                    queryFunc,args=queryFuncGroupItem
                    queryItem=queryFunc(*args)
            tmpQueryStrList.append("({})".format(queryItem))
        queryStr=" INTERSECT ".join(tmpQueryStrList)
        return queryStr
              
    def unionSearchFunc_wait(self,*queryList):
        return self.unionSearchFunc,queryList
        
    def unionSearchFunc(self,*queryFuncList):
        tmpQueryStrList=[]
        for queryFuncGroupItem in queryFuncList:
            self.yieldSysIdList=[]
            self.yieldAttrList=[]
            if type(queryFuncGroupItem)==str:
                queryItem=queryFuncGroupItem
            else:
                if len(queryFuncGroupItem)==3:
                    queryFunc,args,kwargs=queryFuncGroupItem
                    queryItem=queryFunc(*args,**kwargs)
                else:
                    queryFunc,args=queryFuncGroupItem
                    queryItem=queryFunc(*args)
            tmpQueryStrList.append("({})".format(queryItem))
        queryStr=" UNION ".join(tmpQueryStrList)
        return queryStr
        
    def seqSearchFunc_wait(self,*queryList):
        for queryItem in queryList[1:]:
            queryItem[2]["head"]=False
        return self.seqSearchFunc,queryList
        
    def seqSearchFunc(self,*queryGroupList):
        '''第一个singleFunc的head为True'''
        tmpQueryStrList=[]
        for queryGroupItem in queryGroupList:
            
            if type(queryGroupItem)==str:
                queryItem=queryGroupItem
            else:
                if len(queryGroupItem)==3:
                    queryFuncItem,args,kwargs=queryGroupItem
                    queryItem=queryFuncItem(*args,**kwargs)
                else:
                    queryFuncItem,args=queryGroupItem
                    queryItem=queryFuncItem(*args)
                
            tmpQueryStrList.append(queryItem)
        queryStr="|".join(tmpQueryStrList)
        return queryStr
        
    def renew(self):
        self.yieldAttrList=[]
        self.yieldSysIdList=[]
        
    def runWaitFunc(self,waitFuncGroupList,maxLayer=0,orderList=[]):
        if type(waitFuncGroupList)==list or type(waitFuncGroupList)==dict:
            return waitFuncGroupList
        typeList=[type(waitFuncGroupItem).__name__ for waitFuncGroupItem in waitFuncGroupList]
        typeSetList=list(set(typeList))
            
        if "str" not in typeList:
            if type(waitFuncGroupList[0]).__name__=="method":
                if waitFuncGroupList[0].__name__=="singleSearchFunc":
                    print("singleSearchFunc")
                    if maxLayer==0:
                        returnVal=waitFuncGroupList[0](*waitFuncGroupList[1],**waitFuncGroupList[2])
                    else:
                        return waitFuncGroupList
                elif waitFuncGroupList[0].__name__=="seqSearchFunc":
                    print("seqSearchFunc")
                    returnVal=waitFuncGroupList[0](*self.runWaitFunc(waitFuncGroupList[1],maxLayer=maxLayer+1))
                elif waitFuncGroupList[0].__name__=="unionSearchFunc":
                    print("unionSearchFunc")
                    returnVal=waitFuncGroupList[0](*self.runWaitFunc(waitFuncGroupList[1],maxLayer=maxLayer+1))
                elif waitFuncGroupList[0].__name__=="intersectSearchFunc":
                    print("intersectSearchFunc")
                    returnVal=waitFuncGroupList[0](*self.runWaitFunc(waitFuncGroupList[1],maxLayer=maxLayer+1))
                
                
                # if type(waitFuncGroupList[1])==tuple:
                #     try:
                #         return waitFuncGroupList[0](*self.runWaitFunc(waitFuncGroupList[1]))
                #     except Exception as ex:
                #         traceback.print_exc()
                #         print(ex)
                # else:
                #     try:
                #         return waitFuncGroupList[0](*self.runWaitFunc(waitFuncGroupList[1]),**self.runWaitFunc(waitFuncGroupList[2]))
                #     except Exception as ex:
                #         traceback.print_exc()
                #         print(ex)
            # elif len(typeSetList)==1 and typeSetList[0]=="tuple":
            #     returnVal=[self.runWaitFunc(waitFuncGroupItem) for waitFuncGroupItem in waitFuncGroupList]
            #     return returnVal
            else:
                return waitFuncGroupList
        
        orderAttrList=["".join(orderAttrPairItem[0].split(".")) for orderAttrPairItem in orderList]
        midRealAttrDict=dict(("".join(orderAttrPairItem[0].split(".")),orderAttrPairItem[0]) for orderAttrPairItem in orderList)
        attrOrderDict=dict(orderList)
        realFakeOrderDict=dict((yieldItem,yieldItem.split("_")[0]) for yieldItem in self.yieldAttrList if yieldItem.split("_")[0] in orderAttrList)
        returnOrderListStr=",".join([" ".join((keyItem,attrOrderDict[midRealAttrDict[realFakeOrderDict[keyItem]]])) 
                                        for keyItem in sorted(list(realFakeOrderDict.keys()),key=lambda realKeyItem:orderAttrList.index(realFakeOrderDict[realKeyItem]))])
        if len(returnOrderListStr)>0:
            returnVal+="|ORDER BY {}".format(returnOrderListStr)
        
        return returnVal
            
    def transMethod(self,methodName):
        if methodName=="singleSearch":
            return self.singleSearchFunc_wait
        elif methodName=="seqSearch":
            return self.seqSearchFunc_wait
        elif methodName=="unionSearch":
            return self.unionSearchFunc_wait
        elif methodName=="intersectSearch":
            return self.intersectSearchFunc_wait
            
    def wrapJson2Query(self,myQueryJson):
        if myQueryJson["searchMethod"] in ["seqSearch","unionSearch","intersectSearch"]:
            searchMethod=self.transMethod(myQueryJson["searchMethod"])
            searchFrameList=myQueryJson["searchFrame"]
            return searchMethod(*[self.wrapJson2Query(searchFrameItem) for searchFrameItem in searchFrameList])
        if myQueryJson["searchMethod"] in ["singleSearch"]:
            searchMethod=self.transMethod(myQueryJson["searchMethod"])
            searchFrameDict=myQueryJson["searchFrame"]
            searchFrameDict["singleYieldList"]=searchFrameDict.get("singleYieldList",{})
            return searchMethod(searchFrameDict,singleYieldList=searchFrameDict["singleYieldList"])
            
        
if __name__=="__main__":
    
    gHost="9.135.95.249"
    gPort=13708
    gUser="root"
    gPassword="nebula"
    gDbName="company_product_field_musklin"

    Connection_pool = ConnectionPool(gHost, gPort,network_timeout=300000)
    gClient = GraphClient(Connection_pool)
    gClient.authenticate(gUser, gPassword)
    myGClient=GraphWrapClient(gClient,gDbName=gDbName)
    esClient= Elasticsearch(["9.134.92.196:9200"],http_auth=("elastic", "devcloud@123"))
    myGQuery=GraphWrapQuery(esClient=esClient,esIndex="hr_integrate_kg")
    
    # # single vertex search with singleSearch
    # queryStr=myGQuery.singleSearchFunc(NodeInfo("Company","CompanyName",nodeIdVal="深圳市腾讯计算机系统有限公司"),
    #                                singleYieldList=[{"nodeType":"Company","nodeAttr":"CompanyName"}])
    # myGQuery.renew()
    # print(queryStr)
    
    # # singleSearch
    # queryStr=myGQuery.singleSearchFunc(RDFInfo(NodeInfo("Company","CompanyName",nodeIdVal="深圳市腾讯计算机系统有限公司"),
    #                                        EdgeInfo("produce"),
    #                                        NodeInfo("Product","ProductName",nodeIdVal=None)),
    #                                singleYieldList=[{"nodeType":"Company","nodeAttr":"CompanyName"},
    #                                                 {"nodeType":"Product","nodeAttr":"ProductName"}])
    # myGQuery.renew()
    # print(queryStr)
    
    # # seqSearch
    # queryStr=myGQuery.seqSearchFunc(
    #     myGQuery.singleSearchFunc_wait(RDFInfo(NodeInfo("Company","CompanyName",nodeIdVal="深圳市腾讯计算机系统有限公司"),
    #                                        EdgeInfo("produce"),
    #                                        NodeInfo("Product","ProductName",nodeIdVal=None)),
    #                                singleYieldList=[{"nodeType":"Company","nodeAttr":"CompanyName"},
    #                                                 {"nodeType":"Product","nodeAttr":"ProductName"}]),
    #     myGQuery.singleSearchFunc_wait(RDFInfo(NodeInfo("Product","ProductName",nodeIdVal=None),
    #                                        EdgeInfo("belongTo"),
    #                                        NodeInfo("Field","FieldName",nodeIdVal=None)),
    #                                singleYieldList=[{"nodeType":"Product","nodeAttr":"ProductName"},
    #                                                 {"nodeType":"Field","nodeAttr":"FieldName"}],
    #                                head=False)
    # )
    # myGQuery.renew()
    # print(queryStr)
    
    # # unionSearch
    # queryStr=myGQuery.unionSearchFunc(
    #     myGQuery.singleSearchFunc_wait(RDFInfo(NodeInfo("Company","CompanyName",nodeIdVal="深圳市腾讯计算机系统有限公司"),
    #                                         EdgeInfo("produce"),
    #                                         NodeInfo("Product","ProductName",nodeIdVal=None)),
    #                                 singleYieldList=[{"nodeType":"Company","nodeAttr":"CompanyName"},
    #                                                 {"nodeType":"Product","nodeAttr":"ProductName"}]),
    #     myGQuery.singleSearchFunc_wait(RDFInfo(NodeInfo("Company","CompanyName",nodeIdVal="国泰君安期货有限公司"),
    #                                         EdgeInfo("produce"),
    #                                         NodeInfo("Product","ProductName",nodeIdVal=None)),
    #                                 singleYieldList=[{"nodeType":"Company","nodeAttr":"CompanyName"},
    #                                                 {"nodeType":"Product","nodeAttr":"ProductName"}])
    # )
    # myGQuery.renew()
    # print(queryStr)
    
    # # union+seqSearch
    # queryFunc=myGQuery.unionSearchFunc_wait(
    #     myGQuery.seqSearchFunc_wait(
    #         myGQuery.singleSearchFunc_wait(RDFInfo(NodeInfo("Company","CompanyName",nodeIdVal="深圳市腾讯计算机系统有限公司"),
    #                                         EdgeInfo("produce"),
    #                                         NodeInfo("Product","ProductName",nodeIdVal=None)),
    #                                 singleYieldList=[{"nodeType":"Company","nodeAttr":"CompanyName"},
    #                                                     {"nodeType":"Product","nodeAttr":"ProductName"}]),
    #         myGQuery.singleSearchFunc_wait(RDFInfo(NodeInfo("Product","ProductName",nodeIdVal=None),
    #                                         EdgeInfo("belongTo"),
    #                                         NodeInfo("Field","FieldName",nodeIdVal=None)),
    #                                 singleYieldList=[{"nodeType":"Product","nodeAttr":"ProductName"},
    #                                                     {"nodeType":"Field","nodeAttr":"FieldName"}],
    #                                 head=False)
    #     ),
    #     myGQuery.seqSearchFunc_wait(
    #         myGQuery.singleSearchFunc_wait(RDFInfo(NodeInfo("Company","CompanyName",nodeIdVal="阿里巴巴"),
    #                                         EdgeInfo("produce"),
    #                                         NodeInfo("Product","ProductName",nodeIdVal=None)),
    #                                 singleYieldList=[{"nodeType":"Company","nodeAttr":"CompanyName"},
    #                                                     {"nodeType":"Product","nodeAttr":"ProductName"}]),
    #         myGQuery.singleSearchFunc_wait(RDFInfo(NodeInfo("Product","ProductName",nodeIdVal=None),
    #                                         EdgeInfo("belongTo"),
    #                                         NodeInfo("Field","FieldName",nodeIdVal=None)),
    #                                 singleYieldList=[{"nodeType":"Product","nodeAttr":"ProductName"},
    #                                                     {"nodeType":"Field","nodeAttr":"FieldName"}],
    #                                 head=False)
    #     )
    # )
    # myGQuery.renew()
    # print(queryStr)
    
    # # intersect+seqSearch
    # queryFunc=myGQuery.intersectSearchFunc_wait(
    #     myGQuery.seqSearchFunc_wait(
    #         myGQuery.singleSearchFunc_wait(RDFInfo(NodeInfo("Company","CompanyName",nodeIdVal="深圳市腾讯计算机系统有限公司"),
    #                                         EdgeInfo("produce"),
    #                                         NodeInfo("Product","ProductName",nodeIdVal=None)),
    #                                 singleYieldList=[{"nodeType":"Company","nodeAttr":"CompanyName"},
    #                                                     {"nodeType":"Product","nodeAttr":"ProductName"}]),
    #         myGQuery.singleSearchFunc_wait(RDFInfo(NodeInfo("Product","ProductName",nodeIdVal=None),
    #                                         EdgeInfo("belongTo"),
    #                                         NodeInfo("Field","FieldName",nodeIdVal=None)),
    #                                 singleYieldList=[{"nodeType":"Product","nodeAttr":"ProductName"},
    #                                                     {"nodeType":"Field","nodeAttr":"FieldName"}],
    #                                 head=False)
    #     ),
    #     myGQuery.seqSearchFunc_wait(
    #         myGQuery.singleSearchFunc_wait(RDFInfo(NodeInfo("Company","CompanyName",nodeIdVal="阿里巴巴"),
    #                                         EdgeInfo("produce"),
    #                                         NodeInfo("Product","ProductName",nodeIdVal=None)),
    #                                 singleYieldList=[{"nodeType":"Company","nodeAttr":"CompanyName"},
    #                                                     {"nodeType":"Product","nodeAttr":"ProductName"}]),
    #         myGQuery.singleSearchFunc_wait(RDFInfo(NodeInfo("Product","ProductName",nodeIdVal=None),
    #                                         EdgeInfo("belongTo"),
    #                                         NodeInfo("Field","FieldName",nodeIdVal=None)),
    #                                 singleYieldList=[{"nodeType":"Product","nodeAttr":"ProductName"},
    #                                                     {"nodeType":"Field","nodeAttr":"FieldName"}],
    #                                 head=False)
    #     )
    # )
    # myGQuery.renew()
    # print(queryStr)
    
    # # wrapJson2Qeury-1
    # queryJson={
    #         "searchMethod":"seqSearch",
    #         "searchFrame":[
    #             {
    #                 "searchMethod":"singleSearch",
    #                 "searchFrame":{
    #                     "head":{
    #                         "nodeType":"Company",
    #                         "nodeIdAttr":"CompanyName",
    #                         "nodeIdVal":"深圳市腾讯计算机系统有限公司"
    #                     },
    #                     "edge":{
    #                         "edgeType":"produce"
    #                     },
    #                     "tail":{
    #                         "nodeType":"Product",
    #                         "nodeIdAttr":"ProductName",
    #                         "nodeIdVal":None
    #                     },
    #                     "singleYieldList":[
    #                         {"nodeType":"Company","nodeAttr":"CompanyName"},
    #                         {"nodeType":"Product","nodeAttr":"ProductName"}
    #                     ]
    #                 }
    #             },{
    #                 "searchMethod":"singleSearch",
    #                 "searchFrame":{
    #                     "head":{
    #                         "nodeType":"Product",
    #                         "nodeIdAttr":"ProductName",
    #                         "nodeIdVal":None
    #                     },
    #                     "edge":{
    #                         "edgeType":"belongTo"
    #                     },
    #                     "tail":{
    #                         "nodeType":"Field",
    #                         "nodeIdAttr":"FieldName",
    #                         "nodeIdVal":None
    #                     },
    #                     "singleYieldList":[
    #                         {"nodeType":"Company","nodeAttr":"CompanyName"},
    #                         {"nodeType":"Product","nodeAttr":"ProductName"},
    #                         {"nodeType":"Field","nodeAttr":"FieldName"}
    #                     ]
    #                 }
    #             }
    #         ]
    #     }
    # queryFunc=myGQuery.wrapJson2Query(queryJson)
    # queryStr=myGQuery.runWaitFunc(queryFunc)
    # myGQuery.renew()
    # print(queryStr)
    
    # # wrapJson2Qeury-2
    # queryJson={
    #     "searchMethod":"singleSearch",
    #     "searchFrame":{
    #         "head":{
    #             "nodeType":"Company",
    #             "nodeIdAttr":"CompanyName",
    #             "nodeIdVal":"深圳市腾讯计算机系统有限公司"
    #         },
    #         "edge":{
    #             "edgeType":"produce"
    #         },
    #         "tail":{
    #             "nodeType":"Product",
    #             "nodeIdAttr":"ProductName",
    #             "nodeIdVal":None
    #         },
    #         "singleYieldList":[
    #             {"nodeType":"Company","nodeAttr":"CompanyName"},
    #             {"nodeType":"Product","nodeAttr":"ProductName"}
    #         ]
    #     }
    # }
    # queryFunc=myGQuery.wrapJson2Query(queryJson)
    # queryStr=myGQuery.runWaitFunc(queryFunc)
    # myGQuery.renew()
    # print(queryStr)
    
    # # wrapJson2Query-seq
    # queryJson={
    #     "searchMethod":"seqSearch",
    #     "searchFrame":[
    #         {
    #             "searchMethod":"singleSearch",
    #             "searchFrame":{
    #                 "head":{
    #                     "nodeType":"YunPost",
    #                     "nodeIdAttr":"YunPostName",
    #                     "nodeIdVal":"*"
    #                 },
    #                 "edge":{
    #                     "edgeType":"subPost"
    #                 },
    #                 "tail":{
    #                     "nodeType":"YunPost",
    #                     "nodeIdAttr":"YunPostName",
    #                     "nodeIdVal":None
    #                 },
    #                 "singleYieldList":[
    #                     {"nodeType":"YunPost","nodeAttr":"YunPostName"}
    #                 ]
    #             }
    #         },{
    #             "searchMethod":"singleSearch",
    #             "searchFrame":{
    #                 "head":{
    #                     "nodeType":"YunPost",
    #                     "nodeIdAttr":"YunPostName",
    #                     "nodeIdVal":None
    #                 },
    #                 "edge":{
    #                     "edgeType":"subPost"
    #                 },
    #                 "tail":{
    #                     "nodeType":"YunPost",
    #                     "nodeIdAttr":"YunPostName",
    #                     "nodeIdVal":None
    #                 },
    #                 "singleYieldList":[
    #                     {"nodeType":"YunPost","nodeAttr":"YunPostName"}
    #                 ]
    #             }
    #         }
    #     ]
    # }
    # queryFunc=myGQuery.wrapJson2Query(queryJson)
    # queryStr=myGQuery.runWaitFunc(queryFunc)
    # myGQuery.renew()
    # print(queryStr)
    
    # # singlesearch
    # queryJson={
    #     "searchMethod":"singleSearch",
    #     "searchFrame":{
    #         "head":{
    #             "nodeType":"Company",
    #             "nodeIdAttr":"CompanyName",
    #             "nodeIdVal":"阿里巴巴"
    #         },
    #         "singleYieldList":[
    #             {"nodeType":"Company","nodeAttr":"CompanyName"},
    #             {"nodeType":"Company","nodeAttr":"AliasNames"}
    #         ]
    #     }
    # }
    # queryFunc=myGQuery.wrapJson2Query(queryJson)
    # queryStr=myGQuery.runWaitFunc(queryFunc)
    # myGQuery.renew()
    # print(queryStr)
    
    # # fuzzy search
    # queryJson={
    #             "searchMethod":"singleSearch",
    #             "searchFrame":{
    #                 "head":{
    #                     "nodeType":"YunPost",
    #                     "nodeIdAttr":"YunPostName",
    #                     "nodeIdVal":"深度学习"
    #                 },
    #                 "edge":{
    #                     "edgeType":"produce"
    #                 },
    #                 "tail":{
    #                     "nodeType":"Skill",
    #                     "nodeIdAttr":"SkillName",
    #                     "nodeIdVal":None
    #                 },
    #                 "singleYieldList":[
    #                     {"nodeType":"YunPost","nodeAttr":"YunPostName"},
    #                     {"nodeType":"Skill","nodeAttr":"SkillName"}
    #                 ]
    #             }
    #         }
    # queryFunc=myGQuery.wrapJson2Query(queryJson)
    # queryStr=myGQuery.runWaitFunc(queryFunc)
    # myGQuery.renew()
    # print(queryStr)
    
    # # singlesearch
    # queryJson={
    #     "searchMethod":"singleSearch",
    #     "searchFrame":{
    #         "head":{
    #             "nodeType":"Company",
    #             "nodeIdAttr":"CompanyName",
    #             "nodeIdVal":"*"
    #         },
    #         "singleYieldList":[
    #             {"nodeType":"Company","nodeAttr":"CompanyName"},
    #             {"nodeType":"Company","nodeAttr":"AliasNames"}
    #         ]
    #     }
    # }
    # queryFunc=myGQuery.wrapJson2Query(queryJson)
    # queryStr=myGQuery.runWaitFunc(queryFunc)
    # myGQuery.renew()
    # print(queryStr)
    
    # queryJson={
    #         "searchMethod":"singleSearch",
    #         "searchFrame":{
    #             "head":{
    #                 "nodeType":"YunPost",
    #                 "nodeIdAttr":"YunPostName",
    #                 "nodeIdVal":"golang"
    #             },
    #             "edge":{
    #                 "edgeType":"contain"
    #             },
    #             "tail":{
    #                 "nodeType":"Skill",
    #                 "nodeIdAttr":"SkillName",
    #                 "nodeIdVal":None
    #             },
    #             "singleYieldList":[
    #                 {"nodeType":"YunPost","nodeAttr":"YunPostName"},
    #                 {"nodeType":"Skill","nodeAttr":"SkillName"},
    #                 {"edgeType":"contain","edgeAttr":"score"}
    #             ]
    #         }
    #     }
    # queryFunc=myGQuery.wrapJson2Query(queryJson)
    # queryStr=myGQuery.runWaitFunc(queryFunc)
    # myGQuery.renew()
    # print(queryStr)
    
    # # 职位技能关系查询-排序
    # queryJson={
    #         "searchMethod":"singleSearch",
    #         "searchFrame":{
    #             "head":{
    #                 "nodeType":"Post",
    #                 "nodeIdAttr":"PostName",
    #                 "nodeIdVal":"应用开发"
    #             },
    #             "edge":{
    #                 "edgeType":"contain"
    #             },
    #             "tail":{
    #                 "nodeType":"Skill",
    #                 "nodeIdAttr":"SkillName",
    #                 "nodeIdVal":None
    #             },
    #             "singleYieldList":[
    #                 {"nodeType":"Post","nodeAttr":"PostName"},
    #                 {"nodeType":"Skill","nodeAttr":"SkillName"},
    #                 {"edgeType":"contain","edgeAttr":"score"}
    #             ]
    #         }
    #     }
    # queryFunc=myGQuery.wrapJson2Query(queryJson)
    # queryStr=myGQuery.runWaitFunc(queryFunc,orderList=[["contain.score","desc"]])
    # myGQuery.renew()
    # print(queryStr)
    
    #  # 职位技能关系查询-排序
    # queryJson={
    #         "searchMethod":"singleSearch",
    #         "searchFrame":{
    #             "head":{
    #                 "nodeType":"Skill",
    #                 "nodeIdAttr":"SkillName",
    #                 "nodeIdVal":"*"
    #             },
    #             "singleYieldList":[
    #                 {"nodeType":"Skill","nodeAttr":"SkillName"},
    #                 {"nodeType":"Skill","nodeAttr":"count"}
    #             ]
    #         }
    #     }
    # queryFunc=myGQuery.wrapJson2Query(queryJson)
    # queryStr=myGQuery.runWaitFunc(queryFunc,orderList=[["Skill.count","desc"]])
    # myGQuery.renew()
    # print(queryStr)
    
    #  # 忽略大小写
    # queryJson={
    #     "searchMethod":"unionSearch",
    #     "searchFrame":[
    #         {
    #             "searchMethod":"seqSearch",
    #             "searchFrame":[
    #                 {
    #                     "searchMethod":"singleSearch",
    #                     "searchFrame":{
    #                         "head":{
    #                             "nodeType":"Company",
    #                             "nodeIdAttr":"CompanyName",
    #                             "nodeIdVal":"阿里巴巴",
    #                             "case_sensitive":False
    #                         },
    #                         "edge":{
    #                             "edgeType":"produce"
    #                         },
    #                         "tail":{
    #                             "nodeType":"Product",
    #                             "nodeIdAttr":"ProductName",
    #                             "nodeIdVal":False
    #                         },
    #                         "singleYieldList":[
    #                             {
    #                                 "nodeType":"Company",
    #                                 "nodeAttr":"AliasNames"
    #                             },
    #                             {
    #                                 "nodeType":"Company",
    #                                 "nodeAttr":"CompanyName"
    #                             },
    #                             {
    #                                 "nodeType":"Product",
    #                                 "nodeAttr":"ProductName"
    #                             }
    #                         ]
    #                     }
    #                 },
    #                 {
    #                     "searchMethod":"singleSearch",
    #                     "searchFrame":{
    #                         "head":{
    #                             "nodeType":"Product",
    #                             "nodeIdAttr":"ProductName",
    #                             "nodeIdVal":None
    #                         },
    #                         "edge":{
    #                             "edgeType":"belongTo"
    #                         },
    #                         "tail":{
    #                             "nodeType":"Field",
    #                             "nodeIdAttr":"FieldName",
    #                             "nodeIdVal":None
    #                         },
    #                         "singleYieldList":[
    #                             {
    #                                 "nodeType":"Product",
    #                                 "nodeAttr":"ProductName"
    #                             },
    #                             {
    #                                 "nodeType":"Field",
    #                                 "nodeAttr":"FieldName"
    #                             }
    #                         ]
    #                     }
    #                 }
    #             ]
    #         }
    #     ]
    # }
    # queryFunc=myGQuery.wrapJson2Query(queryJson)
    # queryStr=myGQuery.runWaitFunc(queryFunc,orderList=[["Skill.count","desc"]])
    # myGQuery.renew()
    # print(queryStr)
    
    
     # 模糊查询
    queryJson={
            "searchMethod":"singleSearch",
            "searchFrame":{
                "head":{
                    "nodeType":"Company",
                    "nodeIdAttr":"CompanyName",
                    "nodeIdVal_fuzzy":"深圳腾讯计算机系统有限公司"
                },
                "singleYieldList":[
                    {"nodeType":"Company","nodeAttr":"CompanyName"}
                ]
            }
        }
    queryFunc=myGQuery.wrapJson2Query(queryJson)
    queryStr=myGQuery.runWaitFunc(queryFunc,orderList=[["Skill.count","desc"]])
    myGQuery.renew()
    
    
    
    
    print(queryStr)
    print(123)
    # queryReq,queryDf=myGClient.execute_query("INSERT VERTEX hv1NodeType(headIdAttr) VALUES uuid('hv1NodeType_7'):(7)")
    # myGClient.singleFunc(hetDict=)x