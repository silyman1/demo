# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urlmanager import  UrlManager
import sys
import time
import re
import unicodecsv
import codecs
import json
from getgps import geocodeG
from multiprocessing import Process,Queue,Lock
import threadpool,time
reload(sys)
sys.setdefaultencoding('utf-8')
class Anjuke(object):
	def __init__(self,):
		self.count = 0
		self.wcount = 0
		self.mylock = Lock()
		self.csvfile = file('sz.csv','a')#ks.csv
		self.csvfile.write(codecs.BOM_UTF8)
		self.item_queue = Queue()
		self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
         }
		self.proxies = {'http':'https://121.61.0.33:9999',"https":'https://121.61.0.33:9999'}
		self.mysign = True
		#https://suzhou.anjuke.com/community
		self.rawurl = 'https://suzhou.anjuke.com/community/'
		self.urlmanager = UrlManager()
	def get_villages(self):
		rep = requests.get(self.rawurl,headers = self.headers,verify=False,timeout=2)
		soup = BeautifulSoup(rep.text,'lxml')
		results = soup.find_all('span',attrs={'class':'elems-l'})
		items = results[0].find_all('a')
		for item in items:
			if item.get("title") == "全部小区":
				print '剔除(全部)这一选项'
				continue
			vurl = item.get('href')
			print vurl
			self.get_villages2(vurl)
			#self.get_villages3(vurl)
			print '======================================'
		self.urlmanager.save_urls_process_status(self.urlmanager.new_urls,r'new_urls.txt')
		self.urlmanager.save_urls_process_status(self.urlmanager.crawled_urls,r'crawled_urls.txt')
	def get_villages2(self,vurl):
		rep = requests.get(vurl,headers = self.headers,verify=False,timeout=2)
		soup = BeautifulSoup(rep.text,'lxml')
		results = soup.find_all('div',attrs={'class':'sub-items'})
		items = results[0].find_all('a')
		for item in items:
			if item.get("title") == "全部小区":
				print '剔除(全部)这一选项2'
				continue
			url2 = item.get('href')
			print url2
			self.get_villages3(url2)
	def get_villages3(self,url):
		while 1:
			rep = requests.get(url,headers = self.headers,verify=False,timeout=2)
			soup = BeautifulSoup(rep.text,'lxml')
			results = soup.find_all('div',attrs={'_soj':'xqlb'})
			for result in results:
				item_url = result.get('link')
				self.count += 1
				print 'No.',self.count,':',item_url
				self.urlmanager.add_new_url(item_url)
			next_item = soup.find('a',attrs={'class':'aNxt'})
			if next_item == None:
				break
			else:
				url = next_item.get('href')
		# time.sleep(1)
	def get_detail(self,c_url):
		rlist=[]
		# item ={}
		try:
			rep = requests.get(c_url,headers = self.headers,verify=False,timeout = 4)
		except:
			print 'current:urls num2:',self.urlmanager.new_urls_size()
			self.urlmanager.readd_new_url(c_url)
			return
		if rep.url.startswith('https://www.anjuke.com/captcha-verify/'):
			self.urlmanager.readd_new_url(c_url)
			self.urlmanager.save_urls_process_status(self.urlmanager.new_urls,r'new_urls.txt')
			self.urlmanager.save_urls_process_status(self.urlmanager.crawled_urls,r'crawled_urls.txt')
			return
		print rep.url
		soup = BeautifulSoup(rep.text,'lxml')
		name = soup.find('h1')
		addr =name.find('span')
		print name.contents[0].strip(),addr.string
		rlist.append(name.contents[0].strip().decode("utf-8"))
		rlist.append(addr.string.decode("utf-8"))
		village = re.search("(.*?)-.*?",addr.string).group(1)
		try:
			y,x = geocodeG(addr.string.replace(village,'苏州'))#昆山
		except:
			try:
				y,x = geocodeG(name.contents[0].strip().decode("utf-8"))
			except:
				y,x = geocodeG(u'苏州'+village)#昆山
		rlist.append(y)
		rlist.append(x)
		price = re.search('.*comm_midprice":"(.*?)"',rep.text)
		if price ==None:
			price = u'暂无报价'
		else:
			price = price.group(1)
		print 'price:',price
		rlist.append(price)
		# item['price'] = price.group(1)
		result = soup.find('dl',attrs={"class":'basic-parms-mod'})
		for a in result.find_all('dd'):
			# print a.string.strip().decode('utf-8')
			rlist.append(a.string.strip().decode('utf-8'))
			print '----'
		id = re.search('view/(\d+)',rep.url)
		rent_url = 'https://ks.anjuke.com/v3/ajax/communityext/?commid='+ str(id.group(1)) +'&useflg=onlyForAjax'
		print rent_url
		response = requests.get(rent_url,headers = self.headers,verify=False,timeout=2)
		print response.text
		content=json.loads(response.text)
		print content.get('comm_propnum').get('rentNum'),content.get('comm_propnum').get('saleNum')
		rlist.append(content.get('comm_propnum').get('rentNum'))
		rlist.append(content.get('comm_propnum').get('saleNum'))
		# self.item_queue.put(rlist)
		return rlist
		# item['property-type'] = value_list[0].string.strip().replace("：",'')
		# item['property-cost'] = value_list[1].string.strip().replace("：",'')
		# item['area'] = value_list[2].string.strip().replace("：",'')
		# item['households'] = value_list[3].string.strip().replace("：",'')
		# item['build-years'] = value_list[4].string.strip().replace("：",'')
		# item['parking-nums'] = value_list[5].string.strip().replace("：",'')
		# item['cap-rate'] = value_list[6].string.strip().replace("：",'')
		# item['greeening-rate'] = value_list[7].string.strip().replace("：",'')
		# item['developer'] = value_list[8].string.strip().replace("：",'')
		# item['property-management'] = value_list[9].string.strip().replace("：",'')
			# print j.string.strip().replace("：",'')
		# for (k,v) in  item.items(): 
			# print "dict[%s]=" % k,v 
	def write_to_csv(self,item):
		csv_write = unicodecsv.writer(self.csvfile,encoding='utf-8-sig',dialect='excel')
		csv_write.writerow(item)
	def write_to_csv2(self):
		if not self.item_queue.empty():
			self.mylock.acquire(10)
			with open('ks.csv','a') as csvfile:
				item = self.item_queue.get()
				csv_write = unicodecsv.writer(csvfile,encoding='utf-8-sig',dialect='excel')
				csv_write.writerows(item)
			self.mylock.release()
	def write_to_csv3(self):
		while not self.item_queue.empty():
			item = self.item_queue.get()
			csv_write = unicodecsv.writer(self.csvfile,encoding='utf-8-sig',dialect='excel')
			self.wcount +=1
			print 'write No.',self.wcount,'url'
			csv_write.writerow(item)
	def start2(self):
		num = 0
		self.get_villages()
		print 'current:urls num1:',self.urlmanager.new_urls_size()
		while self.urlmanager.has_new_url():
			num +=1
			new_url = self.urlmanager.get_new_url()
			try:
				print 'get No.',num,'url'
				url_process = Process(target=self.get_detail,args=(new_url,self.item_queue))
				url_process.start()
			except:
				with open("anjuke.log",'w+') as f:
					f.write('current:urls num2:')
					f.write(str(self.urlmanager.new_urls_size()))
				self.urlmanager.readd_new_url(new_url)
				self.urlmanager.save_urls_process_status(self.urlmanager.new_urls,r'new_urls.txt')
				self.urlmanager.save_urls_process_status(self.urlmanager.crawled_urls,r'crawled_urls.txt')
		while not self.item_queue.empty():
			print 'write No.',num,'url'
			self.write_to_csv(item)
			# write_process = Process(target=self.write_to_csv2)
			# write_process.start()
	def start3(self):
		# self.get_villages()
		fo = open("anjuke.log",'w+')
		s = sys.stdout
		sys.stdout = fo
		print 'current:urls num1:',self.urlmanager.new_urls_size()
		while self.urlmanager.has_new_url():
			newlist = []
			flag = 100
			while flag:
				if self.urlmanager.has_new_url():
					new_url = self.urlmanager.get_new_url()
					newlist.append(new_url)
					flag -=1
				else:
					break
			pool = threadpool.ThreadPool(12)
			requests = threadpool.makeRequests(self.get_detail,newlist)
			[pool.putRequest(req) for req in requests]

			pool.wait()
			self.urlmanager.save_urls_process_status(self.urlmanager.new_urls,r'new_urls.txt')
			self.urlmanager.save_urls_process_status(self.urlmanager.crawled_urls,r'crawled_urls.txt')
			self.write_to_csv3()
		sys.stdout = s
	def start(self):
		fo = open("anjuke.log",'w+')
		s = sys.stdout
		sys.stdout = fo
		num  =0
		# self.get_villages()
		print 'current:urls num1:',self.urlmanager.new_urls_size()
		while self.urlmanager.has_new_url():
			new_url = self.urlmanager.get_new_url()
			self.urlmanager.save_urls_process_status(self.urlmanager.new_urls,r'new_urls.txt')
			self.urlmanager.save_urls_process_status(self.urlmanager.crawled_urls,r'crawled_urls.txt')
			try:
				item = self.get_detail(new_url)
				num +=1
				print 'write No.',num,'url'
				self.write_to_csv(item)
			except:
				print 'current:urls num2:',self.urlmanager.new_urls_size()
				self.urlmanager.readd_new_url(new_url)
				self.urlmanager.save_urls_process_status(self.urlmanager.new_urls,r'new_urls.txt')
				self.urlmanager.save_urls_process_status(self.urlmanager.crawled_urls,r'crawled_urls.txt')
		sys.stdout = s
if __name__ == "__main__":
	# fo = open("anjuke.log",'w+')
	# s = sys.stdout
	# sys.stdout = fo
	
	a = Anjuke()
	a.start()
	# sys.stdout = s
	print u'安居客数据爬取完毕！！！'