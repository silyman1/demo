#**encoding=utf-8
import requests
from bs4 import BeautifulSoup

Base_URL = "https://github.com/login"
Login_URL = "https://github.com/session"

def get_github_html(url):
	response = requests.get(url)
	first_cookie = response.cookies.get_dict()
	return response.text,first_cookie
def get_token(html):
	soup = BeautifulSoup(html,'lxml')
	res = soup.find("input",attrs={"name":"authenticity_token"})
	token = res["value"]
	return token
def gihub_login(url,token,cookie):
	data= {
	"commit": "Sign in",
	"utf8":"✓",
	"authenticity_token":token,
	"login":"1161626597@qq.com",
	"password":"********"#密码
	}
	response = requests.post(url,data=data,cookies=cookie)
	print(response.status_code)
	cookie = response.cookies.get_dict()
	return cookie
if __name__ == '__main__':
	html,cookie1 = get_github_html(Base_URL)
	token = get_token(html)
	cookie2 = gihub_login(Login_URL,token,cookie1)
	response = requests.get("https://github.com/settings/repositories",cookies=cookie2)
	a = response.text
	soup = BeautifulSoup(a,'lxml')
	item_list = soup.find_all('a',attrs={'class':'mr-1'})
	print u'git仓库如下'
	for item in item_list:
		print item.text