'''
抓取百度贴吧---生活大爆炸的基本内容
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
		r=requests.get(url,timeout=30)
		r.raise_for_status()
		#这里我们直到百度贴吧的编码是utf-8，所以手动设置的。爬取其它页面时建议使用:
		#r.endcoding=r.apparent_endcoding
		r.encoding='utf-8'
		return r.text
	except:
		return "ERROR"
def get_content(url):
	'''
	分析贴吧的网页文件，整理信息，保存在列表变量中
	'''
	#初始化一个列表来保存所有的帖子信息：
	comments=[]
	#首先把需要爬取信息的网页下载到本地
	html=get_html(url)

	#我们来做一锅汤
	soup=BeautifulSoup(html,'lxml')
	#按照之前的分析，我们找到所有具有'j_thread_list clearfix'属性的li标签。返回一个列表
	liTags=soup.find_all('li',attrs={'class':' j_thread_list clearfix'})
	#if liTags==None:print("没有找到liTags!!!.......")
	#通过循环找到每个帖子里的我们需要的信息

	for li in liTags:
		#初始化一个字典来储存文章信息：
		comment={}
	#在这里使用一个try except防止爬虫找不到信息从而停止运行
		try:
			comment['title']=li.find('a',attrs={'class':'j_th_tit '}).text.strip()
			comment['link']="http://tieba.baidu.com/"+li.find('a',attrs={'class':'j_th_tit '})['href']
			comment['name']=li.find('span',attrs={'class':'tb_icon_author '}).text.strip()
			comment['time']=li.find('span',attrs={'class':"threadlist_reply_date pull_right j_reply_data"}).text.strip()
		#	comment['replyNum']=li.find('span',attrs={'class':'threadlist_rep_num center_text'}).text.strip()
			comments.append(comment)
		except:
			print('出了点小问题。')
	return  comments
def out2File(dict):
	"""
	#将爬取到的文件写入到本地
	#保存到当前目录的TTBT.txt文件中。	
    """
	with open('/home/jiade/TTBT.txt','a+') as f:

		for comment in dict:
			#f.write('标题:{}\t 链接：{}\t 发贴人：{}\t 发帖时间:{}\t 回复数量：{}\n'.format(comment['title'],comment['link']))
			f.write('标题:{}\t 链接：{}\t 发贴人:{}\t发帖时间{}：\t 回复数量:\t \n'.format(comment['title'],comment['link'],comment['name'],comment['time']))
		print('当前网页爬取完成。')

def main(base_url,deep):
	url_list=[]
	for i in range(0,deep):
		url_list.append(base_url+'&pn'+str(50*i))
	print('所有的网页已经下载到本地！开始筛选信息...')
	#循环写入所有的数据
	for url in url_list:
		content=get_content(url)
		out2File(content)
	print('所有的信息都已经保存完毕！')
base_url='http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'
	#设置需要爬取的页码数量
deep=1
main(base_url,deep)
