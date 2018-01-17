#—*—coding=utf-8
import urllib2
import sys
'''
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from bs4 import BeautifulSoup
url1 = 'http://music.163.com/discover/toplist?id=3778678'#云音乐热歌榜
response = requests.get(url1)
print response.status_code
html = response.content
fo = open ('a.log','w')
sys.stdout = fo
print html '''
#soup = BeautifulSoup(html)
#sss = soup.find_all('ul')
#items = soup.find('iframe')

#a = items.find('body')
url1 = 'http://music.163.com/discover/toplist?id=3778678'
request = urllib2.Request(url1)
response =urllib2.urlopen(request)
fo = open ('a.log','w')
sys.stdout = fo
print response.read()