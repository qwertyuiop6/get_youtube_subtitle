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
	"play_list_file":""			//从指定文件读取视频链接下载字幕
}
```
* test_token : 接口测试的api,可下载单个字幕
* token : 私人api-key, 在[api.zhuwei.me](https://api.zhuwei.me)申请
* single_language : 单语言字幕下载
* multilanguage : 是否下载双语字幕,若为true则single_language选项无效
* which_language_to_zh : xxx语言+简中(机翻)字幕 (接口暂只支持xxx=>简中)
* notimeline : 字幕不要时间线
* play_list_file : 从所填文件读取链接下载(文件可自行创建,手动添加url,一行一个链接)
<br>

> 环境:Python3, 依赖: requests (pip install requests)

### Usage:
1 . 命令行输入单个视频链接或playlist链接(需申请api-key)即可下载字幕:

> python get_sub.py

2 . 从本地文件批量读取视频链接下载字幕(需申请api-key):
>1 . 手动创建文件,一行一个视频链接<br>
>2 . "play_list_file" 填入文件**全称**(.xxx后缀不要忘记加)<br>3 . 运行 python get_sub.py

３.将playlist所有视频链接暂存文件再下载
>1 . 运行 python get_list.py 将自动把输入的playlis链接里的所有视频链接保存到文件<br> 2 . python get_sub.py 将自动下载以上文件
## Other:

* 字幕语言支持详见[api.zhuwei.me](https://api.zhuwei.me)