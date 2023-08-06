import flashtext
import tqdm
import pandas as pd
from nebula.graph import ttypes,GraphService
from nebula.ConnectionPool import ConnectionPool
from nebula.Client import GraphClient
from maintain_PlatoUtils.maintain_PlatoUtils import wrapNebula2Df
from maintain_PlatoUtils.text_utils.preprocessor import fuzzyText,simpleCutWords,simpleRecoverText
from elasticsearch import Elasticsearch
import json
def asynFunc(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        threadItem=threading.Thread(target=func,args=args,kwargs=kwargs)
        threadItem.start()
        return "0"
    try:
        return wrapper
    except Exception as ex:
        print(ex)
        return str(ex)

class SimpleRelationRecognizer(flashtext.KeywordProcessor):
    
    def __init__(self,gHost, gPort,gUser,gPassword,gDBName,esClient=None,esIndex="hr_integrate_index",*args,**kwargs):
        super(SimpleRelationRecognizer, self).__init__()
        connection_pool = ConnectionPool(gHost, gPort,network_timeout=60000)
        self.gClient = GraphClient(connection_pool)
        self.gClient.authenticate(gUser,gPassword)
        self.gClient.execute_query("USE {}".format(gDBName))
        edgeTypeDf=wrapNebula2Df(self.gClient.execute_query("SHOW EDGES"))
        self.edgeTypeList=edgeTypeDf["Name"].values.tolist()
        self.entityAttrDict={}
        self.buildEntityKWProcessor()
        self.esClient=esClient
        self.esIndex=esIndex
        
    def buildEntityKWProcessor(self):
        
        tagDf=wrapNebula2Df(self.gClient.execute_query("SHOW TAGS"))
        tagList=tagDf["Name"].values.flatten().tolist()
        
        indexDf=wrapNebula2Df(self.gClient.execute_query("SHOW TAG INDEXES"))
        indexList=indexDf["Index Name"].values.flatten().tolist()
        
        for indexItem in tqdm.tqdm(indexList,desc="loading entities"):
            nodeType=indexItem.split("_")[0]
            indexInfoDf=wrapNebula2Df(self.gClient.execute_query("DESCRIBE TAG INDEX {}".format(indexItem)))
            indexAttrName=indexInfoDf["Field"].values.flatten().tolist()[0]
            nodeInfoDf=wrapNebula2Df(self.gClient.execute_query("LOOKUP ON {nodeType} WHERE {nodeType}.{indexAttrName}!='不可能的名字' \
                                                                    YIELD {nodeType}.{indexAttrName} AS {nodeType}{indexAttrName}".format(nodeType=nodeType,
                                                                                                                                            indexAttrName=indexAttrName)))
            dfIndexAttrName="{}{}".format(nodeType,indexAttrName)
            
            oriAliasDict={}
            aliasQueryStrList=[]
            if nodeInfoDf.shape[0]>0:
                enitityNameList=nodeInfoDf[dfIndexAttrName].values.flatten().tolist()
                for entityNameItem in tqdm.tqdm(enitityNameList,desc="entity {}".format(nodeType)):
                    aliasQueryStrItem="LOOKUP ON {nodeType} WHERE {nodeType}.{indexAttrName}=='{nodeIdVal}'|\
                                                                            GO FROM $-.VertexID OVER alias BIDIRECT \
                                                                                $^.{nodeType}.{indexAttrName} AS oriName,\
                                                                                $$.Alias.Name AS aliasName".format(
                                                                                nodeType=nodeType,
                                                                                indexAttrName=indexAttrName,
                                                                                nodeIdVal=entityNameItem
                                                                            )
                    aliasQueryStrList.append(aliasQueryStrItem)
                    self.entityAttrDict[entityNameItem]=self.entityAttrDict.get(entityNameItem,[])+[(entityNameItem,nodeType,indexAttrName)]
                    oriAliasDict[entityNameItem]=[entityNameItem]
                    if len(aliasQueryStrList)>=256:
                        aliasQueryStr=" UNION ".join(aliasQueryStrList)
                        oriAliasDf=wrapNebula2Df(self.gClient.execute_query(aliasQueryStr))
                        if oriAliasDf.shape[0]>0:
                            oriList=oriAliasDf["oriName"].drop_duplicates().values.flatten().tolist()
                            for oriNameItem in oriList:
                                candidateAliasWordList=[]
                                if self.esClient is not None:
                                    candidateAliasWord=simpleRecoverText(fuzzyText(simpleCutWords(oriNameItem),lostP=0.5,changeP=0.5,exchangeP=0.3,esClient=self.esClient))
                                    if candidateAliasWord not in candidateAliasWordList:
                                        candidateAliasWordList.append(candidateAliasWord)
                                aliasList=oriAliasDf.loc[oriAliasDf["oriName"]==oriNameItem,"aliasName"].values.flatten().tolist()
                                oriAliasDict[oriNameItem]+=aliasList+candidateAliasWordList
                        self.add_keywords_from_dict(oriAliasDict)
                        aliasQueryStrList=[]
                        oriAliasDict={}
                if len(aliasQueryStrList)>0:
                    aliasQueryStr=" UNION ".join(aliasQueryStrList)
                    oriAliasDf=wrapNebula2Df(self.gClient.execute_query(aliasQueryStr))
                    if oriAliasDf.shape[0]>0:
                        oriList=oriAliasDf["oriName"].drop_duplicates().values.flatten().tolist()
                        for oriNameItem in oriList:
                            aliasList=oriAliasDf.loc[oriAliasDf["oriName"]==oriNameItem,"aliasName"].values.flatten().tolist()
                            oriAliasDict[oriNameItem]+=aliasList
                    self.add_keywords_from_dict(oriAliasDict)
                    aliasQueryStrList=[]
                    oriAliasDict={}
                
    def relationRecognize(self,text,windowSize=256):
        '''简单关系识别'''
        for windowI in range(0,len(text),windowSize):
            entityList=self.extract_keywords(text[windowI:windowI+windowSize])
            relDfList=[]
            for edgeTypeItem in self.edgeTypeList:
                queryStrList=[]
                for entity1I in range(len(entityList)):
                    entity1AttrGroup=self.entityAttrDict[entityList[entity1I]]
                    for entity1AttrI in range(len(entity1AttrGroup)):
                        for entity2I in range(len(entityList)):
                            entity2AttrGroup=self.entityAttrDict[entityList[entity2I]]
                            for entity2AttrI in range(len(entity2AttrGroup)):
                                
                                entity1=entityList[entity1I]
                                headIdVal=self.entityAttrDict[entity1][entity1AttrI][0]
                                headType=self.entityAttrDict[entity1][entity1AttrI][1]
                                headIdAttrName=self.entityAttrDict[entity1][entity1AttrI][2]
                                
                                entity2=entityList[entity2I]
                                tailIdVal=self.entityAttrDict[entity2][entity2AttrI][0]
                                tailType=self.entityAttrDict[entity2][entity2AttrI][1]
                                tailIdAttrName=self.entityAttrDict[entity2][entity2AttrI][2]
                                
                                queryStrItem="LOOKUP ON {headType} WHERE {headType}.{headIdAttrName}=='{headIdVal}'|\
                                                GO FROM $-.VertexID OVER {edgeType} \
                                                    WHERE $$.{tailType}.{tailIdAttrName}=='{tailIdVal}'\
                                                        YIELD $^.{headType}.{headIdAttrName} AS headIdVal,\
                                                            $$.{tailType}.{tailIdAttrName} AS tailIdVal,\
                                                                '{edgeType}' AS edgeType".format(
                                                                                                headType=headType,
                                                                                                headIdAttrName=headIdAttrName,
                                                                                                headIdVal=headIdVal,
                                                                                                edgeType=edgeTypeItem,
                                                                                                tailType=tailType,
                                                                                                tailIdAttrName=tailIdAttrName,
                                                                                                tailIdVal=tailIdVal
                                                                                            )
                                queryStrList.append(queryStrItem)
                                if len(queryStrList)>64:
                                    queryStr=" UNION ".join(queryStrList)
                                    queryDfItem=wrapNebula2Df(self.gClient.execute_query(queryStr))
                                    if queryDfItem.shape[0]>0:
                                        relDfList.append(queryDfItem)
                                    queryStrList=[]

            if len(queryStrList)>0:
                queryStr=" UNION ".join(queryStrList)
                queryDfItem=wrapNebula2Df(self.gClient.execute_query(queryStr))
                if queryDfItem.shape[0]>0:
                    relDfList.append(queryDfItem)
                
        returnRelJson=[]
        if len(relDfList)>0:
            relDf=pd.concat(relDfList)
            returnRelJson=json.loads(relDf.to_json(orient="records"))
        return entityList,returnRelJson
    
if __name__=="__main__":
    
    gHost="9.135.95.249"
    gPort=13708
    gUser="root"
    gPassword="nebula"
    gDBName="post_skill_school_ianxu"
    
    esClient=Elasticsearch(["9.134.92.196:9200"],http_auth=("elastic", "devcloud@123"))

    mySimpleRelationRecognizer=SimpleRelationRecognizer(gHost,gPort,gUser,gPassword,gDBName,esClient=esClient,esIndex="hr_integrate_index")
    kwList,returnRelJson=mySimpleRelationRecognizer.relationRecognize("开发和测试大型开放世界游戏是一项艰巨的任务。为了应对这一挑>战的规模，育碧Reflections一直在《全境封锁》项目过程中开发“客户端机器人”(Client Bots)，这是一种控制玩家、模仿人类输入，同时报告问题(如任务无法完成、性能统计等)的AI。该技术的应用包括自动任务播放和报告生成、跟踪机器人(帮助QC和关卡设计师独自测试多人任务)、街道漫游(收集性能数据)、任何定制测试的通用平台以及辅助bug复制的工具。本部分将介绍系统背后的动机，并引用育碧Reflections团队的许多案例来深入了解其客户端机器人的内部架构、团队所面临的挑战，以及如何构建支持此类技术内容的最佳实践展示。")
    print(kwList,returnRelJson)
    
    print(123)