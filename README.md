#HEAD

让你的qq机器人利用sovits4.1模型实现翻唱

## 参考项目

[LangBot_RVC项目](https://github.com/zzseki/LangBot_RVC_Music?tab=readme-ov-file) 


由于 sovits4.1 的要求更高，相较于原项目，本项目在人声分离端和 sovits 端均新增了显存清理及垃圾回收机制（否则显存容易溢出，个人配置为 4060 8G）。此外，在 sovits 推理端采用了切片推理的方式（切片大小设定为 10 秒）。

由于目前使用的是旧版 Qchat，音频转换为 QQ 语音的功能依赖于 yiri-mirai 库。而在新版 Langbot 中，其内置库与 yiri-mirai 存在冲突，导致无法安装 yiri-mirai 库。

Tips:若需兼容新版本，需对本项目中 main.py 的代码段进行修改，具体为：ctx.add_return("reply", [Voice(path=str(silk_path))])。其中，Voice 的作用是将音频转换为 QQ 录音格式.

或者在sovits项目中将输出文件转换为目标语音格式。（目前本人尚未完成相关修改，之后有空改一下）


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

4、前往https://www.alapi.cn/  进行注册，用来获取网易云的歌曲（免费一天时间，后面要冲会员）

   在token管理中点击Copy复制Token
   
   然后点击‘我的接口’，搜索并开启网易云接口

   在本插件文件夹下main.py文件中找到以下代码行，并替换成你获取到的token（不要弄丢引号）

```
./LANGBOT_SOVITS_MUSIC/main.py
token = 'YOURTOKEN'  # 请将这里的'YOUR_TOKEN'替换为你实际获取的token
cookie = "YOUR_COOKIE"  # 请将这里的'YOUR_COOKIE'替换为你实际获取的cookie
#关于cookie的获取方式可以参考这个网址：https://blog.csdn.net/qq_46607667/article/details/136751625

```

同时修改flask_api_full_song_slice.py文件：
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

