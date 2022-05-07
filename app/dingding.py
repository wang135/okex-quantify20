import requests,json
#https://oapi.dingtalk.com/robot/send?access_token=8f9be933d1d701fcd7556dd318d3e34cf10f1f4c510b744dd98d90b5fe987602
# windows
from app.authorization import dingding_token

# linux
# from app.authorization import dingding_token

class Message:





    def dingding_warn(self,text):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        api_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % dingding_token
        json_text = self._msg(text)
        requests.post(api_url, json.dumps(json_text), headers=headers).content

    def _msg(self,text):
        json_text = {
            "msgtype": "text",
            "at": {
                "atMobiles": [
                    "11111"
                ],
                "isAtAll": False
            },
            "text": {
                "content": "赢顺势交易"+text
            }
        }
        return json_text

if __name__ == "__main__":
    msg = Message()
    print(msg.dingding_warn("EOSUSDT"))