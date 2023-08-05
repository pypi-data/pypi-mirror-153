import time
from re import search
import pandas as pd

from . import preprocessor
from maintain_PlatoUtils.maintain_PlatoUtils import wrapNebula2Df
from nebula.graph import ttypes,GraphService
from nebula.ConnectionPool import ConnectionPool
from nebula.Client import GraphClient
import tqdm
import numpy as np
import traceback
from multiprocessing import Process,Queue
import threading
from elasticsearch import Elasticsearch

def passDf2Queue(gClient,queryStr,myQueue):
    myDf=wrapNebula2Df(gClient.execute_query(queryStr))
    myQueue.put(myDf)
    
def rankScore(searchText,companyName):
    sumDelta=0
    for searchCharI in range(1,len(searchText)):
        if searchText[searchCharI] in companyName and searchText[searchCharI-1] in companyName:
            delta=int(companyName.index(searchText[searchCharI])>companyName.index(searchText[searchCharI-1]))
            sumDelta+=delta
    return sumDelta

def esSearch(esClient,searchWord,searchType="*",searchIdAttr="*",withCount=False,withWeight=False,topN=300,tfidfModel=None):
    cuttedWord=" ".join(preprocessor.simpleCutWords(searchWord))
    stopMinLimit=4
    hitList=[]
    while len(hitList)==0:
        if tfidfModel is not None: # 不重要词汇筛除
            if len(cuttedWord)>=4:
                tfidfMat=tfidfModel.transform([cuttedWord])
                cuttedWordList=[tokenItem 
                                for tokenItem in cuttedWord.split(" ") 
                                if tokenItem in tfidfModel.vocabulary_ and 
                                    tfidfMat[0,tfidfModel.vocabulary_[tokenItem]]>0.2]
                cuttedWord=" ".join(cuttedWordList)
        qbody={
                "query":{
                    "bool":{
                        "must": [
                            {
                                "match": {
                                    "Name": {
                                        "query": cuttedWord,
                                        "minimum_should_match": "{}%".format(int(min(1,stopMinLimit/len(searchWord))*100)) # 削弱全词匹配需求
                                    }
                                }
                            }
                        ],
                        "should":{
                            "match_phrase": {
                                "Name": {
                                    "query":cuttedWord,
                                    "slop": "7"
                                }
                            }
                        }
                }},
                "size":topN
            }
        if withCount==True:
            qbody["sort"]={"count_num":{"order":"desc"}}
        if searchType!="*":
            qbody["query"]["bool"]["must"].append({"term":{"gTagName":"Company"}})
        esReq=esClient.search(index="hr_integrate_kg",body=qbody,timeout='60s')
        hitList=esReq["hits"]["hits"]
        if len(hitList)==0:
            print("死循环：",cuttedWord)
            stopMinLimit-=1
        if stopMinLimit<=0:
            break
    if len(hitList)>0:
        hitDf=pd.DataFrame([hitItem["_source"] for hitItem in hitList])["Name"].dropna()
        return pd.DataFrame(hitDf)
    else:
        return pd.DataFrame([])


def tfidfSearch(gClient,searchWord,searchType="*",searchIdAttr="*",withCount=False,withWeight=False,topN=3000):
    if type(searchWord)==str:
        tokenList=preprocessor.simpleCutWords(searchWord)
    else:
        tokenList=searchWord
    finalSearchList=[]
    nodeTypeDf=wrapNebula2Df(gClient.execute_query("SHOW TAGS"))
    nodeTypeList=nodeTypeDf["Name"].values.flatten().tolist()
    nodeTypeAttrDict={}

    nodeIndexDf=wrapNebula2Df(gClient.execute_query("SHOW TAG INDEXES"))
    nodeIndexList=nodeIndexDf["Index Name"].values.flatten().tolist()
    totalIndexAttrList=[]
    for nodeIndexItem in nodeIndexList:
        indexAttrDf=wrapNebula2Df(gClient.execute_query("DESCRIBE TAG INDEX {}".format(nodeIndexItem)))
        indexAttrList=indexAttrDf["Field"].values.flatten().tolist()
        totalIndexAttrList+=indexAttrList

    if searchType=="*":
        if searchIdAttr=="*":
            for nodeTypeItem in nodeTypeList:
                nodeTypeAttrDf=wrapNebula2Df(gClient.execute_query("DESCRIBE TAG {}".format(nodeTypeItem)))
                nodeTypeAttrList=nodeTypeAttrDf["Field"].values.flatten().tolist()
                nodeTypeAttrList=[nodeTypeAttrItem for nodeTypeAttrItem in nodeTypeAttrList if nodeTypeAttrItem in totalIndexAttrList]
                nodeTypeAttrDict[nodeTypeItem]=nodeTypeAttrDict.get(nodeTypeItem,[])+nodeTypeAttrList
        else:
            raise Exception("searchType为'*'时，searchIdAttr也应为'*'")
    else:
        nodeTypeList=[searchType]

        if searchIdAttr=="*":
            for nodeTypeItem in nodeTypeList:
                nodeTypeAttrDf=wrapNebula2Df(gClient.execute_query("DESCRIBE TAG {}".format(nodeTypeItem)))
                nodeTypeAttrList=nodeTypeAttrDf["Field"].values.flatten().tolist()
                nodeTypeAttrList=[nodeTypeAttrItem for nodeTypeAttrItem in nodeTypeAttrList if nodeTypeAttrItem in totalIndexAttrList]
                nodeTypeAttrDict[nodeTypeItem]=nodeTypeAttrDict.get(nodeTypeItem,[])+nodeTypeAttrList
        else:
            nodeTypeAttrDict[nodeTypeList[0]]=[searchIdAttr]

    tokenSearchList=["LOOKUP ON Token WHERE Token.TokenName=='{}'|\
                        GO FROM $-.VertexID OVER consistOf REVERSELY YIELD $^.Token.TokenName AS TokenName,consistOf._dst AS tailSysId,$$.Company.CompanyName AS CompanyName,consistOf.weight AS weight|\
                            ORDER BY $-.weight DESC|LIMIT {}".format(tokenItem,int(topN/len(searchWord))) for tokenItem in tokenList if tokenItem not in ["公","司"]]
    
    tokenSearchGroupStr=" UNION ".join(tokenSearchList)

    finalSysIdWeightDf=wrapNebula2Df(gClient.execute_query(tokenSearchGroupStr))

    sortColList=["totalScore"]

    if finalSysIdWeightDf.shape[0]>0:
        sysIdList=finalSysIdWeightDf["tailSysId"].astype(str).values.flatten().tolist()
        sysIdListStr=",".join(sysIdList)
        finalSearchStr="FETCH PROP ON * {}".format(sysIdListStr)
        finalSearchReq=gClient.execute_query(finalSearchStr)
        finalSearchTmpDf=wrapNebula2Df(finalSearchReq)

        tailNodeTypeList=list(set([colItem.split(".")[0] for colItem in finalSearchTmpDf.columns if "." in colItem]))
        for nodeTypeItem in tailNodeTypeList:
            # 返回的实体及实体id属性
            idAttrName=nodeTypeAttrDict[nodeTypeItem][0]
            dfIdAttrName="{searchType}.{idAttr}".format(searchType=nodeTypeItem,idAttr=idAttrName)
            finalSearchTmpDf=pd.merge(finalSearchTmpDf,finalSysIdWeightDf,how="left",left_on="VertexID",right_on="tailSysId")
            if withWeight==True:  # 若需要伴随相关分数,需要Token关联的边上有weight属性
                tmpSearchDf=finalSearchTmpDf.groupby(dfIdAttrName).sum("weight").reset_index()
                delist=[colItem for colItem in finalSearchTmpDf.columns if colItem in tmpSearchDf and colItem!="VertexID"]
                finalSearchTmpDf=pd.merge(tmpSearchDf,finalSearchTmpDf.drop(delist,axis=1),left_on="tailSysId",right_on="VertexID",how="left")
            else:
                tmpSearchDf=finalSearchTmpDf.groupby(dfIdAttrName).count().reset_index().drop("weight",axis=1).rename({"VertexID":"weight"},axis=1)
                delist=[colItem for colItem in finalSearchTmpDf.columns if colItem in tmpSearchDf and colItem!="VertexID"]
                finalSearchTmpDf=pd.merge(tmpSearchDf,finalSearchTmpDf.drop(delist,axis=1),left_on="tailSysId",right_on="VertexID",how="left")
            if withCount==True: # 若需要伴随点击量,需要相关节点具有count_num属性
                finalSearchTmpDf=finalSearchTmpDf.groupby(dfIdAttrName).mean("{}.count_num".format(nodeTypeItem)).reset_index()
                sortColList.append("{}.count_num".format(nodeTypeItem))
            finalSearchList.append(finalSearchTmpDf.loc[:,[dfIdAttrName,"weight"]])

    if len(finalSearchList)==0:
        raise Exception("错误：无法查询:{}".format(searchWord))
    finalSearchDf=pd.concat(finalSearchList)

    finalSearchDf["rankScore"]=finalSearchDf["Company.CompanyName"].apply(lambda companyItem:rankScore(searchWord,companyItem))
    finalSearchDf["totalScore"]=finalSearchDf["weight"]+finalSearchDf["rankScore"]
    finalSearchDf=finalSearchDf.sort_values(sortColList,ascending=False).reset_index(drop=True).head(topN)
    end=time.time()
    
    return finalSearchDf

if __name__=="__main__":

    # # test
    # gHost="9.135.95.249"
    # platoAPIPort=7001
    # gPort=13708
    # gUser="root"
    # gPassword="nebula"
    # schemaPath="csv2plato"
    # gSpace="for_kg_search"

    # # product
    # # gHost="10.99.218.40"
    # # platoAPIPort=8081
    # # gPort=8080
    # # gUser="root"
    # # gPassword="nebula"
    # # schemaPath="csv2plato"
    # # gSpace="company_product_field_musklin"

    # gConnection_pool = ConnectionPool(gHost, gPort,network_timeout=300000)
    # gClient = GraphClient(gConnection_pool)
    # gClient.authenticate(gUser, gPassword)
    # gClient.execute_query("USE {}".format(gSpace))
    
    # # print(123)
    # start=time.time()
    # adf=tfidfSearch(gClient,"南昌金科交通科技股份有限公司",withWeight=True,searchType="Company",searchIdAttr="CompanyName",topN=15)
    # end=time.time()
    # print(adf)
    # print("耗时：{}".format(end-start))

    esClient=Elasticsearch(["9.134.92.196:9200"],http_auth=("elastic", "devcloud@123"))
    hitList=esSearch(esClient,"南昌金科交通科技股份有限公司")
    print(hitList)