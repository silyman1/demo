# -*- coding: UTF-8 -*-


import requests
import sys
import os
import json
import threading
import time 
from datetime import datetime
import re
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')

class Bilibili_Spider(object):
	video_num=0
	referer = 'https://www.bilibili.com/'
	lock = threading.Lock()
	__stdout__ = sys.stdout
	fu = open('total.log','w+')
	

	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
		'referer':referer,
	}
	header2 = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
	}
	base_url = 'https://api.bilibili.com/x/web-interface/ranking/region?callback=jQuery17207618180920996875_1516760805670&jsonp=jsonp&rid=20&day=7&original=0&_=1516760817794'
	predict_num = 200
	type_list =[]
	def get_types(self):
		print 'get type'
		url= 'https://www.bilibili.com/'
		response = requests.get(url,headers=self.header2)
		soup  =BeautifulSoup(response.text)
		items = soup.find_all('li')
		for item in items:
			try:
				type = item.find('div',attrs={'class':'nav-name'}).text
				print type
				detail_types =item.find_all('ul',attrs={'class':'sub-nav'})
				detail_types = detail_types[0].find_all("span")
			except:
				continue
			detail_types=[i.text for i in detail_types]
			print detail_types
			if type and detail_types:
				self.type_list.append((type,detail_types))
		return
	def parse(self,content):
		for type_h in self.type_list:
			#print type_h
			if content.get('data')[0].get('typename') in type_h[1]:
				print 'in'
				if  not os.access("%s.txt"%type_h[0], os.W_OK):
					print "File is not accessible to write"
					if self.lock.acquire():
						pass
				fn = open('%s.txt'%type_h[0],'a')
				sys.stdout = fn
				if content.get('data')[0].get('title'):
					print type_h[0]
					print content.get('data')[0].get('typename')
				type_h[1].remove(content.get('data')[0].get('typename'))
				for i in range(1,11):
					try:
						print '%s.'%i,content.get('data')[i].get('title')
						self.video_num += 1
					except:
						pass
				print '-----------------------------------------------------------------'
				sys.stdout = self.__stdout__
				print self.lock.locked()
				if self.lock.locked():
					self.lock.release()
	def count_error(self,content,i):
		fo = open('error.log','a')
		sys.stdout = fo
		print 'error_num %s=============================================='%i
		print content
		sys.stdout = self.__stdout__
	def main(self):
		print u'正在获取所有类型名称....'
		sys.stdout = self.fu
		self.get_types()
		sys.stdout =self.__stdout__
		print u'获取所有类型名称完毕，准备获取所有数据...'
		for i in range(self.predict_num+1):
			url = self.base_url.replace(re.findall('&rid=(.*?)&',self.base_url)[0],str(i))
			print url
			print u'正在获取某类型排名前十的视频...'
			response =self.getdetail(url)#requests.get(url,headers=self.headers)
			pattern = re.compile('\w.*?\(')
			#h_name = 'h%s'%i
			#h_name  = threading.Thread(target=self.getdetail,args=(url,))
			#h_name.start()
			a = re.findall(pattern,response.text)[0]
			try:
				content = json.loads(response.text.replace(a,'').replace(')',''))
			except Exception as e:
				self.count_error(content,i)
				raise e
			sys.stdout =self.fu
			print content
			sys.stdout =self.__stdout__
			if content.get('code')==-400 or content.get('data') ==[]:
				self.count_error(content,i)
			else:
				t_name = 't%s'%i
				t_name  = threading.Thread(target=self.parse,args=(content,))
				t_name.start()
				#self.parse(content)
	def getdetail(self,url):
		return requests.get(url,headers=self.headers)
	def mytime(self):
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
	
if __name__ =='__main__':
	start_time = datetime.now()
	a = Bilibili_Spider()
	a.main()
	endtime = datetime.now()
	print u'运行时间为：',(endtime-start_time).seconds
	print u'video num :',a.video_num 
 