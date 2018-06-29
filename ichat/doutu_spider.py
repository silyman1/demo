#-*-coding:utf-8-*-
import requests
import random
from bs4 import BeautifulSoup
class Doutu_Spider(object):
	base_url ='https://fabiaoqing.com/bqb/lists/type/liaomei/page/'
	headers={'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
	def getpic(self):
		page_num = random.randint(0,25)
		url = self.base_url+str(page_num)
		response = requests.get(url,headers=self.headers).text
		soup = BeautifulSoup(response,'lxml')
		
		img_urls = soup.find_all('img',attrs={'class':'ui image lazy'})
		#for j in img_urls:
			#print 'l:',j
		i =random.randint(0,len(img_urls))

		return img_urls[i].get('data-original')
	def save(self,url):
		img = requests.get(url,headers=self.headers).content
		with open(r'E:\gitprojects\test\a.jpg','wb') as f:  
			f.write(img)
			f.close()
if __name__ == '__main__':
	#f=r'E:\gitprojects\test\a.jpg' #图片地址
	a= Doutu_Spider()
	url = a.getpic()
	a.save(url)
