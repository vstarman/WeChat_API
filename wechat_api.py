# -*- coding:utf-8 -*-
from flask import Flask, request
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

    print signature,timestamp,nonce,echostr
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
        # 否则为post请求
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
        print '---------------> : %s' % msg_type
	print xml_dict
        if 'text' == msg_type:
            # 接收文本消息
            response_dict = {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": xml_dict.get("Content"),
            }
            print 'text' + '--' * 50
            print 'Text Content:', xml_dict.get('Content')
        elif 'voice' == msg_type:
            # 接收语音消息
            response_dict = {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": xml_dict.get("Recognition"),
            }
            print 'voice' + '--' * 50
            print 'Voice Content:', xml_dict.get('Recognition')
        elif 'event' == msg_type:
            # 代表当前有用户订阅了
            if 'subscribe' == xml_dict.get('Event'):
                response_dict = {
                    "ToUserName": xml_dict.get("FromUserName"),
                    "FromUserName": xml_dict.get("ToUserName"),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": "感谢你丫的关注,送你一杯卡布奇诺...",
                }
                if xml_dict.get("EventKey"):
                    response_dict["Content"] += "；场景值是："
                    response_dict["Content"] += xml_dict.get("EventKey")
            elif "SCAN" == xml_dict.get("Event"):
                # 代表当前用户已关注，扫描的二维码
                response_dict = {
                    "ToUserName": xml_dict.get("FromUserName"),
                    "FromUserName": xml_dict.get("ToUserName"),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": "感谢你的扫描..."
                }
                if xml_dict.get("EventKey"):
                    response_dict["Content"] += "；场景值是："
                    response_dict["Content"] += xml_dict.get("EventKey")
            else:   # 可能被取消关注了
                print '%s取消关注了...' % xml_dict.get("FromUserName")
                response_dict = None
        else:
            response_dict = {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": '文件格式不对,你丫欠揍吧~',
            }
        if response_dict:
            response_dict = {'xml': response_dict}
            return xmltodict.unparse(response_dict)
        else:
            return ''
    else:
        return 'error', 403

if __name__ == '__main__':
    app.run(port=8002, debug=True)
