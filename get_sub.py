import requests
import html
import json

api_url='https://api.zhuwei.me/v1/captions/'

with open('config.json','r') as conf:
	config=json.load(conf)

token=config['token']

# test token
# token='a2d09c7d76fced01f8be4b1f4cce8bec'

#字幕获取方法
def get_sub(api_url,title,**kw):
	#构造想要的字幕url
	# sub_url=api_url
	# if kw['multilanguage']:
	# 	sub_url=sub_url[:55]+'en-auto?api-key='+token+'&multilanguage=multilanguage'
	# 	# sub_url='/'.join(sub_url.split('/')[:-2]) +'/en-auto?api-key='+token+'&multilanguage=multilanguage'
	# else:
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
	with open('/home/shadow771/Videos/youtube/%s.srt' % title,'w') as sub_file:
		sub_file.write(html.unescape(sub_content))
	print('Download '+title+'.srt complete!')

def main():
	have_sub=requests.get(api_url+v_id+'?'+'api-key='+token).json()
	print(have_sub)
	try:
		res=have_sub['response']['captions']
		sub_title=res['title']
		sub_list=res['available_captions']
		print(sub_list)
	except Exception as e:
		print('Can\'t find sub! check url!',e)

	find=False
	for i in sub_list:
		if config['multilanguage']:
			#寻找目标双语字幕
			if config['which_language_to_zh'] in i['language']:
				print('Find '+i['language']+' and zh-Hans subtitle!')
				get_sub(i['caption_content_url'],sub_title,**config)
				find=True
				break
		#单语言字幕
		else:
			if i['language'] in config['language']:
				print('Find '+i['language']+'subtitle!')
				get_sub(i['caption_content_url'],sub_title,**config)
				find=True
	if find:
		with open('/home/shadow771/Videos/youtube/history.txt','a') as his:
			his.write(v_url+'\n') 
	else:
		print('Can\'t find '+i['language']+' subtitle!')
if __name__ == '__main__':
	v_url=input('please input video url:')
	v_id=v_url[-11:]
	main()