# -*- coding:utf-8 -*-
from flask import Flask, request, make_response
import hashlib

app = Flask(__name__)


<<<<<<< HEAD
@app.route('/wechat')
=======
@app.route('/')
def index():
    return 'index'


@app.route('/wechat8000')
>>>>>>> 47044ce41ed24957f6a32594bb4f1cad070b12b8
def index():
    # 设置token
    token = 'Samuel'
    # 获取参数
    data = request.args
    print data
    signature = data.get('signature')
    timestamp = data.get('timestamp')
    nonce = data.get('nonce')
    echostr = data.get('echostr')
    # 将token、timestamp、nonce三个参数进行字典序排序
    temp = [timestamp, nonce, token].sort()
    temp = temp.sort()
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
