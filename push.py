import requests, json, os, re

def config():
    path = os.getcwd()
    if path == '/opt/function':
        path = 'code/'
    else:
        path = ''
    with open(path + 'config.json', encoding='utf-8') as f:
        account = f.read()
    a = account.count('/*')
    for i in range(a):
        x = account.find('/*')
        y = account.find('*/') + 2
        account = account[:x] + account[y:]
    account = re.sub(' ', '', account)
    account = re.sub('\n', '', account)
    account = json.loads(account)
    return account

def WeCom(content):
    wx = config()["push"]["WeCom"]
    if not eval(os.environ.get("WE_COM_PUSH", wx["push"])):
        print('企业微信不推送')
    else:
        # 获取企业微信推送所需的配置信息
        corpid = wx.get("corpid", "")
        secret = wx.get("secret", "")
        agentid = wx.get("agentid", "")
        if corpid and secret and agentid:
            url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + secret
            access_token = requests.get(url)
            access_token = json.loads(access_token.text)
            access_token = access_token.get("access_token")
            # 推送逻辑...
            # 这里根据access_token等信息执行企业微信推送

def Ding(content):
    ding = config()["push"]["Ding"]
    if not eval(os.environ.get("DING_PUSH", ding["push"])):
        print('钉钉不推送')
    else:
        # 获取钉钉推送所需的配置信息
        appkey = ding.get("appkey", "")
        appsecret = ding.get("appsecret", "")
        if appkey and appsecret:
            access_token = requests.get('https://oapi.dingtalk.com/gettoken?appkey=' + appkey + '&appsecret=' + appsecret)
            access_token = access_token.text
            access_token = json.loads(access_token)
            access_token = access_token["access_token"]
            # 推送逻辑...
            # 这里根据access_token等信息执行钉钉推送


def pushplus(content):
    pushplus = config()["push"]["pushplus"]
    if not eval(os.environ.get("PUSHPLUS_PUSH", pushplus["push"])):
        print('pushplus不推送')
    else:
        # 获取pushplus推送所需的配置信息
        token = pushplus.get("token", "")
        if token:
            url = "http://www.pushplus.plus/send"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "token": token,
                "title": '腾讯视频签到',
                "content": content
            }
            try:
                requests.post(url, headers=headers, data=json.dumps(data))
            except:
                print('推送失败')

def main(content):
    print(content)
    WeCom(content)
    Ding(content)
    pushplus(content)

if __name__ == '__main__':
    main()
