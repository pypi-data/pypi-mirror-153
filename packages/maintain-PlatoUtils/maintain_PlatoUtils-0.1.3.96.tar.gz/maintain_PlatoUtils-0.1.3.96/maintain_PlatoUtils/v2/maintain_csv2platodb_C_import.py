import requests
import json


def importData(gUrl,taskId="12",cookie=""):

    url = "{}/api/import/log?dir=%2Fupload-dir&startByte=0&endByte=1000000&taskId={}".format(gUrl,taskId)

    payload={}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.1.232416773.1651137071; _gid=GA1.1.1694003004.1651137071; locale=ZH_CN; nsid=ce5e85f8f404cd565ec5269f69f1770a; Secure=true; SameSite=None; nh=124.221.69.218:9669; nu=root; np=nebula; _gat_gtag_UA_60523578_13=1',
        'Referer': '{}/import'.format(gUrl),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    print(response.text)

    for i in range(3):
        url = "{}/api/import/log?dir=%2Fupload-dir&startByte=742&endByte=1000742&taskId={}".format(gUrl,taskId)

        payload={}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Cookie': '_ga=GA1.1.232416773.1651137071; _gid=GA1.1.1694003004.1651137071; locale=ZH_CN; nsid=ce5e85f8f404cd565ec5269f69f1770a; Secure=true; SameSite=None; nh=124.221.69.218:9669; nu=root; np=nebula; _gat_gtag_UA_60523578_13=1',
            'Referer': '{}/import'.format(gUrl),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

    return response.json()


if __name__=="__main__":
    
    # test
    ghost="9.135.95.249"
    gport=13708
    guser="root"
    gpassword="nebula"
    gspace="post_skill_school_ianxu"
    gUrl="http://9.135.95.249:7001"

    taskId="12"

    importData(gUrl,taskId=taskId)