# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs
import unicodecsv
'''http://www.iwt.cn/CN/article/showTenYearVolumnDetail.do?nian=1986'''
def get_qikang_list(url):
	urls_list =[]
	rep =requests.get(url)
	soup = BeautifulSoup(rep.text,'lxml')
	results = soup.find_all('a',attrs={"class":'J_WenZhang'})
	for i in range(4,len(results)):
		print results[i].string.replace(' ','')
		print results[i].get('href')
		urls_list.append(results[i].get('href'))
	return urls_list
def get_zhaiyao(url):
	urls_list =[]
	rep =requests.get(url)
	soup = BeautifulSoup(rep.text,'lxml')
	results = soup.find_all('a',attrs={'class':'J_VM'})
	for result in results:
		if result.string=='摘要':
			print result.string
			print result.get('href')
			urls_list.append(result.get('href'))
	return urls_list
def get_detail(url):
	item_list =[]
	rep =requests.get(url)
	rep.encoding = rep.apparent_encoding
	soup = BeautifulSoup(rep.text,'lxml')
	results = soup.find('td',attrs={'class':'J_author_cn'})
	if results == None:
		return
	name_list = []
	for result in results.stripped_strings:
		print result
		name_list.append(result)
	l1 =name_list[::2]
	l11 = []
	for a in l1:
		l11.append(a.replace(',',''))
	print l1
	l2 = name_list[1::2]
	nums =[]
	for i in l2:
		nums = re.findall('\d+',i)
		print nums
	result2 =  results.parent.next_sibling.next_sibling.find('td')
	print result2
	company_list = []
	for result in result2:
		if result.string != None and result.string != '<br/>':
			print result.string,type(result.string)
			company_list.append(result.string)
	print results.parent.next_sibling.next_sibling.find('td').string
	index = 0
	for item in l11:
		name = item
		company = ''
		for num in nums: 
			company += company_list[int(num)-1]
		print name,':',company
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
	csvfile = file('gyscl.csv','a')#ks.csv
	csvfile.write(codecs.BOM_UTF8)
	fo = open("gyscl.log",'w+')
	s = sys.stdout
	sys.stdout = fo
	for page in range(1981,2019):
		origin_url = 'http://www.iwt.cn/CN/article/showTenYearVolumnDetail.do?nian='+str(page)
		print origin_url
		urls_list = get_qikang_list(origin_url)
		for url in urls_list:
			astr = 'http://www.iwt.cn/CN'
			url = url.replace('..',astr)
			zurls_list = get_zhaiyao(url)
			for zurl in zurls_list:
				url = zurl.replace('..',astr)
				print '=============',url
			# if url == 'http://www.rubbertire.com.cn/gy/xjgy/ch/reader/view_abstract.aspx?file_no=LTY20161209&flag=1':
				# flag = False
				# print 'go on'
			# if flag:
				# print 'pass'
				# continue
				url = 'http://www.iwt.cn/CN/abstract/abstract12047.shtml'
				items_list = get_detail(url)
				write_csv(items_list,csvfile)
				print '++++++++++++++++++'
				break
			break