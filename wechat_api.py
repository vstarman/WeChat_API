# -*- coding:utf-8 -*-
from flask import Flask, request, make_response
import hashlib
import xmltodict
import time
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

    # print signature,timestamp,nonce,echostr
    # 将token、timestamp、nonce三个参数进行字典序排序
    temp = [timestamp, nonce, token]
    temp.sort()
    # 将三个参数字符串拼接成一个字符串进行sha1加密
    temp = "".join(temp)
    sig = hashlib.sha1(temp).hexdigest()
    # 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    if signature == sig:
        if request.method == 'GET':
            return echostr
        # todo: 否则为post请求
        """
        <xml>
         <ToUserName><![CDATA[toUser]]></ToUserName>
         <FromUserName><![CDATA[fromUser]]></FromUserName>
         <CreateTime>1348831860</CreateTime>
         <MsgType><![CDATA[text]]></MsgType>
         <Content><![CDATA[this is a test]]></Content>
         <MsgId>1234567890123456</MsgId>
         </xml>
        """
        # 获取文本字典信息
        xml_data = request.data
        xml_dict = xmltodict.parse(xml_data)['xml']
        msg_type = xml_dict['MsgType']
        if 'text' == msg_type:
            # 接收文本消息
            response_dic = {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": xml_dict.get("Content"),
            }
            print '--' * 50
            print 'Text Content:', xml_dict.get('Content')
        elif 'voice' == msg_type:
            # 接收语音消息
            response_dic = {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                # 微信自带语音识别
                "Content": xml_dict.get("Recognition"),
            }
            print '--' * 50
            print 'Voice Content:', xml_dict.get('Recognition')
        else:
            response_dic = {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": '文件格式不对,你丫欠揍吧~',
            }
        if response_dic:
            response_dic = {'xml': response_dic}
            return xmltodict.unparse(response_dic)
        else:
            return ''
    else:
        return 'error', 403

if __name__ == '__main__':
    app.run(port=8002, debug=True)
