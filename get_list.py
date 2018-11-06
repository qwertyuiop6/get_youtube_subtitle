import requests
import json
import os,time

with open('config.json','r') as conf:
		config=json.load(conf)
		token=config['token']

def get_list(list_url):
	list_id=list_url[list_url.find('list=')+5:]
	list_api_url='https://api.zhuwei.me/v1/videos/playlists/'
	list_res=requests.get(list_api_url+list_id+'?api-key='+token).json()
	if list_res['meta']['code']==200:
		print('Find video list!')
		v_list=list_res['response']['playlist']['videos']
		for i in range(len(v_list)):
			v_list[i]='https://www.youtube.com/watch?v='+v_list[i]
		return v_list
	else:
		print('Can\'t find the video list! check your url or api-key!')
		return False

def save_list(res):
	data='\n'.join(res)
	# if not os.path.exists('playlist'):
	# 	os.mkdir('playlist')
	file_name=time.strftime("playlist%m%d-%H:%M", time.localtime())
	with open('%s.txt' % file_name,'w') as txt:
		txt.write(data)
	with open('config.json','w') as c:
		config['play_list_file']=file_name+'.txt'
		c.write(json.dumps(config))
	print('playlist download complete!')

def main():
	list_url=input('please input playlist url:')
	save_list(get_list(list_url))

if __name__ == '__main__':
	main()
	
	

