import requests
# import multiprocessing
import html,json,time,os,re
from concurrent import futures
from get_list import get_list

class Sub_getter(object):

	with open('config.json','r') as conf:
		config=json.load(conf)

	def __init__(self):
		self.api_url='https://api.zhuwei.me/v1/captions/'
		config=self.config
		if config['token']:
			self.token=config['token']
		else:
			self.token=config['test_token']
		self.play_list=config['play_list_file']

	#下载字幕到文件
	def get_sub(self,api_url,title,**kw):
		
		#构造自定义配置的字幕url
		sub_url=api_url+'?api-key='+self.token\
		+('&multilanguage=multilanguage' if kw['multilanguage'] else '')\
		+('&notimeline=notimeline' if kw['notimeline'] else '')
		
		#获取字幕url数据
		sub_res=requests.get(sub_url)
		sub_content=sub_res.json().get('contents').get('content')
		# useless=['&quot;','?']
		# for i in useless:
		# 	title=title.replace(i,'')
		
		#写入字幕文件
		if not os.path.exists('Download_subtitles'):
			os.mkdir('Download_subtitles')

		if os.name=='nt':
		#windows文件替换非法字符
			with open('Download_subtitles/%s.srt' % re.sub('[\/:?"*<>|]','-',html.unescape(title)),'w') as sub_file:
				sub_file.write(html.unescape(sub_content))
		else:
			with open('Download_subtitles/%s.srt' % html.unescape(title).replace('/','-'),'w') as sub_file:
				sub_file.write(html.unescape(sub_content))
		self.complete+=1
		print('Download 【'+title+'.srt】 complete!')


	#查询字幕支持列表
	def req_api(self,v_url):
		have_sub=requests.get(self.api_url+v_url[-11:]+'?'+'api-key='+self.token).json()
		
		#返回200ok,得到字幕列表
		if have_sub['meta']['code']==200:
			res=have_sub['response']['captions']
			sub_title=res['title']
			sub_list=res['available_captions']
			# print(sub_list)
			
			#设置目标语言字幕找到与否状态
			find=False
			for i in sub_list:
				#寻找目标双语字幕
				if self.config['multilanguage']:
					if self.config['which_language_to_zh'] in i['language']:
						print('Find （'+sub_title+'） 【'+i['language']+' and zh-Hans】 subtitle!')
						self.get_sub(i['caption_content_url'],sub_title,**self.config)
						find=True
						break
				#单语言字幕
				else:
					if i['language'] in self.config['single_language']:
						print('Find （'+sub_title+'） 【'+i['language']+'】 subtitle!')
						self.get_sub(i['caption_content_url'],sub_title,**self.config)
						find=True
						break
			#找到目标字幕写入成功下载历史
			if find:
				with open('Success_history.txt','a') as succ_log:
					succ=html.unescape(sub_title)+'   '+time.strftime("%Y-%m-%d【%H-%M】", time.localtime())\
					+'\n'+v_url+'\n\n'
					succ_log.write(succ) 
			else:
				print('Can\'t find '+i['language']+' subtitle!')

		#未获取到字幕列表写入失败历史文件
		else:
			print('Can\'t find '+v_url+' sub! check video id!')
			with open('Failure_history.txt','a') as fail_log:
					fail=v_url+'   '+time.strftime("%Y-%m-%d【%H-%M】", time.localtime())+'\n\n'
					fail_log.write(fail) 

	#多线程下载字幕列表
	def download_list(self,tasks):
		# cpu_count=multiprocessing.cpu_count()
		# pool=multiprocessing.Pool(cpu_count)
		# pool.map(self.req_api,tasks)
		with futures.ThreadPoolExecutor(50) as e:
			e.map(self.req_api,tasks)
		
		print('Download complete,Success get:【',self.complete,'】subtitles. Failure:【',len(tasks)-self.complete,'】')

	#入口
	def run(self):
		self.complete=0

		if self.play_list:
			try:
				with open('%s'% self.play_list,'r') as v_list:
					tasks=v_list.read().split('\n')
				self.download_list(tasks)
			except Exception as e:
				print('Can\'t find list! check your play_list\'s path!',e)

		else:
			v_url=input('Please input video or playlist url:')
			if 'list=' in v_url:	
				try:
					self.download_list(get_list(v_url))
				except Exception:
					print('Check your playlist url or api-key!')
			else:
				self.req_api(v_url)


if __name__ == '__main__':
	app=Sub_getter()
	app.run()
