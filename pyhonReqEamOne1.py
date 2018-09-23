'''
爬取最新电影排行榜单
爬虫路线：requests  -bs4
Python版本：3.5
OS :ubuntu 16.04
'''
import requests

import time
from bs4 import BeautifulSoup
#首先我们写好抓取网页的函数
def get_html(url):
	try:
		r=requests.get(url,timeout=90)
		r.raise_for_status()
		#这里我们直到百度贴吧的编码是utf-8，所以手动设置的。爬取其它页面时建议使用:
		#r.endcoding=r.apparent_endcoding
		#r.encoding='utf-8'
		r.encoding='gbk'
		return r.text
	except:
		return "ERROR"
def get_content(url):
	'''
	分析贴吧的网页文件，整理信息，保存在列表变量中
	'''
	#首先把需要爬取信息的网页下载到本地
	html=get_html(url)

	#我们来做一锅汤
	soup=BeautifulSoup(html,'lxml')
	#找到电影排行榜的u1列表
	movies_list=soup.find('ul',class_='picList clearfix')
	if movies_list==None :print('jiade hahahh')
	print('here is here')
	movies=movies_list.find_all('li')
	for top in movies:
		img_url='http:'+top.find('img')['src']
		print(img_url)
		
		#name=top.find('span',class_='sTit').a.text
		if not top.find('span',class_='sTit')==None:

			name=top.find('span',class_='sTit').string
			print(name)
		try:
			time=top.find('span',class_='sIntro').text
		except:
			time="暂无上映时间"
		#这里用bs4库迭代找出'pActor'的所有子孙节点，即每一位演员解决了名字分割的问题

		actors=top.find('p',class_='pActor')
		actor=''
		if actors != None:
			for  act in actors.contents:
				actor=actor+act.string+'  '
		#找到影片简介
		x= top.find('p',class_='pTxt pIntroShow')
		intro=''
		if x!=None:intro=x.text


		print("片名:{}\t{}\n{}\n{}\n\n".format(name,time,actor,intro))
		#download the picture
		with open('/home/jiade/'+name+'.jpg','wb+')as f:
			f.write(requests.get(img_url).content)
def main():
	url='http://dianying.2345.com/top/'
	get_content(url)
if __name__=="__main__":
		main()
