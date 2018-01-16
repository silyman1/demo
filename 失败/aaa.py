# -*- coding: utf-8 -*-
import requests
import time
from copyheaders import headers_raw_to_dict
url1= 'https://www.zhihu.com/signup?next=%2F'
s = requests.Session()
response = s.get(url1)
cookie1 = response.cookies.get_dict()
print cookie1
authorization='oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
#content-type='multipart/form-data; boundary=----WebKitFormBoundaryNddGmdMf8F8p9Ult'
#User-Agent='Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
post_headers_raw = b'''

accept:application/json, text/plain, */*

Accept-Encoding:gzip, deflate, br

Accept-Language:zh-CN,zh;q=0.9,zh-TW;q=0.8

authorization:oauth c3cef7c66a1843f8b3a9e6a1e3160e20

Connection:keep-alive

DNT:1

Host:www.zhihu.com

Origin:https://www.zhihu.com

Referer:https://www.zhihu.com/signup?next=%2F

User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36

'''
headers = headers_raw_to_dict(post_headers_raw)
headers['X-UDID'] = 'AFCiSgFd-gyPTs1arsdBa8XzsdrAvrxw3fI='

headers['X-Xsrftoken'] = '59adec9d-9550-46a2-9d5c-aab33f4be3d1'
username='18721350673'
password='1161626597'
timestamp = int(float(time.time()) * 1000)
data = {

	'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20', 'grant_type': 'password',

	'timestamp': '1515994615454', 'source': 'com.zhihu.web',

	'signature': '106cfd3d6c636253bc77fcf49fa43e38ae4c6049', 'username': username,

	'password': password, 'captcha': '',

	'lang': 'cn', 'ref_source': 'homepage', 'utm_source': ''

	}




url33 = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
hh = headers.pop('X-Xsrftoken')
z = s.get(url33, headers=headers)
print(z.json())
response2 = s.post('https://www.zhihu.com/api/v3/oauth/sign_in',data=data,headers=headers)
print response.status_code
print response2.text
