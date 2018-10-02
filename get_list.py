import requests
import json
import os
import time

with open('config.json','r') as conf:
	config=json.load(conf)

token=config['token']


def get_list(list_id):
	list_url='https://api.zhuwei.me/v1/videos/playlists/'
	list_res=requests.get(list_url+list_id+'?api-key='+token).json()
	if list_res['meta']['code']==200:
		print('Find video list!')
		v_list=list_res['response']['playlist']['videos']
		return v_list
	else:
		print('can\'t find the video list!')
		return False

def save_list(res):
	data='\n'.join(res)
	if not os.path.exists('playlist'):
		os.mkdir('playlist')
	file_name=time.strftime("%Y-%m-%d【%H:%M】", time.localtime()) 
	with open('playlist/%s.txt' % file_name,'w') as txt:
		txt.write(data)
	print('playlist: '+list_id+' complete!')

if __name__ == '__main__':
	list_id=input('please input playlist url:')[-34:]
	res=get_list(list_id)
	save_list(res)

