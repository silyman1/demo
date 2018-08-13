#-*-coding:utf-8-*-
import requests
import json
import PyV8
import re
import base64
import binascii
import random
import rsa
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class SinaLogin(object):
	def __init__(self,username,password):
		self.username = username
		self.password =password
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
						'Referer':'https://login.sina.com.cn/signup/signin.php'}


		self.session = requests.session()
		self.s = self.session.get('http://login.sina.com.cn',headers=self.headers)
		if(self.s.status_code == 200):
			print 'init session successfully'
	def getpostdata(self):
		pre_url = 'https://login.sina.com.cn/sso/prelogin.php?entry=account&callback=sinaSSOController.preloginCallBack&su=MTE2MTYyNjU5NyU0MHFxLmNvbQ%3D%3D&rsakt=mod&client=ssologin.js(v1.4.15)&_=1534126164960%20HTTP/1.1'
		response = self.session.get(pre_url)
		print response.text
		jsondata = re.findall(r'\((\{.*?\})\)',response.text)[0]
		data = json.loads(jsondata)
		try:
			servertime = data.get('servertime')#time.time()*1000
			nonce = data.get('nonce')
			pubkey = data.get('pubkey')
			rsakv = data.get('rsakv')
			return servertime,nonce,pubkey,rsakv
		except Exception:
			print 'getpostdata failed'
			raise Exception
	def encode_su(self):
		a = base64.b64encode(urllib.quote(self.username))
		print 'su',base64.b64encode(urllib.quote(self.username))
		b = base64.encodestring(urllib.quote(self.username))
		print b
		return base64.b64encode(urllib.quote(self.username))
	def encode_sp(self,pubkey,servertime,nonce):
		Pubkey = int(pubkey, 16)
		rsa_n = int('10001',16)
		rsakey = rsa.PublicKey(Pubkey, rsa_n) #创建公钥
		codeStr = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #根据js拼接方式构造明文
		pwd = rsa.encrypt(codeStr,rsakey)  #使用rsa进行加密
		print binascii.hexlify(pwd)
		return binascii.hexlify(pwd)  #将加密信息转换为16进制。
	def login(self,servertime,nonce,rsakv,pubkey):
		prelt = random.randint(40, 100)
		print prelt
		su = self.encode_su()
		sp = self.encode_sp(pubkey, servertime, nonce)
		print '#######################################'
		print su
		print sp
		print servertime
		print nonce
		print rsakv
		print prelt
		post_data = {
					'entry':'account',
					'gateway':'1',
					'from':'',
					'savestate':30,
					'useticket':0,
					'pagerefer':'',
					'vsnf':1,
					'su':su,
					'service':'account',
					'servertime':servertime,
					'nonce':nonce,
					'pwencode':'rsa2',
					'rsakv':rsakv,
					'sp':sp,
					'sr':'1024*768',
					'encoding':'UTF-8',
					'cdult':3,
					'domain':'sina.com.cn',
					'prelt':prelt,
					'returntype':'TEXT'
        }
		response = self.session.post('https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)',data =post_data,allow_redirects=False)
		print '###########',response.status_code
		print response.text.decode('utf-8').encode('gbk','ignore')
if __name__ == "__main__":

	username = '1161626597@qq.com'
	password = 'pzc1161626597'
	sinalogin = SinaLogin(username, password)

	servertime,nonce,pubkey,rsakv = sinalogin.getpostdata()
	sinalogin.login(servertime, nonce, rsakv, pubkey)
	# s = sinalogin.session.get('https://weibo.com/u/2143279462/home')
	# print s.status_code,'3333333'
	# print s.text.decode('utf-8').encode('gbk','ignore')
	# print s.history

