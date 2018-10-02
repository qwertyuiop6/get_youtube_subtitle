## Python youtube subtitle download script

基于[zhuwei.me](https://api.zhuwei.me)字幕接口编写<br>

>在config.json里修改配置下载选项:<br>
```javascript
{
	
	"test_token":"a2d09c7d76fced01f8be4b1f4cce8bec",  	
	"token":"d9ca7344e013c0d5c79ea441dad005078fc84f0f", 	
	"multilanguage":true,
	"which_language_to_zh":"en",	
	"notimeline":false,		
	"language":"zh-Hans",
	"download_list":"playlist/2018-10-02【01:55】.txt"	
}
```
* test_token : 接口测试的api
* token : 私人api-key, 在[api.zhuwei.me](https://api.zhuwei.me)申请
* multilanguage : 是否下载双语字幕,若为true则language选项无效
* which_language_to_zh :  ??语言+简中(机翻)字幕 (接口暂只支持??=>简中)
* notimeline : 字幕不要时间线
* download_list : 批量下载的下载列表文件位置

#### usage:
```shell
python get_sub.py
```
