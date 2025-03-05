#HEAD

让你的qq机器人利用sovits4.1模型实现翻唱

## 参考项目

[LangBot_RVC项目](https://github.com/zzseki/LangBot_RVC_Music?tab=readme-ov-file) 


由于sovits4.1要求更高，与原项目相比，人声分离端以及sovits端均增加了清除显存等垃圾回收机制（不然会爆显存，个人配置4060 8G）,在sovits推理端采用切片推理(切片大小设置为10秒)


(由于使用的是旧版Qchat，将音频转换为qq语音的是yiri-mirai库，新版Langbot中的库与其冲突，无法安装yiri-mirai库)

若要兼容新版本，需要修改本项目中main.py中的代码段：ctx.add_return("reply", [Voice(path=str(silk_path))])。其中的Voice是把音频转换为qq录音,或者将sovits的输出文件转换为语言格式。（本人还未完成修改)：


## 安装

配置完成 主程序后使用管理员账号向机器人发送命令即可安装


```
!plugin get <插件发布仓库地址>
```
或查看详细的[插件安装说明](https://github.com/RockChinQ/QChatGPT/wiki/5-%E6%8F%92%E4%BB%B6%E4%BD%BF%E7%94%A8)

## 配置
1、需要先部署[sovits项目](https://github.com/svc-develop-team/so-vits-svc)  

2、将"flask_api_full_song_slice.py"和"开启接口服务.bat"文件剪切sovits项目的主目录下
更改好参数后，双击打开"开启接口服务.bat"文件运行flask_api_full_song_slice

3、需要下载安装ffmpeg   

4、前往https://www.alapi.cn/  进行注册（免费一天时间，后面要冲会员）

   在token管理中点击Copy复制Token

   在本插件文件夹下main.py文件中找到这行，并替换成你获取到的token（不要弄丢引号）

```
./LANGBOT_SOVITS_MUSIC/main.py
token = 'YOURTOKEN'  # 请将这里的'YOUR_TOKEN'替换为你实际获取的token
cookie = "YOUR_COOKIE"  # 请将这里的'YOUR_COOKIE'替换为你实际获取的cookie
#关于cookie的获取方式可以参考这个网址：https://blog.csdn.net/qq_46607667/article/details/136751625
```
以及修改flask_api_full_song_slice.py文件
```
if spk=='ly':#(spk需要与config_name中的speaker一致)
   model_name = "models/G_56800.pth"  # 模型地址
   config_name = "configs/config.json"  # config地址
   diffusion_path="models/diffusion/model_7000.pt"#如果没有diffusion模型可以直接删除这行
```

## 使用

配置好后，向机器人发送：   #翻唱[歌名 歌手名][升key或降key][模型说话人名称]

如：#翻唱[春日影 CRYCHIC][0][MYGO]

（第一个框对应网易云的搜索框，提取的是网页版网易云的以第一个搜索结果）

