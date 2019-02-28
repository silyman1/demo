# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs
import unicodecsv
def get_qikang_list(url):
	urls_list =[]
	rep =requests.get(url)
	soup = BeautifulSoup(rep.text,'lxml')
	results = soup.find_all('a')
	for result in results:
		if result.string.startswith('第'):
			print result.string
			print result.get('href')
			urls_list.append(result.get('href'))
	return urls_list
def get_zhaiyao(url):
	urls_list =[]
	rep =requests.get(url)
	soup = BeautifulSoup(rep.text,'lxml')
	results = soup.find_all('a')
	for result in results:
		if result.string=='摘要':
			print result.string
			print result.get('href')
			urls_list.append(result.get('href'))
	return urls_list
def get_detail(url):
	item_list =[]
	rep =requests.get(url)
	soup = BeautifulSoup(rep.text,'lxml')
	results = soup.find('span',attrs={'id':'Author'})
	if results == None:
		return
	goal=results.find_all('tr')
	if goal == None:
		return
	for i in range(1,len(goal)):
		myitem = []
		item=goal[i].find_all('font',attrs={'color':'blue'})
		author = '暂无'
		company = '暂无'
		mail= '暂无'
		try:
			author = item[0].string
			print item[0].string
		except:
			author = '暂无'
		try:
			company = item[1].string
			print item[1].string
		except:
			company = '暂无'
		mail_pats = goal[i].find_all('a')
		for pat in mail_pats:
			if pat.get('href').startswith('mailto'):
				mail= pat.string
		print mail
		myitem.append(author)
		myitem.append(company)
		myitem.append(mail)
		item_list.append(myitem)
	return item_list
def write_csv(items,csvfile):
	if items is None:
		return
	csv_write = unicodecsv.writer(csvfile,encoding='utf-8-sig',dialect='excel')
	for item in items:
		csv_write.writerow(item)

if __name__ == "__main__":
	csvfile = file('xjgy.csv','a')#ks.csv
	csvfile.write(codecs.BOM_UTF8)
	fo = open("xjgy.log",'w+')
	s = sys.stdout
	sys.stdout = fo
	origin_url = 'http://www.rubbertire.com.cn/gy/xjgy/ch/reader/issue_browser.aspx'
	urls_list = get_qikang_list(origin_url)
	flag =True
	for url in urls_list:
		astr = 'http://www.rubbertire.com.cn/gy/xjgy/ch/reader/'
		url = astr+url
		zurls_list = get_zhaiyao(url)
		for zurl in zurls_list:
			url = astr+zurl
			print '=============',url
			if url == 'http://www.rubbertire.com.cn/gy/xjgy/ch/reader/view_abstract.aspx?file_no=XJY19941211&flag=1':
				flag = False
				print 'go on'
			if flag:
				print 'pass'
				continue
			items_list = get_detail(url)
			write_csv(items_list,csvfile)
			print '++++++++++++++++++'