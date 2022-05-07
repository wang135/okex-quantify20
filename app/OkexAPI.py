from app.authorization import recv_window,api_secret,api_key



import json


import datetime
import requests
import hmac
import base64
try:
    from urllib import urlencode
# python3
except ImportError:
    from urllib.parse import urlencode
CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'

APPLICATION_JSON = 'application/json'
class Okex(object):
    #BASE_URL = "https://www.binance.com/api/v1"
    # BASE_URL_V3 = "https://api.binance.com/api/v3"
    # PUBLIC_URL = "https://www.binance.com/exchange/public/product"

    def __init__(self, api_key, secret_key,passphrase):
        self.api_key = api_key
        self.secret_key =secret_key
        self.passphrase = passphrase

    def get_timestamp(self):
        now = datetime.datetime.utcnow()
        t = now.isoformat("T", "milliseconds")
        return t + "Z"

    def pre_hash(self,timestamp, method, request_path, body):
        return str(timestamp) + str.upper(method) + request_path + body

    def sign(self,message, secretKey):
        mac = hmac.new(bytes(secretKey, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)

    def get_header(self,api_key, sign, timestamp, passphrase):
        header = dict()
        header[CONTENT_TYPE] = APPLICATION_JSON
        header[OK_ACCESS_KEY] = api_key
        header[OK_ACCESS_SIGN] = sign
        header[OK_ACCESS_TIMESTAMP] = str(timestamp)
        header[OK_ACCESS_PASSPHRASE] = passphrase
        return header


    # 需要授权才能操作
    def login(self,request_path):
        url = 'https://www.okex.com' + request_path

        timestamp = self.get_timestamp()  # 获取时间戳
        method = 'GET'
        body = ''
        my_sign = self.sign(self.pre_hash(timestamp, method, request_path, str(body)), self.secret_key)  # 签名
        header = self.get_header(self.api_key, my_sign, timestamp, self.passphrase)  # 设置请求头
        response = requests.get(url, headers=header,timeout=10)
        return response.json()
##公共数据
    def publie(self,request_path,data):
        url = 'https://www.okex.com' + request_path
        response2 = requests.get(url, params=data,timeout=10)
        return response2.json()

    ##交易的数据
    def zhengqiam(self,request_path,params):
        url = 'https://www.okex.com' + request_path
        body = json.dumps(params)
        timestamp = self.get_timestamp()  # 获取时间戳
        method = 'POST'
        my_sign = self.sign(self.pre_hash(timestamp, method, request_path, str(body)), self.secret_key)  # 签名
        header = self.get_header(self.api_key, my_sign, timestamp, self.passphrase)  # 设置请求头
        response = requests.post(url, headers=header,data=body, timeout=10)
        return response.json()