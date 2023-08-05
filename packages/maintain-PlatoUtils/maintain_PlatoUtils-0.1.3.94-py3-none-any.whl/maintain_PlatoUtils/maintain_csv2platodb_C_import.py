import requests
import json


def importData(gUrl,taskId="12",cookie=""):

    url="{}/api/import/import".format(gUrl)

    payload = json.dumps({
        "taskId": taskId
    })
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

    response = requests.request("POST", url, headers=headers, data=payload)
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