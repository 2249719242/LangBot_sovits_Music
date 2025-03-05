<<<<<<< HEAD
## 安装

配置完成 主程序后使用管理员账号向机器人发送命令即可安装(由于使用的是yiri-mirai库，所以对新版Langbot不适用，若要兼容新版本，需要修改main.py中的ctx.add_return("reply", [Voice(path=str(silk_path))])，其中的Voice是把音频转换为qq录音。（但本人还未完成修改)：

```
!plugin get <插件发布仓库地址>
```
或查看详细的[插件安装说明](https://github.com/RockChinQ/QChatGPT/wiki/5-%E6%8F%92%E4%BB%B6%E4%BD%BF%E7%94%A8)

## 使用  
1、需要先部署[sovits项目](https://github.com/svc-develop-team/so-vits-svc)  

2、将"flask_api_full_song_slice.py"和"开启接口服务.bat"文件剪切sovits项目的主目录下
更改好参数后，双击打开"开启接口服务.bat"文件运行flask_api_full_song_slice

3、需要下载安装ffmpeg   

4、前往https://www.alapi.cn/  进行注册（截至上传时是免费的）

   在token管理中点击Copy复制Token

   在本插件文件夹下main.py文件中找到这行，并替换成你获取到的token（不要弄丢引号）

```
./LANGBOT_SOVITS_MUSIC/main.py
token = 'YOURTOKEN'  # 请将这里的'YOUR_TOKEN'替换为你实际获取的token
cookie = "YOUR_COOKIE"  # 请将这里的'YOUR_COOKIE'替换为你实际获取的cookie
```
以及flask_api_full_song_slice.py
修改这段：
spk需要与config_name中的speaker一致
if spk=='ly':
   model_name = "models/G_56800.pth"  # 模型地址
   config_name = "configs/config.json"  # config地址
   diffusion_path="models/diffusion/model_7000.pt"
