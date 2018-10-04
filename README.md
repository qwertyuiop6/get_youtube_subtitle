## Python Youtube Subtitles Download Script

基于[zhuwei.me](https://api.zhuwei.me)字幕接口编写下载脚本<br>

>在config.json里修改配置下载选项:<br>
```javascript
{
	
	"test_token":"a2d09c7d76fced01f8be4b1f4cce8bec",  	//测试用api-key
	"token":"", 				       		//个人申请的api-key
	"single_language":"zh-Hans",		//单语言下载选项,"en","zh-Hans",...
	"multilanguage":false,			//是否下载双语,true 或false
	"which_language_to_zh":"en",		//哪种语言=>简中,"en","kr","jp"...
	"notimeline":false,			//无字幕时间线 ,ture 或false
	"input_playlist_url":false,		//输入playlist链接批量下载
	"play_list_file":""			//从指定文件读取视频链接下载字幕
}
```
* test_token : 接口测试的api,可下载单个字幕
* token : 私人api-key, 在[api.zhuwei.me](https://api.zhuwei.me)申请
* single_language : 单语言字幕下载
* multilanguage : 是否下载双语字幕,若为true则single_language选项无效
* which_language_to_zh : xxx语言+简中(机翻)字幕 (接口暂只支持xxx=>简中)
* notimeline : 字幕不要时间线
* input_playlist_url : 是否开启模式:输入playlist链接进行下载,需有私人api-key
* play_list_file : 从所填文件读取链接下载(文件可自行创建,手动添加url,一行一个链接)
<br>
> 环境:Python3, 依赖: requests (pip install requests)

### Usage:
1 . 单个视频链接下载字幕:

> python get_sub.py

2 . 从Youtube playlist 链接批量下载字幕(需申请api-key):
>　修改congig.json  "input_playlist_url" 为true,再运行:
> python get_sub.py

3 . 从本地文件批量读取视频链接下载字幕(需申请api-key):
>批量视频链接的文件:<br>1 .手动创建文件,一行一个视频链接 或者:<br> 1 .运行 python get_list.py 将自动把输入的playlis链接里的所有视频链接下载到文件<br> 

%@##----确保有文件后----------------->><br>
>2 ."play_list_file" 填入文件全称<br>3 . 同时确保"input_playlist_url"为false<br>4 . 运行 python get_sub.py

## Other:

* 字幕语言支持详见[api.zhuwei.me](https://api.zhuwei.me)