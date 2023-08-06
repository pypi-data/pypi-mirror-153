from textwrap import wrap
import pandas as pd
import numpy as np
import tqdm
import os
import time
import json
import requests
import gc
import random
from string import punctuation
import argparse
import re
import shutil
from nebula2.gclient.net import ConnectionPool
from nebula2.Config import Config

def wrapNebula2Df(nebulaObj):
    '''将platoDB查询到的对象转为df'''
    # print(nebulaObj.column_names)
    kvDict={}
    if len(nebulaObj.keys())==1 and nebulaObj.keys()[0]=="vertices_":
        kvDict=[]
        for row in nebulaObj.column_values("vertices_"):
            for tagNameItem in row.as_node().tags():
                kvDictItem=dict(list(zip(row.as_node().prop_names(tagNameItem),
                                    [valItem._value.value.decode("utf8") for valItem in row.as_node().prop_values(tagNameItem)])))
                kvDict.append(kvDictItem)
    else:
        keyList=[keyItem for keyItem in nebulaObj.keys()]
        myData=[]
        for row in nebulaObj.rows():
            try:
                rowData=[valItem.value.decode("utf8") 
                            if type(valItem.value)==bytes else valItem.value
                            for valItem in row.values]
                myData.append(rowData)
            except UnicodeDecodeError as ue:
                print("encoding error")
        kvDict=[dict(list(zip(keyList,row))) for row in myData]
    return pd.DataFrame(kvDict).drop_duplicates()

def pdPlatoTypeSame(pdSeries,gType):
    '''pd.DataFrame的series的数据类型是否和gType一致'''
    tmpPdSeries=pdSeries.dropna()
    if gType=="string":
        if tmpPdSeries.dtype==object:
            return True
    elif gType=="int":
        if tmpPdSeries.dtype==np.int64:
            return True
    elif gType=="double":
        if tmpPdSeries.dtype==np.float64:
            return True
    return False

def delEdge(gClient,sysIdList,edgeType="*"):
    '''删除与源节点sysIdList关联的边edgeType'''
    if edgeType=="*":
        relDf=wrapNebula2Df(gClient.execute("SHOW EDGES"))["Name"]
        relList=relDf.values.flatten().tolist()
    else:
        relList=[edgeType]
    for relItem in tqdm.tqdm(relList,desc="del edges"):
        for srcSysIdItem in sysIdList:
            searchRelStr="GO FROM {srcSysId} OVER {edgeName} BIDIRECT YIELD {edgeName}._dst AS tgtSysId".format(
                                                                                                                srcSysId=srcSysIdItem,
                                                                                                                edgeName=relItem)
            print(searchRelStr)
            relTailSysIdDf=wrapNebula2Df(gClient.execute(searchRelStr))
            if relTailSysIdDf.shape[0]>0:
                relTailSysIdList=relTailSysIdDf["tgtSysId"].values.flatten().tolist()
                delOrderGroupStr=",".join(["{}->{}".format(srcSysIdItem,tailSysIdItem) for tailSysIdItem in relTailSysIdList])
                delReverseGroupStr=",".join(["{}->{}".format(tailSysIdItem,srcSysIdItem) for tailSysIdItem in relTailSysIdList])
                delGroupStr=",".join([delOrderGroupStr,delReverseGroupStr])
                delStr="DELETE EDGE {} {}".format(relItem,delGroupStr)
                print(delStr)
                gClient.execute(delStr)

def delVertex(gClient,sysIdList,delRel=True):
    '''（关联）删除节点'''
    delReq={"data":[],"error_code":0}
    if delRel==True:
        relDf=wrapNebula2Df(gClient.execute("SHOW EDGES"))
        if relDf.shape[0]>0:
            relList=relDf["Name"].values.flatten().tolist()
            for relItem in tqdm.tqdm(relList,desc="del edges with vertexes"):
                for srcSysIdItem in tqdm.tqdm(sysIdList,desc="del srcs from edges with vertexes"):
                    relTailStr="GO FROM {srcSysId} OVER {edgeName} BIDIRECT YIELD {edgeName}._dst AS tgtSysId".format(
                        srcSysId=srcSysIdItem,
                        edgeName=relItem)
                    # print(relTailStr)
                    relTailSysIdDf=wrapNebula2Df(gClient.execute(relTailStr))
                    if relTailSysIdDf.shape[0]>0:
                        relTailSysIdList=relTailSysIdDf["tgtSysId"].values.flatten().tolist()
                        delOrderGroupStr=",".join(["{}->{}".format(srcSysIdItem,tailSysIdItem) for tailSysIdItem in relTailSysIdList])
                        delReverseGroupStr=",".join(["{}->{}".format(tailSysIdItem,srcSysIdItem) for tailSysIdItem in relTailSysIdList])
                        delGroupStr=",".join([delOrderGroupStr,delReverseGroupStr])
                        delStr="DELETE EDGE {} {}".format(relItem,delGroupStr)
                        # print(delStr)
                        gClient.execute(delStr)
    # print(sysIdList)
    for batchI in tqdm.tqdm(range(0,len(sysIdList),50),desc="del vertexes"): 
        delVerGroupStr=",".join([str(sysIdItem) for sysIdItem in sysIdList[batchI:batchI+50]])
        delStr="DELETE VERTEX {}".format(delVerGroupStr)
        # print(delStr)
        delReq=gClient.execute(delStr)
    return delReq
                
def existTag(nodeType,nodeIdAttr,nodeName,gClient):
    '''查看nodeType的nodeIdAttr为nodeName的节点是否在gClient中（gClient提前设定好图数据库）'''
    passTag=0
    while passTag<5:
        try:
            searchTagDf=wrapNebula2Df(gClient.execute("LOOKUP ON {nodeType} WHERE {nodeType}.{nodeIdAttr}=='{nodeName}'|LIMIT 1".format(
                nodeType=nodeType,
                nodeIdAttr=nodeIdAttr,
                nodeName=nodeName
            )))
            if searchTagDf.shape[0]>0:
                return True
            else:
                passTag+=1
        except:
            passTag+=1
    return False

def transferBetweenPlato(gHost,gPort,gUser,gPassword,
                         srcGdbName,tgtGdbName,tgtGAPIUrl,edgeTypeList=[],
                         srcVertexKeynameDict={"srcNodeType":"srcNodeIdAttr"},csv2platoDTypeDict={"srcNodeIdAttr":"string"},
                         batchSize=64,projectName="",platoAPIIP="",platoAPIPort=8083):
    '''图数据库之间数据转换'''
    
    srcConnection_pool = ConnectionPool(gHost, gPort,network_timeout=300000)
    srcClient = GraphClient(srcConnection_pool)
    srcClient.authenticate(gUser, gPassword)
    srcClient.execute("use {}".format(srcGdbName))

    tgtConnection_pool = ConnectionPool(gHost, gPort,network_timeout=300000)
    tgtClient = GraphClient(tgtConnection_pool)
    tgtClient.authenticate(gUser, gPassword)
    tgtClient.execute("use {}".format(tgtGdbName))

    # 1.构建data的项目

    # 获取schema
    srcVertexTypeDf=wrapNebula2Df(srcClient.execute("SHOW TAGS"))
    srcVertexTypeAttrSetDict={}
    for srcVertexTypeItem in srcVertexTypeDf["Name"].values.tolist():
        tagTypeListStr="DESCRIBE TAG {}".format(srcVertexTypeItem)
        srcVertexInfoDf=wrapNebula2Df(srcClient.execute(tagTypeListStr))
        srcVertexTypeAttrSetDict[srcVertexTypeItem]=dict(srcVertexInfoDf.loc[:,["Field","Type"]].values.tolist())
    
    srcEdgeTypeDf=wrapNebula2Df(srcClient.execute("SHOW EDGES"))
    srcEdgeTypeAttrSetDict={}
    for srcEdgeTypeItem in srcEdgeTypeDf["Name"].values.tolist():
        if len(edgeTypeList)==0 or srcEdgeTypeItem in edgeTypeList:
            edgeTypeListStr="DESCRIBE EDGE {}".format(srcEdgeTypeItem)
            srcEdgeInfoDf=wrapNebula2Df(srcClient.execute(edgeTypeListStr))
            srcEdgeTypeAttrSetDict[srcEdgeTypeItem]=dict(srcEdgeInfoDf.loc[:,["Field","Type"]].values.tolist())
    
    # 构建schema
    for srcVertexTypeAttrSetItem in srcVertexTypeAttrSetDict:
        srcVertexTypeSet=srcVertexTypeAttrSetDict[srcVertexTypeAttrSetItem]
        attrList=["{} {}".format(srcVertexTypeItem,srcVertexTypeSet[srcVertexTypeItem] if srcVertexTypeSet[srcVertexTypeItem] not in ["int","double"] else srcVertexTypeSet[srcVertexTypeItem]+" DEFAULT 0") for srcVertexTypeItem in srcVertexTypeSet]
        attrList.append("from_kb string")
        tagAttrStr=",".join(attrList)
        buildTagSchemaStr="CREATE TAG IF NOT EXISTS {}({}) ".format(srcVertexTypeAttrSetItem,tagAttrStr)
        tgtClient.execute(buildTagSchemaStr)

    
    for srcEdgeTypeAttrSetItem in srcEdgeTypeAttrSetDict:
        srcEdgeTypeSet=srcEdgeTypeAttrSetDict[srcEdgeTypeAttrSetItem]
        attrList=["{} {}".format(srcEdgeTypeItem,srcEdgeTypeSet[srcEdgeTypeItem]) for srcEdgeTypeItem in srcEdgeTypeSet]
        attrList.append("from_kb string")
        edgeAttrStr=",".join(attrList)
        buildEdgeSchemaStr="CREATE EDGE IF NOT EXISTS {}({}) ".format(srcEdgeTypeAttrSetItem,edgeAttrStr)
        tgtClient.execute(buildEdgeSchemaStr)

    # 构建index
    for vertexTypeItem in srcVertexKeynameDict:
        tagIndexName="{}_{}_index".format(vertexTypeItem.lower(),srcVertexKeynameDict[vertexTypeItem].lower())
        tgtClient.execute("CREATE TAG INDEX IF NOT EXISTS {} ON {}({})".format(tagIndexName,vertexTypeItem,srcVertexKeynameDict[vertexTypeItem]))
        tgtClient.execute("REBUILD TAG INDEX {} OFFLINE".format(tagIndexName))

    # 获取nebula graph导入形式的数据
    if len(projectName)==0:
        projectName="tmpProject_{}".format(int(time.time()*1000))
    if "csv2plato" not in os.listdir("."):
        os.mkdir("csv2plato")
    if projectName not in os.listdir("csv2plato"):
        os.mkdir("csv2plato/"+projectName)
    rawSchemaJson={
        "gDbName":tgtGdbName,
        "coverOldData":True, 
        "vertex":[],
        "edge":[]
    }
    vertexRecordList=[]
    edgeRecordList=[]
    for srcVertexTypeItem in tqdm.tqdm(srcVertexKeynameDict):
        batchI=0
        while True:
            vertexSysIdDf=wrapNebula2Df(srcClient.execute("LOOKUP ON {vertexType} WHERE {vertexType}.{attrKeyname}!='不可能的名字'|LIMIT {batchI},{batchSize}".format(
                                                                                                                                                vertexType=srcVertexTypeItem,
                                                                                                                                                attrKeyname=srcVertexKeynameDict[srcVertexTypeItem],
                                                                                                                                                batchI=batchI,
                                                                                                                                                batchSize=batchSize
            )))
            if vertexSysIdDf.shape[0]==0:
                break
            vertexSysIdList=vertexSysIdDf["VertexID"].values.tolist()
            vertexSysIdList=[str(vertexSysIdItem) for vertexSysIdItem in vertexSysIdList]

            vertexInfoDf=wrapNebula2Df(srcClient.execute("FETCH PROP ON {} {}".format(srcVertexTypeItem,",".join(vertexSysIdList))))
            while vertexInfoDf.shape[0]==0:
                vertexInfoDf=wrapNebula2Df(srcClient.execute("FETCH PROP ON {} {}".format(srcVertexTypeItem,",".join(vertexSysIdList))))
                print("line wrong,check!")
            columnList=list(vertexInfoDf.columns)
            columnRenameDict=dict((colItem,colItem.split(".")[1]) for colItem in columnList if "." in colItem)
            vertexInfoDf.rename(columnRenameDict,axis=1,inplace=True)
            vertexInfoDf.drop("VertexID",axis=1,inplace=True)
            vertexInfoDf["{}SysId".format(srcVertexTypeItem)]=vertexInfoDf["{}".format(srcVertexKeynameDict[srcVertexTypeItem])].apply(lambda row:"{}".format(srcVertexTypeItem)+"_"+row)
            vertexInfoDf["from_kb"]=srcGdbName
            if batchI==0:
                vertexInfoDf.to_csv("csv2plato/{}/{}Node-fornew.csv".format(projectName,srcVertexTypeItem),index=None)
            else:
                vertexInfoDf.to_csv("csv2plato/{}/{}Node-fornew.csv".format(projectName,srcVertexTypeItem),header=None,index=None,mode="a")
            csv2platoAttrMapDict=dict((colItem,colItem) for colItem in vertexInfoDf.columns)
            csvAttrTypeDict=dict((colItem,csv2platoDTypeDict[vertexInfoDf[colItem].dtype.name]) for colItem in vertexInfoDf.columns)

            if srcVertexTypeItem not in vertexRecordList:
                rawSchemaJson["vertex"].append({
                    "file_name":"{}Node-fornew.csv".format(srcVertexTypeItem),
                    "node_type":srcVertexTypeItem,
                    "id_col":srcVertexKeynameDict[srcVertexTypeItem],
                    "csv2plato_attr_map":csv2platoAttrMapDict,
                    "attr_type_map":csvAttrTypeDict
                })
                vertexRecordList.append(srcVertexTypeItem)

            for srcEdgeTypeItem in srcEdgeTypeAttrSetDict:
                for tgtVertexTypeItem in srcVertexKeynameDict:
                    attrListStr=",".join(["{}.{}".format(srcEdgeTypeItem,edgeItem) for edgeItem in srcEdgeTypeAttrSetDict[srcEdgeTypeItem]])
                    if len(attrListStr)==0:
                        attrListStr=""
                    else:
                        attrListStr=","+attrListStr
                    goDf=wrapNebula2Df(srcClient.execute("GO FROM {headSysId} OVER {edge} YIELD $^.{headType}.{headKeyname} AS headId,$$.{tailType}.{tailKeyname} AS tailId{attrList}".format(
                        headSysId=",".join(vertexSysIdList),
                        edge=srcEdgeTypeItem,
                        headType=srcVertexTypeItem,
                        headKeyname=srcVertexKeynameDict[srcVertexTypeItem],
                        tailType=tgtVertexTypeItem,
                        tailKeyname=srcVertexKeynameDict[tgtVertexTypeItem],
                        attrList=attrListStr
                    )))
                    goDf["from_kb"]=srcGdbName
                    goDf.replace("",np.nan,inplace=True)
                    goDf.dropna(inplace=True)
                    if goDf.shape[0]>0:

                        goDf["headId"]=goDf["headId"].apply(lambda row:"{}_".format(srcVertexTypeItem)+row)
                        goDf["tailId"]=goDf["tailId"].apply(lambda row:"{}_".format(tgtVertexTypeItem)+row)
                        columnRenameDict=dict((colItem,colItem.split(".")[1]) for colItem in goDf.columns if "." in colItem)
                        goDf.rename(columnRenameDict,axis=1,inplace=True)

                        if "{}Rel-fornew.csv".format(srcEdgeTypeItem) not in os.listdir("csv2plato/{}/".format(projectName)):
                            goDf.to_csv("csv2plato/{}/{}Rel-fornew.csv".format(projectName,srcEdgeTypeItem),index=None)
                        else:
                            goDf.to_csv("csv2plato/{}/{}Rel-fornew.csv".format(projectName,srcEdgeTypeItem),index=None,header=None,mode="a")
                        
                        csv2platoAttrMapDict=dict((colItem,colItem) for colItem in goDf.columns if colItem not in ["headId","tailId"])
                        csvAttrTypeDict=dict((colItem,csv2platoDTypeDict[goDf[colItem].dtype.name]) for colItem in goDf.columns if colItem not in ["headId","tailId"])
                        
                        if srcEdgeTypeItem not in edgeRecordList:
                            rawSchemaJson["edge"].append({
                                "file_name":"{}Rel-fornew.csv".format(srcEdgeTypeItem),
                                "edge_type":srcEdgeTypeItem,
                                "src_type":srcVertexTypeItem,
                                "tgt_type":tgtVertexTypeItem,
                                "src_id":"headId",
                                "tgt_id":"tailId",
                                "csv2plato_attr_map":csv2platoAttrMapDict,
                                "attr_type_map":csvAttrTypeDict
                            })
                            edgeRecordList.append(srcEdgeTypeItem)

            batchI+=batchSize

    with open("csv2plato/{}/rawSchema.json".format(projectName),"w+",encoding="utf8") as rawSchemaJsonFile:
        json.dump(rawSchemaJson,rawSchemaJsonFile)

    fileList=[]
    closedFileList=[]
    for fileItem in tqdm.tqdm(os.listdir("csv2plato/"+projectName)):
        uploadedFile=open("csv2plato/"+projectName+"/"+fileItem,'rb')
        if fileItem.split(".")[1]=="csv":
            fileList.append(("csv",(fileItem,uploadedFile,"test/csv")))
        if fileItem.split(".")[1]=="json":
            fileList.append(("json",(fileItem,uploadedFile,"application/json")))
        closedFileList.append(uploadedFile)

    tgtGAPIUrl=tgtGAPIUrl
    fileServerUrl="{}/csv2platodb/upload".format(tgtGAPIUrl)
    response = requests.request("POST", fileServerUrl, files=fileList)
    
    for fileItem in closedFileList:
        fileItem.close()
    shutil.rmtree("csv2plato/"+projectName)
        
    print(response.text)
    return response

def existEdge(headType,headIdAttr,headIdVal,tailType,tailIdAttr,tailIdVal,edgeType,edgeDir,gClient):
    '''查看头节点为headIdVal，尾节点为tailIdVal的edgeType边是否存在（gClient提前设定好图数据库）'''
    searchEdgeDf=wrapNebula2Df(gClient.execute("LOOKUP ON {headType} WHERE {headType}.{headIdAttr}=='{headIdVal}'|\
                                                        GO FROM $-.VertexID OVER {edgeType} {edgeDir} WHERE  $$.{tailType}.{tailIdAttr}=='{tailIdVal}'|LIMIT 1\
                                                            YIELD $$.{tailType}.{tailIdAttr}".format(
                                                                                                headType=headType,
                                                                                                headIdAttr=headIdAttr,
                                                                                                headIdVal=headIdVal,
                                                                                                edgeType=edgeType,
                                                                                                edgeDir=edgeDir,
                                                                                                tailType=tailType,
                                                                                                tailIdAttr=tailIdAttr,
                                                                                                tailIdVal=tailIdVal
                                                                                            )))
    if searchEdgeDf.shape[0]>0:
        return True
    return False

def nlpPreprocessAttr(gClient,nodeType,nodeIdAttrName,nodeAttrName,tabuStr=""):
    '''图数据库属性的文本预处理'''
    tabuStr="\\/'"+tabuStr+punctuation
    nodeSysIdDf=wrapNebula2Df(gClient.execute("LOOKUP ON {nodeType} WHERE {nodeType}.{nodeIdAttr}!='不可能的名字'\
                                                        YIELD {nodeType}.{nodeAttr} AS tgtAttr".format(nodeType=nodeType,
                                                                                            nodeIdAttrName=nodeIdAttrName,
                                                                                            nodeAttrName=nodeAttrName)))
    if nodeSysIdDf.shape[0]>0:
        nodeSysIdDf["tgtAttr"]=nodeSysIdDf["tgtAttr"].apply(lambda row:re.sub("["+tabuStr+"]","",row))
        nodeSysIdAttrList=nodeSysIdDf.loc[:,["VertexID","tgtAttr"]].values.tolist()
        for nodeSysId,nodeAttrVal in nodeSysIdAttrList:
            gClient.execute("UPDATE VERTEX {nodeSysId} SET {nodeType}.{nodeAttr}='{nodeVal}'".format(
                                                                                                            nodeSysId=nodeSysId,
                                                                                                            nodeType=nodeType,
                                                                                                            nodeAttr=nodeAttrName,
                                                                                                            nodeVal=nodeAttrVal
                                                                                                        ))
        
        
    

def addTokenForEntities(gClient,gDBName,nodeIdAttrList,tabuList=[],projectName="",email=""):
    '''构建实体的token实体'''
    if "csv2platodb" not in os.listdir("."):
        os.mkdir("csv2platodb")
        
    if len(projectName)==0:
        projectName="tmp_{}".format(int(time.time()*1000))
        os.mkdir("csv2platodb/{}".format(projectName))
    
    if len(tabuList)==0:
        tabuList=list(punctuation)+["“","”","‘","’","，","。"]
    
    # 构建节点和边的数据
    schemaVertex=[]
    schemaEdge=[]
    for nodeItdPairItem in nodeIdAttrList:
        
        nodeType=nodeItdPairItem.split(".")[0]
        nodeIdAttr=nodeItdPairItem.split(".")[1]
        
        tgtNameDf=wrapNebula2Df(gClient.execute("LOOKUP ON {nodeType} WHERE {nodeType}.{nodeIdAttr}!='不可能的名字' \
                                                        YIELD {nodeType}.{nodeIdAttr} AS tgtName".format(nodeType=nodeType,
                                                                                                          nodeIdAttr=nodeIdAttr)))
        srcTokenPairList=[]
        tokenInfoList=[]
        for tgtNameItem in tqdm.tqdm(tgtNameDf["tgtName"].values.flatten().tolist(),desc=nodeType):
            tgtNameItem=tgtNameItem.lower()
            for tgtNameTokenItem in tgtNameItem:
                if tgtNameTokenItem not in tabuList:
                    tokenInfoList.append({"Name":tgtNameTokenItem})
                # print({"headEntity":tgtNameItem,"tailEntity":tgtNameTokenItem})
                srcTokenPairList.append({"headEntity":tgtNameItem,"tailEntity":tgtNameTokenItem})
        srcTokenPairDf=pd.DataFrame(srcTokenPairList)
        tokenInfoDf=pd.DataFrame(tokenInfoList)
            
        tokenInfoDf.to_csv("./csv2platodb/{}/tokenInfo_{}.csv".format(projectName,nodeType),index=None)
        srcTokenPairDf.to_csv("./csv2platodb/{}/consistOfRel_{}.csv".format(projectName,nodeType),index=None)
        
        schemaVertex.append({ 
                                "file_name":"tokenInfo_{}.csv".format(nodeType),
                                "node_type":"Token",
                                "id_col":"Name", 
                                "csv2plato_attr_map":{ 
                                    "Name":"Name"
                                },
                                "attr_type_map":{ 
                                    "Name":"string"
                                }
                            })
        schemaEdge.append({
                                "file_name":"consistOfRel_{}.csv".format(nodeType),
                                "edge_type":"consistOf",
                                "src_type":nodeType,
                                "tgt_type":"Token",
                                "src_id":"headEntity",
                                "tgt_id":"tailEntity",
                                "csv2plato_attr_map":{},
                                "attr_type_map":{}
                            })
    # 构建数据schema
    VESchema={
        "gDbName":gDBName,
        "vertex":schemaVertex,
        "edge":schemaEdge,
        "email":email
    }
    if len(email)==0:
        VESchema.pop("email")
    
    with open("./csv2platodb/{}/rawSchema.json".format(projectName,nodeType),"w+",encoding="utf8") as VESchemaFile:
        json.dump(VESchema,VESchemaFile)
    
    print("本地文件生成")
    return VESchema

def ucreateGDB(gClient,gdbname):
    '''创建图数据库'''
    gClient.execute("CREATE SPACE {}".format(gdbname))
    
def ucreateTag(gClient,tagAttrTypeDefaultDict,defaultTagAttrTypeDict={"Alias":{"Name":{"type":"string","default":"null"},
                                                                                "checked":{"type":"string","default":"false"},
                                                                                "from_kg":{"type":"string","default":""}}}):
    '''创建标签'''
    for tagTypeItem in tagAttrTypeDefaultDict:
        attrList=["{} {} DEFAULT {}".format(attrNameKeyItem,
                                                tagAttrTypeDefaultDict[attrNameKeyItem]["type"],
                                                tagAttrTypeDefaultDict[attrNameKeyItem]["default"]) for attrNameKeyItem in tagAttrTypeDefaultDict[tagTypeItem]]
        attrListStr=",".join(attrList)
        gClient.execute("CREATE TAG IF NOT EXISTS {} ({})".format(tagTypeItem,attrListStr))

def ucreateEdge(gClient,edgeAttrTypeDefaultDict,defaultEdgeAttrTypeDict={"alias":{"checked":{"type":"string","default":"false"},
                                                                                "from_kg":{"type":"string","default":""}}}):
    '''创建边'''
    for tagTypeItem in edgeAttrTypeDefaultDict:
        attrList=["{} {} DEFAULT {}".format(attrNameKeyItem,
                                                edgeAttrTypeDefaultDict[attrNameKeyItem]["type"],
                                                edgeAttrTypeDefaultDict[attrNameKeyItem]["default"]) for attrNameKeyItem in edgeAttrTypeDefaultDict[tagTypeItem]]
        attrListStr=",".join(attrList)
        gClient.execute("CREATE EDGE IF NOT EXISTS {} ({})".format(tagTypeItem,attrListStr))

from maintain_PlatoUtils.v2 import maintain_csv2platodb_A_uploadFile
from maintain_PlatoUtils.v2 import maintain_csv2platodb_B_submitSchema
from maintain_PlatoUtils.v2 import maintain_csv2platodb_C_import
def uploadGraph(gClient,folderName,cookie,
                    tgtGdbUser,tgtGdbPassword,tgtGdbHost,tgtGdbPort,
                    tgtGOfficialAPI):
    '''上传图数据库'''
    uploadSchemaJson["force"]=uploadSchemaJson.get("force",False)
    maintain_csv2platodb_A_uploadFile.buildGraphDB(gClient,
                                                    uploadSchemaJson,
                                                    realDbName=uploadSchemaJson["gDbName"],
                                                    force=uploadSchemaJson.get("force",False))
    useSpaceStr="USE {}".format(uploadSchemaJson["gDbName"])
    gClient.execute(useSpaceStr)
    gClient.set_space(uploadSchemaJson["gDbName"])
    uploadSchemaJson.pop("force")
    uploadSchemaJson=maintain_csv2platodb_A_uploadFile.remakeRawSchema(uploadSchemaJson,csvFolder=folderName,gClient=gClient)
    with open(folderName+"/uploadSchema.json","w+",encoding="utf8") as uploadSchemaJsonFile:
        json.dump(uploadSchemaJson,uploadSchemaJsonFile)
    
    print("uploading ...",tgtGOfficialAPI)
    maintain_csv2platodb_A_uploadFile.uploadFolder(folderName,tgtGOfficialAPI,cookie=cookie)
    
    with open(folderName+"/uploadSchema.json","r") as uploadSchemaFile:
        uploadSchemaJson=json.load(uploadSchemaFile)
    gspace=uploadSchemaJson["gDbName"]
    
    maintain_csv2platodb_B_submitSchema.createSchemaFromSchemaJson(uploadSchemaJson,graphClient=gClient)
    gClient.execute("USE {}".format(gspace))
    gClient.set_space(gspace)
    
    vertexJsonList=[]
    edgeJsonList=[]
    if "vertex" in uploadSchemaJson:
        vertexJsonList=maintain_csv2platodb_B_submitSchema.buildVertex(uploadSchemaJson["vertex"],graphClient=gClient)
    if "edge" in uploadSchemaJson:
        edgeJsonList=maintain_csv2platodb_B_submitSchema.buildEdge(uploadSchemaJson["edge"],graphClient=gClient)
        
    time.sleep(15) # 构造完成schema后延时15秒
    
    schemaJson={
        "version": "v2",
        "description": "web console import",
        "clientSettings": {
            "concurrency": 10,
            "channelBufferSize": 128,
            "space": gspace,
            "connection": {
                "user": tgtGdbUser,
                "password": tgtGdbPassword,
                "address": "{}:{}".format(tgtGdbHost,tgtGdbPort)
            }
        },
        "logPath": "./tmp/import.log",
        "files": vertexJsonList+edgeJsonList
    }
    with open(folderName+"/schemaJson.json","w+") as schemaJsonFile:
        json.dump(schemaJson,schemaJsonFile)
        
    taskId=maintain_csv2platodb_B_submitSchema.submitSchema(schemaJson,gUrl=tgtGOfficialAPI,cookie=cookie)
    maintain_csv2platodb_C_import.importData(tgtGOfficialAPI,taskId=taskId,cookie=cookie)

def downloadGraph(gClient,
                    srcGdbName,srcFakeGdbName,
                    edgeTypeList=[],
                    srcVertexKeynameDict={"srcNodeType":"srcNodeIdAttr"}):
    
    '''以上传的格式下载图数据'''
    if "downloadGraph" not in os.listdir("."):
        os.mkdir("downloadGraph")
    rawSchema={"gDbName":srcFakeGdbName,"vertex":[],"edge":[]}
    gClient.execute("USE {}".format(srcGdbName))
    downloadFolderName="tmp_{}".format(int(time.time()*1000))
    if downloadFolderName not in os.listdir("./downloadGraph"):
        os.mkdir("./downloadGraph/"+downloadFolderName)
    for srcVertexTypeItem in srcVertexKeynameDict:
        lookupVertexGroupStr="LOOKUP ON {nodeType} WHERE {nodeType}.{nodeIdAttr}!='不可能的名字'|FETCH PROP ON {nodeType} $-.VertexID".format(
                                                                                                                                                nodeType=srcVertexTypeItem,
                                                                                                                                                nodeIdAttr=srcVertexKeynameDict[srcVertexTypeItem]
                                                                                                                                            )
        vertexDfItem=wrapNebula2Df(gClient.execute(lookupVertexGroupStr))
        renameColumnDict=dict((colItem,colItem.split(".")[1])
                                if "." in colItem else (colItem,colItem) 
                                for colItem in vertexDfItem.columns)
        vertexDfItem.rename(renameColumnDict,axis=1,inplace=True)
        
        vertexAttrDTypeDf=wrapNebula2Df(gClient.execute("DESCRIBE TAG {}".format(srcVertexTypeItem)))
        vertexAttrList=vertexAttrDTypeDf["Field"].values.flatten().tolist()
        # csv2platodb
        csv2platoDBAttrDict=dict((colItem,colItem) for colItem in vertexDfItem.columns if colItem not in vertexAttrList)
        
        # platoAttrType
        attrDTypeDict=dict(vertexAttrDTypeDf.values.tolist())
        for colItem in vertexDfItem.columns:
            if colItem in attrDTypeDict:
                if attrDTypeDict[colItem]=="string":
                    vertexDfItem[colItem].fillna("null",inplace=True)
                    vertexDfItem[colItem]=vertexDfItem[colItem].astype(str)
                elif attrDTypeDict[colItem]=="int":
                    vertexDfItem[colItem].fillna(0,inplace=True)
                    vertexDfItem[colItem]=vertexDfItem[colItem].astype(int)
                elif attrDTypeDict[colItem]=="double":
                    vertexDfItem[colItem].fillna(0.0,inplace=True)
                    vertexDfItem[colItem]=vertexDfItem[colItem].astype(float)
        
        vertexDfItem.to_csv("./downloadGraph/{}/{}.csv".format(downloadFolderName,srcVertexTypeItem),index=None)
        vertexSchemaItem={
                            "cover_label":"escape,cover",
                            "file_name":"{}.csv".format(srcVertexTypeItem),
                            "node_type":srcVertexTypeItem,
                            "id_col":srcVertexKeynameDict[srcVertexTypeItem], 
                            "csv2plato_attr_map":csv2platoDBAttrDict,
                            "attr_type_map":attrDTypeDict
                        }
        rawSchema["vertex"].append(vertexSchemaItem)
        
    for edgeTypeItem in edgeTypeList:
        for srcVertexTypeItem_head in srcVertexKeynameDict:
            for tgtVertexTypeItem_tail in srcVertexKeynameDict:
                edgeLookupReq=gClient.execute("LOOKUP ON {srcNodeType} WHERE {srcNodeType}.{srcNodeIdAttr}!='不可能的名字'|\
                                                        GO FROM $-.VertexID OVER {edgeType} YIELD   {edgeType}._src AS srcSysID,\
                                                                                                    {edgeType}._dst AS tgtSysID,\
                                                                                                    $^.{srcNodeType}.{srcNodeIdAttr} AS srcSysID,\
                                                                                                    $$.{tgtNodeType}.{tgtNodeIdAttr} AS tgtSysID".format(
                                                                                                        srcNodeType=srcVertexTypeItem_head,
                                                                                                        srcNodeIdAttr=srcVertexKeynameDict[srcVertexTypeItem_head],
                                                                                                        edgeType=edgeTypeItem,
                                                                                                        tgtNodeType=tgtVertexTypeItem_tail,
                                                                                                        tgtNodeIdAttr=srcVertexKeynameDict[tgtVertexTypeItem_tail]
                                                                                                    ))
                edgeLookupDf=wrapNebula2Df(edgeLookupReq).dropna()
                
                edgeSysIdList=edgeLookupDf.loc[:,["srcSysID","tgtSysID"]].astype(str).values.tolist()
                edgeSysIdListStr=",".join(["->".join(edgeSysIdItem) for edgeSysIdItem in edgeSysIdList])
                edgeFetchReq=gClient.execute("FETCH PROP ON {edgeType} {edgeList}".format(
                                                                                                    edgeType=edgeTypeItem,
                                                                                                    edgeList=edgeSysIdListStr
                                                                                                ))
                edgeFetchDf=wrapNebula2Df(edgeFetchReq)
                
                edgeDfItem=pd.merge(edgeLookupDf,edgeFetchDf,
                                    left_on=["srcSysID","tgtSysID"],
                                    right_on=["{edgeType}._src".format(edgeType=edgeTypeItem),
                                              "{edgeType}._dst".format(edgeType=edgeTypeItem)])
                renameColDict=dict((colItem,colItem.split(".")[1])
                                    if "." in colItem else (colItem,colItem)
                                    for colItem in edgeDfItem.columns)
                edgeDfItem.rename(renameColDict,axis=1,inplace=True)
                
                edgeAttrDTypeDf=wrapNebula2Df(gClient.execute("DESCRIBE EDGE {}".format(edgeTypeItem)))
                edgeAttrList=edgeAttrDTypeDf["Field"].values.flatten().tolist()
                # csv2platodb
                csv2platoAttrDict=dict((colItem,colItem) for colItem in vertexDfItem.columns  if colItem in edgeAttrList)
                
                # platoAttrType
                attrDTypeDict=dict(edgeAttrDTypeDf.values.tolist())
                for colItem in edgeDfItem.columns:
                    if colItem in attrDTypeDict:
                        if attrDTypeDict[colItem]=="string":
                            edgeDfItem[colItem].fillna("null",inplace=True)
                            edgeDfItem[colItem]=edgeDfItem[colItem].astype(str)
                        elif attrDTypeDict[colItem]=="int":
                            edgeDfItem[colItem].fillna(0,inplace=True)
                            edgeDfItem[colItem]=edgeDfItem[colItem].astype(int)
                        elif attrDTypeDict[colItem]=="double":
                            edgeDfItem[colItem].fillna(0.0,inplace=True)
                            edgeDfItem[colItem]=edgeDfItem[colItem].astype(float)
                
                edgeDfItem.to_csv("./downloadGraph/{}/{}.csv".format(downloadFolderName,edgeTypeItem),index=None)
                edgeSchemaItem={
                    "cover_label":"escape,escape,cover",
                    "file_name":"{}.csv".format(edgeTypeItem),
                    "edge_type":edgeTypeItem,
                    "src_type":srcVertexTypeItem_head,
                    "tgt_type":tgtVertexTypeItem_tail,
                    "src_id":"{srcNodeType}{srcNodeIdAttr}_head".format(srcNodeType=srcVertexTypeItem_head,srcNodeIdAttr=srcVertexKeynameDict[srcVertexTypeItem_head]),
                    "tgt_id":"{tgtNodeType}{tgtNodeIdAttr}_tail".format(tgtNodeType=tgtVertexTypeItem_tail,tgtNodeIdAttr=srcVertexKeynameDict[tgtVertexTypeItem_tail]),
                    "csv2plato_attr_map":csv2platoAttrDict,
                    "attr_type_map":attrDTypeDict
                }
                
                rawSchema["edge"].append(edgeSchemaItem)
                
    
    with open("./downloadGraph/{}/rawSchema.json".format(downloadFolderName),"w+") as rawSchemaFile:
        json.dump(rawSchema,rawSchemaFile)
        
    print("文件已保存于{}".format(downloadFolderName))


if __name__=="__main__":
    
    # test
    # gHost="9.135.95.249"
    # gPort=13708
    # gUser="root"
    # gPassword="nebula"
    # gdbName="post_skill_school_ianxu"

    # cloud
    gHost="124.221.69.218"
    platoAPIPort=7001
    gPort=9669
    gUser="root"
    gPassword="nebula"
    gSpace="CompanyInfo_KG"

    gConfig = Config()
    gConfig.max_connection_pool_size = 10
    connection_pool = ConnectionPool()
    ok = connection_pool.init([(gHost, gPort)], gConfig)
    gClient = connection_pool.get_session(gUser, gPassword)
    
    # start=time.time()
    adf=wrapNebula2Df(gClient.execute("SHOW SPACES"))
    # end=time.time()
    # print(end-start)
    
    print(adf.head())
    
    # srcVertexKeynameDict={
    #     "Skill":"SkillName"
    # }
    # edgeTypeList=["relate"]

    # gHost="9.135.95.249"
    # gPort=13708
    # gUser="root"
    # gPassword="nebula"
    # srcGdbName="post_dept_char_major_skill__wliangwang"
    # tgtGdbName="post_skill_school_ianxu"
    # tgtGAPIUrl="http://{}:8083".format("9.135.95.249")
    
    # projectName="transfer_skills"

    # batchSize=1024
    # myDfList=[]

    # csv2platoDTypeDict={
    #     "object":"string",
    #     "float64":"double",
    #     "int64":"int",
    # }
    
    # transferBetweenPlato(gHost,gPort,gUser,gPassword,
    #                      srcGdbName,tgtGdbName,tgtGAPIUrl,
    #                      edgeTypeList=edgeTypeList,
    #                      srcVertexKeynameDict=srcVertexKeynameDict,
    #                      csv2platoDTypeDict=csv2platoDTypeDict,
    #                      projectName=projectName)
    
    # downloadGraph(srcClient,"post_skill_school_ianxu","post_tag",
    #               edgeTypeList=["subPost"],
    #               srcVertexKeynameDict={"YunPost":"YunPostName"}
    #               )
