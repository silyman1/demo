#-*- coding:utf-8 _*-  
'''
@file : ziru.py
@auther : Ma
@time : 2019/02/27
'''

import re
import urllib2
import requests
import random
from aip import AipOcr
from urllib import urlretrieve
from PIL import Image
import xlwt
import time
import pytesseract
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs
import unicodecsv
ua = ["Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1",
	  "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
	  "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
	  'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
	  'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
	  'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13',
	  'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/8.0.552.224 Safari/533.3',
	  'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.8 (KHTML, like Gecko) Chrome/7.0.521.0 Safari/534.8',
	  'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.458.1 Safari/534.3',
	  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
	  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
	  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
	  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
	  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
	  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Chrome/17.0.940.0 Safari/535.8',
	  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.77 Safari/535.7ad-imcjapan-syosyaman-xkgi3lqg03!wgz'
	  ]


# 将png的透明背景色变成白色
def background_turn_white(image_name):
	""" 将png的透明背景色变成白色 """
	im = Image.open(image_name)
	x, y = im.size

	# 使用白色来填充背景
	p = Image.new('RGBA', im.size, (255, 255, 255))
	p.paste(im, (0, 0, x, y), im)
	white_picture_name = 'white'+ image_name
	p.save(white_picture_name)
	return white_picture_name


# 获取图片
def get_picture(page , image_url):
	""" 获取图片 """
	picture_name = str(page) + 'ziroom.png'
	urlretrieve(url=image_url,filename=picture_name)
	return picture_name


# 读取图片
def get_file_content(file_path):
	""" 读取图片 """
	with open(file_path, 'rb') as fp:
		return fp.read()


# 利用百度ocr将图片转成文字
def bai_du_ocr(white_picture_name):
	""" 你的 APPID AK SK """
	APP_ID = '15642693'
	API_KEY = '8e9ualL4l8WPXXV12Ka17huK'
	SECRET_KEY = 'eU6bbCL9k0ckNwPd2zdkTFCdKGLOD7Iu'

	client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

	image = get_file_content(white_picture_name)

	""" 调用通用文字识别（高精度版） """
	client.basicAccurate(image)
	options = {}
	""" 带参数调用通用文字识别（高精度版） """
	price_res = client.basicAccurate(image, options)
	print price_res
	return price_res['words_result'][0]['words']
	# vcode = pytesseract.image_to_string(white_picture_name)
	# print vcode
	# return vcode

# 当ocr少识别一个数字的时候挽救一波
# 挽救不了，位置不确定
def find_lost_number(price_string):
	list_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

	for num in range(0, 9):
		list_num.remove(int(price_string[num]))

	return list_num[0]


# 将文字转成对应的价格
def get_ziroom_price(page,ROOM_PRICE):

	ROOM_PRICE = eval(ROOM_PRICE)
	image_url = 'http:' + ROOM_PRICE['image']
	print image_url
	offsets = ROOM_PRICE['offset']
	picture_name = get_picture(page,image_url)	# 将图片下载到本地
	white_picture_name = background_turn_white(picture_name) # 将下载的图片背景色改成白色
	price_string = bai_du_ocr(white_picture_name) # 解析出图片的文字

	if len(price_string) == 10:
		prices = []
		# 遍历offset，取出对应的价格
		for offset in offsets:
			if len(offset) == 4:
				price = price_string[offset[0]] + price_string[offset[1]] + price_string[offset[2]] + price_string[offset[3]]
			else:
				price = 0
			prices.append(price)

		print prices
		return prices
	else:
		print('百度OCR识别有问题：' + image_url)
		return [0 for i in range(0,len(offsets))]


# 解析页面
def parse_html(url):
	'''
	:param url:	 请求的网址
	:return: 解析出的结果页面
	'''
	headers = {'User-Agent':random.choice(ua)}
	rep = requests.get(url,headers=headers)
	rep.encoding = rep.apparent_encoding
	print rep.url,'_________________op'
	return rep.text.decode('utf-8')


# 存到excel中
def save_excel(data):
	workbook = xlwt.Workbook(encoding='utf-8')
	booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)

	for i, row in enumerate(data):
		for j, col in enumerate(row):
			booksheet.write(i, j, col)
	workbook.save('ziroom.xls')
def write_csv(items,csvfile):
	if items is None:
		return
	csv_write = unicodecsv.writer(csvfile,encoding='utf-8-sig',dialect='excel')
	for item in items:
		csv_write.writerow(item)
def ziru_get_urls(cityurl):
	headers = {'User-Agent':random.choice(ua)}
	rep = requests.get(cityurl,headers=headers)
	soup = BeautifulSoup(rep.text,'lxml')
	results = soup.find_all('ul',attrs={'class':'clearfix filterList'})
	cons = results[0].find_all('div',attrs={'class':'con'})
	url_list =[]
	# block_dict={}
	for con in cons:
		urltags = con.find_all('a')
		for urltag in urltags:
			if urltag.string == '全部':
				print '全部'
			else:
				print urltag.get('href')
				url_list.append(urltag.get('href'))
	return url_list
def get_items(url):
	items = []
	headers = {'User-Agent':random.choice(ua)}
	rep = requests.get(url,headers=headers)
	rep.encoding = rep.apparent_encoding
	soup = BeautifulSoup(rep.text,'lxml')
	results = soup.find_all('li',attrs={'class':'clearfix'})
	room_price_pat = u'var ROOM_PRICE = (.*?);'
	room_prices_list = re.compile(room_price_pat,re.S).findall(rep.text.decode('utf-8'))		# 价格的image和offset
	room_prices_list = room_prices_list[0]
	try:
		room_price = get_ziroom_price(page, room_prices_list)
	except:
		with open("error.log",'a') as f:
			f.write(url)
		return
	count = 0
	for result in results:
		item =[]
		name = result.find('a',attrs={'class':'t1'}).string
		print name
		price = room_price[count]
		print price
		tmp = result.find('div',attrs={'class':'detail'}).find_all('p')[0]
		area = tmp.find_all('span')[0]
		print area.string
		direction=name[-2]
		print direction
		floor_num = tmp.find_all('span')[1]
		print floor_num.string
		nums=floor_num.string.split('/')
		print nums[0],nums[1]
		housetype = tmp.find_all('span')[2]
		print housetype.string
		count +=1
		item.append(name)
		item.append(price)
		item.append(area.string)
		item.append(direction)
		item.append(housetype.string)
		item.append(nums[0])
		item.append(nums[1])
		items.append(item)
	return items
if __name__ == '__main__':
	csvfile = file('ziroom.csv','a')#ks.csv
	csvfile.write(codecs.BOM_UTF8)
	fo = open("ziru.log",'w+')
	s = sys.stdout
	sys.stdout = fo
	cityurl = 'http://www.ziroom.com/z/nl/z2.html'
	main_urls = ziru_get_urls(cityurl)
	print '==================urls num:',len(main_urls)
	flag = True
	for one_url in main_urls:
		if one_url == '//www.ziroom.com/z/nl/z2-d23008613-b18335729.html':
			flag =False
		if flag:
			continue
	# 获取当前的url有多少页http://www.ziroom.com/z/nl/z2.html
		get_url_page ='http:' + one_url 
		get_url_page_pat = u'下一页</a>.*?<span>共(.*?)页</span>'
		print get_url_page
		pages_html = parse_html(get_url_page)
		pages = re.findall(get_url_page_pat,pages_html)
		if pages:
			print pages[0]
			pages = pages[0]
		else:
			pages = 1

		for page in range(1,int(pages)+1):
			url = get_url_page + '?p='+ str(page)
			items = get_items(url)
			write_csv(items,csvfile)
			time.sleep(1)



