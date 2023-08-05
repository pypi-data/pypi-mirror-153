
def getEntityFromTags(mySentList,myTagList):
    '''
    从tagList中获取sentList中的实体
    '''
    entityList=[]
    tmpEntity=""
    for tagI,_ in enumerate(myTagList):
        if tagI>=len(mySentList):
            break
        if myTagList[tagI]=="B":
            if len(mySentList[tagI])>1:
                tmpEntity=mySentList[tagI]+" "
            else:
                tmpEntity=mySentList[tagI]
        elif myTagList[tagI]=="I":
            if len(mySentList[tagI])>1:
                tmpEntity+=" "+mySentList[tagI]
            else:
                tmpEntity+=mySentList[tagI]
        else:
            if len(tmpEntity)>0:
                entityList.append(tmpEntity)
            tmpEntity=""
    return entityList

def getEntityFromTags(mySentList,myTagList):
    '''
    从tagList中获取sentList中的实体
    '''
    entityList=[]
    tmpEntity=""
    if len(mySentList)==len(myTagList):
        for tagI,_ in enumerate(myTagList):
            if myTagList[tagI]=="B":
                tmpEntity=mySentList[tagI]
            elif myTagList[tagI]=="I":
                tmpEntity+=mySentList[tagI]
            else:
                if len(tmpEntity)>0:
                    entityList.append(tmpEntity)
                tmpEntity=""
    return entityList

if __name__=="__main__":
    
    mySentList=['marketingapi', '接', '入', '规', '范', '和', '实', '操', '指', '南', 'pdf', 'knowhow', 'ams', 'marketingapi', '作', '为', '腾', '讯', '广', '告', '统', '一', '的', '对', '外', 'api', '主', '要', '负', '责', '各', '类', '子', '系', '统', '对', '外', 'api', '能', '力', '的', '封', '装', '提', '供', '统', '一', '的', '广', '告', '投', '放', 'api', '能', '力', '本', '课', '程', '主', '要', '分', '享', '接', '入', 'marketingapi', '模', '块', '时', '需', '要', '了', '解', '注', '意', '的', '各', '项', '规', '范', '对', '接', '流', '程', '从', '开', '发', '到', '测', '试', '到', '发', '布', '提', '供', '实', '际', '接', '入', '例', '子', '方', '便', '后', '续', '各', '类', '子', '系', '统', '对', '接']
    myTagList=['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B', 'I', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B', 'I', 'B', 'I', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
    print(getEntityFromTags(mySentList,myTagList))