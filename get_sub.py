import requests
from api_key import token

url='http://api.zhuwei.me/v1/captions/'

v_id=input('please input video url:')[-11:]

# test token
# token='a2d09c7d76fced01f8be4b1f4cce8bec'

def get_sub(url):
	sub=requests.get(url+'?'+'api-key='+token)
	sub_content=sub.json().get('contents').get('content')
	sub_name=input('Input the sub_file_name:')
	with open('%s.srt' % sub_name,'w') as sub_file:
		sub_file.write(sub_content)
	print('Download complete!')

have_sub=requests.get(url+v_id+'?'+'api-key='+token)
# print(have_sub.json())
try:
	sub_list=have_sub.json().get('response').get('captions').get('available_captions')

	for i in sub_list:
		if i.get('language')=='zh-Hans':
			print('find sub!')
			get_sub(i.get('caption_content_url'))
except Exception as e:
	print('Can\'t find sub! ',e)
