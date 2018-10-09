# -*- coding=utf-8 -*-
import itchat
import requests
import json
from itchat.content import *
from doutu_spider import Doutu_Spider
# @itchat.msg_register([TEXT])
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
# @itchat.msg_register([PICTURE])
def pic_reply(msg):
	f = r'E:\gitprojects\test\a.jpg' #图片地址
	a= Doutu_Spider()
	url = a.getpic()
	print url
	a.save(url)
	#print msg['FromUserName']
	return f
	#itchat.send("hello test",toUserName=msg['FromUserName'])
	#itchat.send("@img@%s" % f,toUserName=msg['FromUserName'])
@itchat.msg_register(TEXT,PICTURE, isGroupChat=True)
def group_reply(msg):
	group = itchat.get_chatrooms(update=True)
	for g in group:
		if g['NickName']== u'动物世界':
			if msg['FromUserName'] == g['UserName']:
				print g['UserName'],g['NickName']
				reply = text_reply(msg)
				#itchat.send('%s:%s'%(msg['ActualNickName'],reply ),g['UserName'])
				f = pic_reply(msg)
				print f
				itchat.send("@img@%s" % f,toUserName=g['UserName'])

itchat.auto_login(enableCmdQR=1,hotReload=True)
#itchat.send("hello",toUserName='filehelper')

itchat.run(debug =True)
  
