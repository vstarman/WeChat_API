#  -*- coding:utf-8 -*-

from flask import Flask,request,make_response
import hashlib

app = Flask(__name__)


@app.route('/wechat')
def wechat():
    # 设置token
    token = 'Samuel'
    # 获取参数
    data = request.args
    signature = data.get('signature')
    timestamp = data.get('timestamp')
    nonce = data.get('nonce')
    echostr = data.get('echostr')

    # 对参数进行字典排序，拼接字符串
    temp = [timestamp, nonce, token]
    temp.sort()
    temp = ''.join(temp)
    # 加密
    if hashlib.sha1(temp).hexdigest() == signature:
        return make_response(echostr)
    else:
        return 'error', 403

if __name__ == '__main__':
    app.run(port=8000)
