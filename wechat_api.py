# -*- coding:utf-8 -*-
from flask import Flask, request, make_response
import hashlib

app = Flask(__name__)


@app.route('/wechat', methods=['post', 'get'])
def index():
    # 设置token
    token = 'Samuel'
    # 获取参数
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    echostr = request.args.get("echostr")
    print '--'*50
    print signature,timestamp,nonce,echostr
    # 将token、timestamp、nonce三个参数进行字典序排序
    temp = [timestamp, nonce, token]
    temp.sort()
    # 将三个参数字符串拼接成一个字符串进行sha1加密
    temp = "".join(temp)
    sig = hashlib.sha1(temp).hexdigest()
    # 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    if signature == sig:
        return make_response(echostr)
    else:
        return 'error', 403

if __name__ == '__main__':
    app.run(port=8002, debug=True)
