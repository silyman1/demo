import requests
import re
import time
import PyV8
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
class BaiduYun_login(object):
	def __init__(self):
		self.js = '''
			function() {
            	return "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(e) {
                var t = 16 * Math.random() | 0
                  , n = "x" === e ? t : 3 & t | 8;
                return n.toString(16)
            }).toUpperCase()
        }
		'''
		self.jstext = PyV8.JSContext()
		self.jstext.__enter__()
		self.jstext.eval(self.js)
	def get_tt(self):
		return time.time()*1000

	def get_token(self,gid):
		tokenurl = 'https://passport.baidu.com/v2/api/?getapi&tpl=netdisk&subpro=netdisk_web&apiver=v3&tt=1533537872571&class=login&gid=%s&loginversion=v4&logintype=basicLogin&traceid=&callback=bd__cbs__uz4vbt'%gid
		response = requests.get(tokenurl)
		if response.status_code == '200':
			pattern = re.compile(r'"token":\s*"(\w+)"')
			token = pattern.search(pattern,response.text)
			if token:
				print 'token:',token
				return token
		else:
			print 'get token failed'
		return None
	def get_gid(self):
		return self.jstext.locals.gid()
	def get_password(self,pubkey,password):
		pubkey = pubkey.replace("\\n",'\n').replace('\\','')
		rsakey = RSA.importKey(pubkey)  # 导入读取到的公钥
		cipher = PKCS1_v1_5.new(rsakey)  # 生成对象
		cipher_text = base64.b64encode(cipher.encrypt(password.encode(encoding="utf-8")))  # 通过生成的对象加密message明文，注意，在python3中加密的数据必须是bytes类型的数据，不能是str类型的数据
		return cipher_text
	def get_rsakey(self,token,tt,gid):
		keyurl = https://passport.baidu.com/v2/getpublickey?token=%s&tpl=netdisk&subpro=netdisk_web&apiver=v3&tt=%d&gid=%s&loginversion=v4&traceid=&callback=bd__cbs__ro4v18%(token,tt,gid)
		response = requests.get(keyurl)
		if response.status_code == '200':
			pattern = re.compile(r'"key":\s*"(\w+)"')
			key = pattern.search(pattern,response.text)
			if key:
				print 'key:',key
				return key
		else:
			print 'get key failed'
		return None

	def get_ppui_logintime(self):
		return 88888
	def login(self):
		post_data = {
				'staticpage':'https://yun.baidu.com/res/static/thirdparty/pass_v3_jump.html',
				'charset':'UTF-8',
				'token':token,
				'tpl':'netdisk',
				'subpro':'netdisk_web',
				'apiver':'v3',
				'tt':tt,
				'codestring':'njGbc06de444762f5e1022a1568a60192002fc45b0690018a4a',
				'safeflg':0,
				'u':'https://yun.baidu.com/disk/home',
				'isPhone':'false',
				'detect':'1',
				'gid':gid,
				'quick_user':0,
				'logintype':'basicLogin',
				'logLoginType':'pc_loginBasic',
				'idc':'',
				'loginmerge':'true'
				'foreignusername':'',
				'username':'username',
				'password':'password',
#'verifycode:bexi
				'mem_pass':'on',
				'rsakey':'rsakey',
				'crypttype':12,
				'ppui_logintime':92027,
				'countrycode':'',
fp_uid:
fp_info:85228d73e97c9a5eb768fbc3d9f274da002~~~x~xx0wjvGhlV9nb_Vxx5zjJ94uxXpJyXMJ_jjJ94uxXpJhXnY_RxnJr-xnJrExxrDxx-Qj0bxHtRTXpiR1MJn12cFXnuzX7iR3p9TYn9i92Hy92-g94ldcn0z14uh945n14ld4M9mXMYi929R14ldHhRTCwafHhc_AVxrGjv9M0V9u__rVxuHVxuCVxrKj0bxch~e5hEy57ClAwg~HhJx9sFRHMufch~e5hEy57ClAwg~HhJx9sFRHMufctSxqtak3tG03hXm3BGVq0CeHwm~qu__tj0bVCtGw57GfqpFn9B5n92Hn5Bvk5n~~92q~XwXwXnbyCt5m9nYgXMqlC4by12q-9tX-5nHF9nYyCM~l54bn14Jy9MAk5nqw9w9iDwAlCwam3pAd9Bcm92-FCB5R5wbm92l-X4JhCw5xX4GMXwci925g54Ji54rl12v~X4aMXBGw9h9x9w9m54a~Ctbi9wbx94vMXR__IVxrLVxryVxrJVxrUxxbBjvOwJEYzF_vjJqBiL3wSy3J__xVxrsxxubVxugVxueVxucVxuXVxuqjRZ40VX2bgX2YF12bn12HzXnbzXY__
loginversion:v4
dv:tk0.35988213966558091533269516134@qqv0vz6C7g4kqbLQGbLmi-6kKy6QixsXii4r8hC3P2FAyNMyhCArljMyYi9MsgP-YXEmi-sC0XsuixsXii4r8hC3P2FAyNMyhCArljMyYi9MsgP-YXEmi-sC3xDMi~6k7b6m~AFAxuA3rsMyYFAyhNsrYNKvrgKcPaKRFbsI9tskWlDCKb6m~AFAxuA3rsMyYFAyhNsrYNKvrgKcPaKRFbsIK~Dkolgv0sqDkK-4kpjs2i~6kFyDm~lDC3-4k6g4kpj6kqX4uitsC6bsk0-4kpy6k9X4r8hC3P2FAyNMyhCArljMyYRL-YjEMoGCvYQJBxmPvxlDCKy4kFc4kpcskA~4v~aE-VT4BWV9B8VKQicskAb6Iqj4k9iskpc4ui_z~~JB~u69Y9Lhuvh62iX4kFxwvlPvbi4I6yDC0t6IpgDC9-sCAt6k3~sC6g6I9xsCp-6C6jhvlJu8jKu6Z4XYxPBtT9RreEuAT9-Yd4X~yLR8VERVTEBF_yvs6mii4kpi6kKbsgpy4kpi6IFbsg9t4kpi6IFb6CqXsmi-sgF_
vcodefrom:login
traceid:0894FE01
callback:parent.bd__pcbs__3dkzwl

if __name__ == '__main__':
	yunlogin = BaiduYun_login()
	account = input(u"用户名：")
	password = input(u"密码：")


