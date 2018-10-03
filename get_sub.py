import requests
import multiprocessing
import html,json,time,os
from get_list import get_list

api_url='https://api.zhuwei.me/v1/captions/'

with open('config.json','r') as conf:
	config=json.load(conf)

if config['token']:
	token=config['token']
else:
	token=config['test_token']
play_list=config['play_list_file']
input_playlist_url=config['input_playlist_url']

#字幕获取方法
def get_sub(api_url,title,**kw):
	
	#构造想要的字幕url
	sub_url=api_url+'?api-key='+token\
	+('&multilanguage=multilanguage' if kw['multilanguage'] else '')\
	+('&notimeline=notimeline' if kw['notimeline'] else '')
	
	#请求下载字幕url
	sub_res=requests.get(sub_url)
	sub_content=sub_res.json().get('contents').get('content')
	# print(sub_content)
	# sub_name=input('Input the sub_file_name:')
	useless=['&quot;','?']
	for i in useless:
		title=title.replace(i,'')
	
	#写入字幕内容文件
	if not os.path.exists('Download_subtitles'):
		os.mkdir('Download_subtitles')
	with open('Download_subtitles/%s.srt' % html.unescape(title),'w') as sub_file:
		sub_file.write(html.unescape(sub_content))
	print('Download 【'+title+'.srt】 complete!')


#主任务 查询字幕存在与否
def req_api(v_url):
	have_sub=requests.get(api_url+v_url[-11:]+'?'+'api-key='+token).json()
	# print(have_sub)
	try:
		res=have_sub['response']['captions']
		sub_title=res['title']
		sub_list=res['available_captions']
		# print(sub_list)
	except Exception as e:
		print('Can\'t find sub! check video id!',e)

	find=False
	for i in sub_list:
		if config['multilanguage']:
			#寻找目标双语字幕
			if config['which_language_to_zh'] in i['language']:
				print('Find （'+sub_title+'） 【'+i['language']+' and zh-Hans】 subtitle!')
				get_sub(i['caption_content_url'],sub_title,**config)
				find=True
				break
		#单语言字幕
		else:
			if i['language'] in config['single_language']:
				print('Find （'+sub_title+'） 【'+i['language']+'】 subtitle!')
				get_sub(i['caption_content_url'],sub_title,**config)
				find=True
				break
	#写入下载历史
	if find:
		with open('history.txt','a') as his_log:
			his=sub_title+'   '+time.strftime("%Y-%m-%d【%H:%M】", time.localtime())\
			+'\n'+v_url+'\n\n'
			his_log.write(his) 
	else:
		print('Can\'t find '+i['language']+' subtitle!')

#多进程下载字幕列表
def download_list(tasks):
	cpu_count=multiprocessing.cpu_count()
	pool=multiprocessing.Pool(cpu_count)
	pool.map(req_api,tasks)
	
#入口
def main():
	if input_playlist_url:
		download_list(get_list())
	elif play_list:
		try:
			with open('%s'% play_list,'r') as v_list:
				tasks=v_list.read().split('\n')
			download_list(tasks)
		except Exception as e:
			print('Can\'t find list! check your play_list\'s path!',e)				
	else:
		v_url=input('please input video url:')
		req_api(v_url)


if __name__ == '__main__':
	main()