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

headers = { 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4)AppleWebKit/537.36(KHTML,likeGecko)Chrome/44.0.2403.157 Safari/537.36',    'Connection':'keep-alive','Accept-Encoding':'gzip, deflate'}
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
	rep =requests.get(url,headers=headers)
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
		oneone = a.split(',')
		for one in oneone:
			if one:
				l11.append(one)
	print 'l11:',l11
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
	someitems = get_detail2(rep.text)
	# for someitem in someitems:
		# item_list.append(someitem)
	for item in l11:
		myitem = []
		name = item.strip()
		company = ''
		# tel =''
		# mymail = ''
		if nums:
			for num in nums: 
				company += company_list[int(num)-1]
		else:
			if company_list:
				company = company_list[0]
		print name,':',company
	# goal=results.find_all('tr')
	# if goal == None:
		# return
	# for i in range(1,len(goal)):
		# myitem = []
		# item=goal[i].find_all('font',attrs={'color':'blue'})
		# author = '暂无'
		# company = '暂无'
		# mail= '暂无'
		# try:
			# author = item[0].string
			# print item[0].string
		# except:
			# author = '暂无'
		# try:
			# company = item[1].string
			# print item[1].string
		# except:
			# company = '暂无'
		# mail_pats = goal[i].find_all('a')
		# for pat in mail_pats:
			# if pat.get('href').startswith('mailto'):
				# mail= pat.string
		# print mail
		myitem.append(name)
		myitem.append(company)
		for someitem in someitems:
			if someitem[0].startswith(name):
				myitem.append(someitem[1])
				myitem.append(someitem[2])
		item_list.append(myitem)
	return item_list
def get_detail2(rep):
	# csvfile = file('gyscl2.csv','a')#ks.csv
	# csvfile.write(codecs.BOM_UTF8)
	someitems = []
	soup = BeautifulSoup(rep)
	results = soup.find_all("span",attrs={"class":"J_zhaiyao"})
	if results == None:
		return someitems
	for result in results:
		item =[]
		if result.find('strong') == None:
			continue
		if result.find('strong').string == '通讯作者:' or result.find('strong').string == '作者简介':
			# pat1 =re.compile('.*?E-mail:(.*?)')
			# pat2 =re.compile('电话:(\d+),.*?E-mail')

			for thing in result.stripped_strings:
				if thing.find('电话:') ==-1 or thing.find('E-mail:') ==-1 or thing.startswith('E-mail:'):
					continue
				print 'thing:',thing
				name =''
				tel =''
				mymail =''

				goals = thing.split(',')
				for i in range(len(goals)):
					if i == 0:
						name = goals[i].replace(':','').strip()
					if goals[i].find('电话:') !=-1:
						tel = goals[i].replace('电话:','').strip()
					if goals[i].find('@') !=-1:
						mymail = goals[i].replace('E-mail:','').strip()
				print name
				print tel
				print mymail
				item.append(name)
				item.append(tel)
				item.append(mymail)
		someitems.append(item)
		# write_csv(someitems,csvfile)
	return someitems
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
	flag =True
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
			# if url == 'http://www.iwt.cn/CN/abstract/abstract15017.shtml':
				# flag = False
				# print 'go on'
			# if flag:
				# print 'pass'
				# continue
				# url = 'http://www.iwt.cn/CN/abstract/abstract12047.shtml'
				items_list = get_detail(url)
				write_csv(items_list,csvfile)
				print '++++++++++++++++++'
				# break
			# break
		# break