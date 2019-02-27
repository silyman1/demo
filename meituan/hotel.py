# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random
import sys
import re
import json
import time
reload(sys)
sys.setdefaultencoding('utf-8')
from xpinyin import Pinyin
class MeituanHotel(object):
	def __init__(self):
		self.count = 0 
		self.testcount = 0
		self.citylist = []
		self.url_list = []
		self.User_Agent_List = [
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',]
		self.id_dict = {}
	def get_cities(self):
		url = 'https://www.meituan.com/changecity/'
		headers = {'User-Agent':random.choice(self.User_Agent_List)}
		rep = requests.get(url,headers=headers)
		soup = BeautifulSoup(rep.text,'lxml')
		results = soup.find_all('span',attrs={"class":'cities'})
		p = Pinyin()
		for result in results:
			for item in result.contents:
				self.count +=1
				print item.string
				tmp = p.get_pinyin(item.string.decode('utf-8'), '')
				print tmp
				self.citylist.append(tmp)
		city_ids = re.findall(r'"id":(\d+),.*?"pinyin":"(.*?)",',rep.text)
		for city_id in city_ids:
			self.id_dict[city_id[1]] = city_id[0]
		print 'cities:',self.count
	def get_onecity(self,city):
		print city
		url = 'https://hotel.meituan.com/'+ str(city)+'/'
		headers = {'User-Agent':random.choice(self.User_Agent_List)}
		rep = requests.get(url,headers=headers)
		rep.encoding = rep.apparent_encoding
		soup = BeautifulSoup(rep.text,'lxml')
		soup2 = soup.find('div',attrs={"class":'search-filter-classify'})
		results = soup2.contents[0].find_all('a',attrs={"class":'classify-item'})
		for result in results:
			if result.get('href') != '':
				# if result.string.find(u"全部") == -1:
				print result.string
				print result.get('href')
				self.url_list.append(result.get('href'))
	def get_items(self,url,city):
		aid = re.search(r"ba(.*?)/",url)
		area_id = int(aid.group(1))
		base_url = 'https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=pc&version_name=999.9&cateId=20&attr_28=129&uuid=B7B83B6B1715DA39D2D84C7E88B8D0B3555620BC13D3646B027B183ECE09CCF4%40'
		timestamp = int(time.time()*1000)
		city_id = self.id_dict[city]
		offset=0
		startDay=20190226
		endDay=20190226
		flag = True
		street_hotelcount = 0
		while flag:
			url_str = '&cityId=%s&offset=%d&limit=20&startDay=%d&endDay=%d&q=&sort=defaults&areaId=%d'%(city_id,offset,startDay,endDay,area_id)
			url_str = url_str +'&X-FOR-WITH=gFvFftAJTXd%2F9bArzPV%2F677IslpIckYPuLPdpHVnAJt9TF43OXEaFUAwKZujVNcwvxRJBFP5Lu061vE%2BQWph8jpQtvZ6JCDn90SBtJjj%2Bou2NPbvmD6R3oXdIVJLUvrpirFTMBvFfWJG3kHJ2pL5hA%3D%3D'
			pageurl = base_url+str(timestamp)+url_str
			print pageurl
			flag,street_hotelcount = self.get_hotels(pageurl,street_hotelcount)
			offset +=20
		print 'street_hotelcount:',street_hotelcount
	def get_hotels(self,url,street_hotelcount):
		headers = {'User-Agent':random.choice(self.User_Agent_List)}
		rep = requests.get(url,headers=headers)
		rep2 = json.loads(rep.text)
		searchresult = rep2.get('data').get('searchresult')
		if(searchresult):
			for item in searchresult:
				print item.get('name')
				self.testcount +=1
				street_hotelcount +=1
			return True,street_hotelcount
		else:
			return False,street_hotelcount
	def test(self):
		self.get_cities()
		print '============================================================='
		url = 'https://hotel.meituan.com/xiamen/'
		print self.id_dict['xiamen']
		print '============================================================='
		headers = {'User-Agent':random.choice(self.User_Agent_List)}
		rep = requests.get(url,headers=headers)
		rep.encoding = rep.apparent_encoding
		soup = BeautifulSoup(rep.text,'lxml')
		soup2 = soup.find('div',attrs={"class":'search-filter-classify'})
		soupflags = soup.find_all('span',attrs={"class":'search-arrow-tab'})
		print soupflags
		for flag in soupflags:
			print flag.contents[0].string
			if flag.contents[0].string == u'热门':
				goal = soup2.contents[1]
				print soup2.contents[1]
				break
			else:
				goal = soup2.contents[0]
		results = goal.find_all('a',attrs={"class":'classify-item'})
		for result in results:
			if result.get('href') != '':
				if result.string.find(u"全部") != -1:
					print result.string
					print result.get('href')
					self.url_list.append(result.get('href'))
		for url in self.url_list:
			self.get_items(url,'xiamen')
		print 'testcount:',self.testcount
	def start(self):
		# self.get_cities()
		# for city in self.citylist:
			# self.get_onecity(city)
			# break
		self.test()
if __name__ == '__main__':
	fo = open("meituan.log",'w+')
	s = sys.stdout
	sys.stdout = fo
	m = MeituanHotel()
	m.start()
	sys.stdout = s