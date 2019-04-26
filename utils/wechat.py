# _*_coding:utf-8_*_
import time
import pickle
import datetime
import json
import requests
from config import APP_ENV

class WeChat(object):
    CORPID = APP_ENV.CORPID
    CORPSECRET = APP_ENV.CORPSECRET
    BASEURL = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}'.format(CORPID, CORPSECRET)
    URL = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s"

    @classmethod
    def get_token(cls):
        token_file = 'token'
        try:
            with open(token_file, 'rb') as f:
                data_dict = pickle.load(f)
        except:
            data_dict = {}

        try:
            expires_time = data_dict['expires_time']
        except:
            expires_time = 0

        now_time = int(time.mktime(datetime.datetime.now().timetuple()))
        if now_time >= expires_time:
            result = requests.get(cls.BASEURL).json()
            expires_time = now_time + 7000
            result['expires_time'] = expires_time
            result['expires_in'] = expires_time - now_time
            with open(token_file, 'wb') as f:
                pickle.dump(result, f)
            access_token = result['access_token']
            expires_in = {"expires_in":result['expires_in']}
        else:
            result = data_dict
            expires_time = data_dict['expires_time']
            result['expires_in'] = expires_time - now_time
            with open(token_file, 'wb') as f:
                pickle.dump(result, f)
            access_token = data_dict['access_token']
            expires_in = {"expires_in":result['expires_in']}
        return access_token,expires_in

    @classmethod
    def handler(cls,cont):
        content = ""
        c = dict()
        title = cont['title']
        ruleurl = cont['ruleUrl']
        if cont['state'] == 'ok':
            content = "已恢复正常"
        elif not cont['evalMatches']:
            content = "监控项异常"
        else:
            i = 1
            for item in cont['evalMatches']:
                value = item["value"]
                if item["tags"]:
                    instance = item["tags"]["instance"]
                else:
                    instance = "instance%s" % i
                c['%s-%s' % (i,instance)] = value
                i+=1
            for k,v in c.items():
                content += "%s:%s,\n" % (k,v)
        return title,ruleurl,content

    @classmethod
    def send_card(cls,cont,**kwargs):
        team_token,expires_in = cls.get_token()
        url = cls.URL % (team_token)
        title,ruleurl,content = cls.handler(cont)
        wechat_json = {
            "touser": APP_ENV.TOUSER,
            "toparty": kwargs.get('toparty') or APP_ENV.TOPARTY,
            "totag": APP_ENV.TOTAG,
            "msgtype": "textcard",
            "agentid": APP_ENV.AGENTID,
            "textcard": {
                "title": title,
                "description": content,
                "url": ruleurl,
                "btntxt": "更多"
                }
        }
        response = requests.post(url, data=json.dumps(wechat_json))
        return response,team_token,expires_in


# 测试数据
testdata={
    "ruleName": "webhooktest",
    "state": "alerting",
    "message": "This is my webhook send test ,my target is to get the alert data.",
    "ruleId": 4,
    "title": "[Alerting] webhooktest",
    "ruleUrl": "http://localhost:3000/dashboard/db/webhookdatatest?fullscreen&edit&tab=alert&panelId=1&orgId=1",
    "evalMatches": [
        {
            "metric": "mytest.age { myName: pangkun2 }",
            "value": 27,
            "tags": {"instance":"tomcat"}
        },
        {
            "metric": "mytest.age { myName: pangkun3 }",
            "value": 26,
            "tags": {"instance":"nginx"}
        }
    ]
}