# -*- coding=utf-8 -*-
import itchat
import requests
import json
from itchat.content import *
from doutu_spider import Doutu_Spider
@itchat.msg_register([TEXT])
def text_reply(msg):
	#return "test:auto_reply"
	info = msg['Text'].encode('utf-8')
	url = 'http://www.tuling123.com/openapi/api'
	data = {
			u"key":"68d95d1a63ba4ac8b0c311e9acf3920e",
			"info": info, 
			u"loc": "", 
			"userid": "",
	}
	content = requests.get(url,data).text
	s = json.loads(content,encoding="utf-8")
	print "s=",s['code'],s['text']
	if s['code'] == 100000:
		#itchat.send("hello",toUserName='filehelper')
		#return u'你大爷：'+ s['text']
		return s['text']
	else:
	    return "test:auto_reply"
@itchat.msg_register([PICTURE])
def pic_reply(msg):
	f = r'E:\gitprojects\test\a.jpg' #图片地址
	a= Doutu_Spider()
	url = a.getpic()
	a.save(url)
	print msg['FromUserName']
	#itchat.send("hello test",toUserName=msg['FromUserName'])
	itchat.send("@img@%s" % f,toUserName=msg['FromUserName'])


itchat.auto_login(enableCmdQR=1,hotReload=True)
#itchat.send("hello",toUserName='filehelper')

itchat.run(debug =True)
  
