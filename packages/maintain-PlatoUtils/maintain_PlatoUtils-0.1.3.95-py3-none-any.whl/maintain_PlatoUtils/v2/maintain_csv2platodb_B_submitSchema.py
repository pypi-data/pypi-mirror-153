from nebula.graph import ttypes,GraphService
from nebula.ConnectionPool import ConnectionPool
from nebula.Client import GraphClient
from maintain_PlatoUtils.v2.maintain_PlatoUtils import wrapNebula2Df,pdPlatoTypeSame
import pandas as pd
import json
import os
import requests
import numpy as np

def buildVertex(vertexJson,graphClient,nodeSysIDUUID=True,serverPath="/usr/local/nebula-graph-studio/nebula-graph-studio/tmp/upload"):

    vertexJsonList=[]
    for vertexInfoItem in vertexJson:
        vertexPath=vertexInfoItem["file_path"]
        vertexFileName=vertexInfoItem["file_name"].split(".")[0]+"_copy.csv"
        csv2plato_attr_map=vertexInfoItem["csv2plato_attr_map"]
        csv_attr2type_map=vertexInfoItem["attr_type_map"]
        nodeType=vertexInfoItem["node_type"]
        idCol=vertexInfoItem["id_col"]
        vertexDf=pd.read_csv(vertexPath)
        
        gNodeAttrDf=wrapNebula2Df(graphClient.execute("DESCRIBE TAG {}".format(nodeType)))
        
        attrTypeList=[]
        if gNodeAttrDf.shape[0]>0:
            gNodeAttrList=gNodeAttrDf["Field"].values.flatten().tolist()
            
            for attrKeyItem in csv_attr2type_map:
                if attrKeyItem in  csv2plato_attr_map and csv2plato_attr_map[attrKeyItem] in gNodeAttrList:
                    if attrKeyItem==idCol:
                        attrTypeList.append({
                                "name": csv2plato_attr_map[attrKeyItem],
                                "type": "string",
                                "index": list(vertexDf.columns).index(attrKeyItem)
                            })
                    else:
                        if pdPlatoTypeSame(vertexDf[attrKeyItem],csv_attr2type_map[attrKeyItem]):
                            attrTypeList.append({
                                    "name": csv2plato_attr_map[attrKeyItem],
                                    "type": csv_attr2type_map[attrKeyItem],
                                    "index": list(vertexDf.columns).index(attrKeyItem)
                                })
                        elif csv_attr2type_map[attrKeyItem]=="string":
                            vertexDf[attrKeyItem]=vertexDf[attrKeyItem].fillna("null")
                            vertexDf[attrKeyItem]=vertexDf[attrKeyItem].astype(str)
                            attrTypeList.append({
                                    "name": csv2plato_attr_map[attrKeyItem],
                                    "type": csv_attr2type_map[attrKeyItem],
                                    "index": list(vertexDf.columns).index(attrKeyItem)
                                })
                        elif csv_attr2type_map[attrKeyItem]=="int" and vertexDf[attrKeyItem].dtype==np.float64:
                            vertexDf[attrKeyItem].fillna(0,inplace=True)
                            vertexDf[attrKeyItem]=vertexDf[attrKeyItem].astype(int)
                            attrTypeList.append({
                                    "name": csv2plato_attr_map[attrKeyItem],
                                    "type": csv_attr2type_map[attrKeyItem],
                                    "index": list(vertexDf.columns).index(attrKeyItem)
                                })
                        else:
                            raise TypeError("csv({}_{})与uploadSchema.json类型冲突，请核查".format(vertexPath.split("/")[-1],
                                                                                            attrKeyItem))
            uuidFunDict={"type":"string"} if nodeSysIDUUID else {}
            vertexItemJson={
                        "path": "{}/{}".format(serverPath,vertexFileName),
                        "failDataPath": "{}/tmp/err/{}Fail.csv".format(serverPath,vertexFileName.split(".")[0]),
                        "batchSize": 10,
                        "type": "csv",
                        "csv": {
                            "withHeader": False,
                            "withLabel": False
                        },
                        "schema": {
                            "type": "vertex",
                            "vertex": {
                                "vid": {**{
                                    "index": list(vertexDf.columns).index(idCol)
                                },**uuidFunDict},
                                "tags": [
                                    {
                                        "name": nodeType,
                                        "props": attrTypeList
                                    }
                                ]
                            }
                        }
                    }
            vertexJsonList.append(vertexItemJson)
    return vertexJsonList
    
def buildEdge(edgeJson,graphClient,srcSysIDUUID=True,tgtSysIDUUID=True,serverPath="/usr/local/nebula-graph-studio/nebula-graph-studio/tmp/upload"):

    edgeJsonList=[]
    for edgeInfoItem in edgeJson:
        edgePath=edgeInfoItem["file_path"]
        edgeFileName=edgeInfoItem["file_name"].split(".")[0]+"_copy.csv"
        edgeType=edgeInfoItem["edge_type"]
        srcId=edgeInfoItem["src_id"]
        tgtId=edgeInfoItem["tgt_id"]
        csv2plato_attr_map=edgeInfoItem["csv2plato_attr_map"]
        csv_attr2type_map=edgeInfoItem["attr_type_map"]
        edgeDf=pd.read_csv(edgePath)
        
        gEdgeAttrDf=wrapNebula2Df(graphClient.execute("DESCRIBE EDGE {}".format(edgeType)))
        
        attrTypeList=[]
        if gEdgeAttrDf.shape[0]>0:
            gEdgeAttrList=gEdgeAttrDf["Field"].values.flatten().tolist()
            for attrKeyItem in csv_attr2type_map:
                if attrKeyItem in  csv2plato_attr_map and csv2plato_attr_map[attrKeyItem] in gEdgeAttrList:
                    if pdPlatoTypeSame(edgeDf[attrKeyItem],csv_attr2type_map[attrKeyItem]):
                        attrTypeList.append({
                                "name": csv2plato_attr_map[attrKeyItem],
                                "type": csv_attr2type_map[attrKeyItem],
                                "index": list(edgeDf.columns).index(attrKeyItem)
                            })
                    else:
                        raise TypeError("csv({}_{})与uploadSchema.json类型冲突，请核查".format(edgePath.split("/")[-1],
                                                                                                attrKeyItem))

        srcVIDDict={"type": "string"} if srcSysIDUUID else {}
        tgtVIDDict={"type": "string"} if tgtSysIDUUID else {}
        edgeItemJson={
                        "path": "{}/{}".format(serverPath,edgeFileName),
                        "failDataPath": "{}tmp/err/{}Fail.csv".format(serverPath,edgeFileName.split(".")[0]),
                        "batchSize": 10,
                        "type": "csv",
                        "csv": {
                            "withHeader": False,
                            "withLabel": False
                        },
                        "schema": {
                            "type": "edge",
                            "edge": {
                                "name": edgeType,
                                "srcVID": {**{
                                    "index": list(edgeDf.columns).index(srcId)
                                },**srcVIDDict},
                                "dstVID": {**{
                                    "index": list(edgeDf.columns).index(tgtId)
                                },**tgtVIDDict},
                                "withRanking": False,
                                "props": attrTypeList
                            }
                        }
                    }
        edgeJsonList.append(edgeItemJson)
    return edgeJsonList

attrTypeNullDict={
    "string":"'null'",
    "int":0,
    "double":0.0
}
def createSchemaFromSchemaJson(schemaJson,graphClient):
    '''
    根据schemaJson构建图数据库/节点-边schema/节点index
    '''
    gDbName=schemaJson["gDbName"]
    graphClient.execute("CREATE SPACE IF NOT EXISTS {}".format(gDbName)) # 构建图数据库
    graphClient.execute("USE {}".format(gDbName))
    createTagErrCode=0
    createTagIndexErrCode=0
    rebuildTagIndexErrCode=0
    createEdgeErrCode=0
    schemaJson["vertex"]=schemaJson.get("vertex",[])+[{"node_type":"Alias","old_id_col":"Name","attr_type_map":{"Name":"string"}}]
    if "vertex" in schemaJson: # 构建节点schema
        schemaTagList=schemaJson["vertex"]
        for schemaTagItem in schemaTagList:
            nodeType=schemaTagItem["node_type"]
            nodeIdAttr=schemaTagItem["old_id_col"]
            schemaTagItem["attr_type_map"]={**schemaTagItem["attr_type_map"],**{"sourceName":"string"}}
            nodeAttrStr=",".join([" ".join([attrKey,schemaTagItem["attr_type_map"][attrKey]])+" DEFAULT {}".format(attrTypeNullDict[schemaTagItem["attr_type_map"][attrKey]]) 
                                    for attrKey in schemaTagItem["attr_type_map"]])
            
            createTagStr="CREATE TAG IF NOT EXISTS {}({})".format(nodeType,nodeAttrStr)
            createTagReq=graphClient.execute(createTagStr)
            createTagErrCode=createTagReq.error_code

            createTagIndexStr="CREATE TAG INDEX IF NOT EXISTS {nodeTypeLower}_{nodeTypeLower}{nodeIdAttrLower}_index ON {nodeType}({nodeIdAttr})".format(
                nodeTypeLower=nodeType.lower(),
                nodeIdAttrLower=nodeIdAttr.lower(),
                nodeType=nodeType,
                nodeIdAttr=nodeIdAttr
            )
            createTagIndexReq=graphClient.execute(createTagIndexStr)
            createTagIndexErrCode=createTagIndexReq.error_code
            
            rebuildTagIndexStr="REBUILD TAG INDEX {nodeTypeLower}_{nodeTypeLower}{nodeIdAttrLower}_index OFFLINE".format(
                nodeTypeLower=nodeType.lower(),
                nodeIdAttrLower=nodeIdAttr.lower(),
                nodeType=nodeType,
                nodeIdAttr=nodeIdAttr
            )
            rebuildTagIndexReq=graphClient.execute(rebuildTagIndexStr)
            rebuildTagIndexErrCode=rebuildTagIndexReq.error_code
    schemaJson["vertex"].pop(-1)
    
    schemaJson["edge"]=schemaJson.get("edge",[])+[{"edge_type":"aliasNameOf","attr_type_map":{}}]
    if "edge" in schemaJson: # 构建关系schema
        schemaEdgeList=schemaJson["edge"]
        for schemaEdgeItem in schemaEdgeList:
            edgeType=schemaEdgeItem["edge_type"]
            schemaEdgeItem["attr_type_map"]={**schemaEdgeItem.get("attr_type_map",{}),**{"sourceName":"string"}}
            edgeAttrStr=",".join([" ".join([attrKey,schemaEdgeItem.get("attr_type_map",{})[attrKey]])+" DEFAULT {}".format(attrTypeNullDict[schemaEdgeItem["attr_type_map"][attrKey]]) 
                                    for attrKey in schemaEdgeItem["attr_type_map"]])

            createEdgeStr="CREATE EDGE IF NOT EXISTS {}({})".format(edgeType,edgeAttrStr)
            createEdgeReq=graphClient.execute(createEdgeStr)
            createEdgeErrCode=createEdgeReq.error_code
            
    schemaJson["edge"].pop(-1)

    return createTagErrCode,createTagIndexErrCode,rebuildTagIndexErrCode,createEdgeErrCode
            

def submitSchema(schemaJson,gUrl="http://9.135.95.249:7001",cookie=""):

    schemaJson["mountPath"]="/upload-dir"
    url = gUrl+"/api/import/config"

    data = json.dumps(schemaJson)
    headers = {
        'Proxy-Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62',
        'Content-Type': 'application/json',
        'Origin': gUrl,
        'Referer': '{}/import'.format(gUrl),
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': cookie
    }

    response = requests.request("POST", url, headers=headers, data=data)

    print(response.text)
    url = gUrl+"/api-import/submit"

    data = json.dumps(schemaJson)
    headers = {
        'Proxy-Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62',
        'Content-Type': 'application/json',
        'Origin': gUrl,
        'Referer': '{}/import'.format(gUrl),
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': cookie
    }

    response = requests.request("POST", url, headers=headers, data=data)

    print(response.text)
    return response.json()["taskId"]


if __name__=="__main__":
    
    # test
    ghost="9.135.95.249"
    gport=13708
    guser="root"
    gpassword="nebula"
    gspace="post_skill_school_ianxu"
    gUrl="http://9.135.95.249:7001"

    schemaPath="csv2platodb/attr2Vertex_1629250000"
    
    # product
    # ghost="10.99.218.40"
    # gport=8080
    # guser="root"
    # gpassword="nebula"
    # gspace="testImport"
    # gUrl="http://10.99.218.40:8081"
    
    '''
    uploadSchema形状：
    {
        "vertex":[
            {
                "file_path": "xxx" (node),
                "file_name": "xxx.csv" (node file),
                "node_type": "NodeType",
                "id_col": "nodeID_col",
                "csv2plato_attr_map":{
                    "csvAttr":"graphAttr"
                },
                "attr_type_map": {
                    "csvAttr":"graphAttrType" (double/int/string only)
                }
            },
            ......
        ],
        "edge":[
            {
                "file_path": "xxx" (edge),
                "file_name": "xxx.csv" (edge file),
                "edge_type": "edgeType",
                "src_id": "src_node_ID_col",
                "tgt_id": "tgt_node_ID_col",
                "csv2plato_attr_map": {
                    "csvAttr":"graphAttr"
                },
                "attr_type_map": {
                    "csvAttr":"graphAttrType" (double/int/string only)
                }
            },
            ......
        ]
    }
    '''
    with open(os.path.join(schemaPath,"uploadSchema.json")) as uploadSchemaFile:
        uploadSchemaJson=json.load(uploadSchemaFile)
    
    gConnection_pool = ConnectionPool(ghost, gport,network_timeout=300000)
    gClient = GraphClient(gConnection_pool)
    gClient.authenticate(guser, gpassword)
    gClient.execute("USE {}".format(gspace))
    
    vertexJsonList=[]
    edgeJsonList=[]
    if "vertex" in uploadSchemaJson:
        vertexJsonList=buildVertex(uploadSchemaJson["vertex"],graphClient=gClient)
    if "edge" in uploadSchemaJson:
        edgeJsonList=buildEdge(uploadSchemaJson["edge"],graphClient=gClient)
    
    schemaJson={
        "version": "v2",
        "description": "web console import",
        "clientSettings": {
            "concurrency": 10,
            "channelBufferSize": 128,
            "space": gspace,
            "connection": {
                "user": guser,
                "password": gpassword,
                "address": "{}:{}".format(ghost,gport)
            }
        },
        "logPath": "/upload-dir/tmp/import.log",
        "files": vertexJsonList+edgeJsonList
    }
    with open(os.path.join(schemaPath,"schemaJson.json"),"w+") as schemaJsonFile:
        json.dump(schemaJson,schemaJsonFile)
        
    resDict=submitSchema(schemaJson,gUrl=gUrl)
    
    print(resDict)