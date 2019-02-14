# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urlmanager import  UrlManager
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')
class Anjuke(object):
	def __init__(self,):
		self.count = 0 
		self.headers = {,
            'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; Chitanda/Akari) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/6.0.0.58_r884092.501 NetType/WIFI'
         }
		self.mysign = True
		#https://suzhou.anjuke.com/community
		self.rawurl = 'https://ks.anjuke.com/community/'
		self.urlmanager = UrlManager()
	def get_list(self):
		i = 1
		while self.mysign:
			page_url = self.rawurl + 'p' + str(i)
			rep = requests.get(page_url,headers = self.headers,verify=False)
			print rep.text
			soup = BeautifulSoup(rep.text,'lxml')
			results = soup.find_all('div',attrs={'_soj':'xqlb'})
			if results:
				for result in results:
					self.count +=1
					item_url = result.get('link')
					print self.count,':',item_url
					flag = self.urlmanager.add_new_url(item_url)
					if flag ==False:
						self.mysign =False
						break
			else:
				break
				
			i += 1
			time.sleep(1)
		return self.urlmanager.new_urls
	def get_detail(self,c_url):
		pass
	def write_to_csv(self,item):
		pass 

	def start(self):
		self.get_list()
		
if __name__ == "__main__":
	fo = open("anjuke.log",'w+')
	s = sys.stdout
	sys.stdout = fo
	
	a = Anjuke()
	a.start()
	sys.stdout = s
	print u'安居客数据爬取完毕！！！'