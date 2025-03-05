import time
import asyncio
from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
import os
import requests
import httpx
import logging
import re
from queue import Queue, Empty
from mirai import Image, MessageChain,Plain,Voice,Plain

import json
import wave
from pydub import AudioSegment
import pyaudio
from audio_separator.separator import Separator
import subprocess
from graiax import silkcoder
import torch
token = 'xqm8k0vw6cvlapuboxveg51fy6ypus'  # 请将这里的'YOUR_TOKEN'替换为你实际获取的token
# cookie = ""  # 请将这里的'YOUR_COOKIE'替换为你实际获取的cookie
cookie = "MUSIC_A_T=1530460507262; MUSIC_R_T=1530460560810; WEVNSM=1.0.0; ntes_utid=tid._.Ki6xp1srQ01BRhEURReRw%252BbuQt8E7ywR._.0; WM_TID=K%2BR1KH6XMtdFRUBARVKUxufqQsoSEx4c; __snaker__id=Q6dpCLdOzKrD4Q8l; ntes_kaola_ad=1; MUSIC_U=00EF144CEBBADDEEAEAEF007AA91772EF3A5333EAEAE668B6AE686DB0DE0047939ADA85FFCE3C4A1790E953A39DF3200743E82CD9BE6E6921EE4DE82A3B2CE5DDAF9F8EEBC0B74719FA0184195229661999811E62D1F02D5A16126EFBF55D43A17490C61B50CE1A872528C380E50C0C07A8B77B77119AFD0F3CB7DD38C499B84526E892E350AE7F00F6D05481789DB245F5CB8608BAD2A44C9AAB3DE31E329C696C91930D5C2489E2E8CEC253562A0F42F6816271F4F2FE4BE2169BB2F36DDD94824375DA04C0FBB9F9AB6CD34185D6E3D620AA420BFD3729189AA48F12E2964849D1F379831E0972F6E677724895E292073890101880D3EA07294BF5A158E82F794075B550609A7FD23B09C918C34B00876E3387E47C9BC8478798E6CC1643503FCF7697A232C21A6E4A90E4C1F0E9CD7FFE6943ACBB1B8BACB4716649B06CE88920E94F9C15B43FB7EDE1606FAE46EFAFC994C3264EC488B9DFEF36EFFA0C71EBD9D3C1A90D70EC35973A5EA780CCBA6; __remember_me=true; _iuqxldmzr_=32; Qs_lvt_382223=1729659434; _ga=GA1.1.1827349827.1729659438; _clck=157rtwz%7C2%7Cfq9%7C0%7C1757; Qs_pv_382223=242568461296104060%2C3639316680175065600%2C1385077227331153700%2C1648293200579800000%2C1844064905126289700; _ga_C6TGHFPQ1H=GS1.1.1729665682.2.1.1729665683.0.0.0; NMTID=00Ouy-pAgHxl_qSZk1fvJLKyTYaB7sAAAGUhOPEog; _ntes_nnid=9cc4f49323cb65cc46edd1f0944279ed,1737396306891; _ntes_nuid=9cc4f49323cb65cc46edd1f0944279ed; WNMCID=kfqbit.1737396308198.01.0; sDeviceId=YD-E%2FlZUDXLzC5AVlAFQAeVh%2BO7E45EqixJ; __csrf=c4df95f69a8ce19848500778adc9a0f1; __csrf=c4df95f69a8ce19848500778adc9a0f1; JSESSIONID-WYYY=%2BE0f5%5C0Rv7o02vot0bKMOJFV%2BNZXTWbTOI7bglxuYBR13r1PoAgw2dnsv2ziuArZ7Fm2gE9NGKOKTCbV%2B71nzUJppZQIfkGBpJuq1O5HnprHib8ir9jzlgGbk4x9TYhSq0XlXBqNvweP0ph72X7qafZVBjc2aJ6SJ1Yac2HB25FAO0Pa%3A1740846924031; WM_NI=cIycOSFt3DhNvxZ7sS8Mcchf%2FdKjMUySh7VpM5SkVzwgviHY3hUIkQScpC%2BfVpC%2B2hlKCZYV37TP5NSpsZxUpFkVP8kMp5JC%2FGcq5AWYOmoYawh5fCVNG7nOWMQg76pdM1E%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb7d43d979dfbb7e145f8b48aa6d54a978a8eadd752ab969682b24485a698d9f02af0fea7c3b92aa197b784ce5986acfda5eb46b6a896d8f259fc93ad84eb6eedbc858bd05fbb8da8d8d57c8feb9d8cd572b5b9ba8acb53f1b89baaea5b91bdc0a4aa6e96b08dccb164b0958dbbdc5ef1e99cb1b84691b0bdbbfb5fb49aa5b7d334a993c0d6c949ed99ad92b84b9587818eee53a3a9a8d6e549969289d8ed4595939f88b63eb4bc83d2c837e2a3"  # 请将这里的'YOUR_COOKIE'替换为你实际获取的cookie
RVC_logs_path = r"D:\AI\AIvoice\RVC1006Nvidia\logs"  # 请将这里的"F:\RVC\RVC1006Nvidia\logs"替换为你部署的RVC项目的logs文件夹的路径
if os.getenv('PATH').find('ffmpeg') == -1:
    os.environ['PATH'] += ';D:\\AI\\ffmpeg\\bin'
new_mdx_params = {"hop_length": 1024, "segment_size": 256, "overlap": 8, "batch_size": 2, "enable_denoise": False}
new_vr_params = {"batch_size": 2, "window_size": 512, "aggression": 5, "enable_tta": False, "enable_post_process": False, "post_process_threshold": 0.2, "high_end_process": False}
model_name='liyi'

# 注册插件
@register(name="RVC_Music", description="RVC翻唱音乐", version="0.1", author="zzseki")
class RVC_Music(BasePlugin):
    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.logger = logging.getLogger(__name__)

        # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_Normal_message_received(self, ctx: EventContext):
        receive_text = ctx.event.text_message
        if "#翻唱" in receive_text:
            print('开始翻唱.')
            await ctx.event.query.adapter.reply_message(ctx.event.query.message_event, [(f"开始翻唱(*´∀`)~♥")], False)            
            pattern = re.compile(r"\[(.*?)\]\[([-+]?\d+)\]\[(.+?)\]")
            match = pattern.search(receive_text)
            if match:
                music = match.group(1)  # 提取第一个方括号内的内容
                f0up = int(match.group(2))  # 提取第二个方括号内的内容
                model_name = match.group(3)  # 提取第三个方括号内的内容
                dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "music")
                wav_path = os.path.join(dir_path, f'{music}.wav')
                # 确保目录存在
                print('111111')
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                id, artists, music_name = self.get_music_id(music)
                print('2111111')
                if id:
                    msg, url = self.get_music(id)
                    if msg != "success":
                        self.ap.logger.info(f"{music_name} {artists}", msg)
                        id, artists, music_name = self.get_music_id(music, 1)
                        if id:
                            msg, url = self.get_music(id)
                    if url:
                        music_name = music_name.replace('/', '&')
                        music_name = music_name.replace('"', '_')
                        music_name = music_name.replace("'", ' ')
                        music_name = music_name.replace(":", ' ')
                        music_name = music_name.replace("：", ' ')
                        artists = artists.replace('/', '&')
                        print('download_audio')
                        wav_path = self.download_audio(url, music_name, artists)
                        # await ctx.event.query.adapter.reply_message(ctx.event.query.message_event, [(f"正在学习 {music_name} {artists}......")], False)
                        try:
                            print('UVR5')
                            # await ctx.event.query.adapter.reply_message(ctx.event.query.message_event, [(f"开始翻唱(*´∀`)~♥")], False)
                            self.UVR5(f"{music_name} {artists}")
                            print('UVR5 down')
                            music_artists=f"{music_name} {artists}"
                            dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "music")
                            music_path = os.path.join(dir_path, f"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Vocals)_5_HP-Karaoke-UVR_(No Reverb)_UVR-DeEcho-DeReverb.wav")
                            
                            print('send_request')
                            gansheng_path = self.send_request(model_name, music_path, f"{music_artists}", int(f0up))
                            
                            if torch.cuda.is_available():
                                torch.cuda.empty_cache()
                                torch.cuda.synchronize()
                            print('send_request down')
                            hesheng_path = os.path.join(dir_path, f"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Instrumental)_5_HP-Karaoke-UVR.wav")
                            banzou_path = os.path.join(dir_path, f"{music_artists}_(Instrumental)_model_bs_roformer_ep_368_sdr_12.wav")  
                            print('伴奏与和声加载完毕')
                            print('干声路径：', gansheng_path)
                            try:
                                print('hesheng_path检验')
                                if not self.is_pcm_s16le(hesheng_path):
                                    print(f"和声 不是 16 位 PCM 格式，正在转换...")
                                    output_path = os.path.splitext(hesheng_path)[0] + "_16bit.wav"
                                    self.convert_to_pcm_s16le(hesheng_path, output_path)
                                print('gansheng_path检验')
                                if not self.is_pcm_s16le(gansheng_path):
                                    print(f"干声 不是 16 位 PCM 格式，正在转换...")
                                    output_path = os.path.splitext(gansheng_path)[0] + "_16bit.wav"
                                    self.convert_to_pcm_s16le(gansheng_path, output_path)
                                print('banzou_path检验')
                                if not self.is_pcm_s16le(banzou_path):
                                    print(f"伴奏 不是 16 位 PCM 格式，正在转换...")
                                    output_path = os.path.splitext(banzou_path)[0] + "_16bit.wav"
                                    self.convert_to_pcm_s16le(banzou_path, output_path)
                            except Exception as e:
                                #输出错误：
                                print("错误：", e)
                            # 加载干声
                            print('加载干声')
                            dry_vocals = AudioSegment.from_wav(gansheng_path)
                            print('加载干声完毕')
                            dry_vocals = dry_vocals + 4
                            print('成功+ 5')
                            print('加载伴奏和和声')
                            accompaniment = AudioSegment.from_wav(banzou_path)
                            harmony = AudioSegment.from_wav(hesheng_path)-5
                             #加载混响
                            print('加载混响')
                            Reverb_vocal_path=os.path.join(dir_path, fr"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Vocals)_5_HP-Karaoke-UVR_(Reverb)_UVR-DeEcho-DeReverb.wav")
                            Reverb_vocal=AudioSegment.from_wav(Reverb_vocal_path)-5
                            #加载原唱的歌声，再-12
                            print('加载原唱的歌声')
                            raw_vocal_path=os.path.join(dir_path, fr"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12.wav")
                            print('开始转换')
                            raw_vocal=AudioSegment.from_wav(raw_vocal_path)
                            raw_vocal=raw_vocal-12
                            print('加载原唱的歌声，再-12db')
                            # 合并音轨(伴奏、原和声、翻唱干声、原唱-12db、混响)
                            print('开始合并音轨')
                
                            combined = accompaniment.overlay(harmony).overlay(dry_vocals).overlay(raw_vocal).overlay(Reverb_vocal)
                            print('合并音轨完毕')
                            RVC_Music_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "RVC_Music")
                            await ctx.event.query.adapter.reply_message(ctx.event.query.message_event, [(f"快唱完了哦~♥")], False)

                            output_file_path = os.path.join(RVC_Music_path, f"{music_artists}_{model_name}.wav")
                            # 导出最终合成的歌曲
                            print('开始导出')
                            combined.export(output_file_path, format="wav")
                            print('导出完毕')
                            if not self.is_pcm_s16le(output_file_path):
                                print(f"伴奏 不是 16 位 PCM 格式，正在转换...")
                                output_path = os.path.splitext(output_file_path)[0] + "_16bit.wav"
                                self.convert_to_pcm_s16le(output_file_path, output_path)
                            print('开始转换silk')
                            silk_path = self.convert_to_silk(model_name, output_file_path, f"{music_artists}")
                            print('开始发送')
                            ctx.add_return("reply", [Voice(path=str(silk_path))])
                            # 删除临时文件
                            os.remove(os.path.join(dir_path, f'{music_artists} dry_vocals_temp.wav'))
                            os.remove(os.path.join(dir_path, f'{music_artists} dry_vocals_with_reverb.wav'))
                            os.remove(gansheng_path)
                            os.remove(hesheng_path)
                            os.remove(banzou_path)
                            os.remove(os.path.join(dir_path, fr"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12.wav"))
                            os.remove(os.path.join(dir_path, fr"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Vocals)_5_HP-Karaoke-UVR.wav"))
                            os.remove(os.path.join(dir_path, fr"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Vocals)_5_HP-Karaoke-UVR_(No Reverb)_UVR-DeEcho-DeReverb.wav"))
                            os.remove(os.path.join(dir_path, fr"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Vocals)_5_HP-Karaoke-UVR_(Reverb)_UVR-DeEcho-DeReverb.wav"))
                            #os.remove(silk_path)
                            os.remove(wav_path)
                            os.remove(output_file_path)
                            ctx.prevent_default()
                        except:
                            # await ctx.event.query.adapter.reply_message(ctx.event.query.message_event, [(f"出错啦！ •᷄ࡇ•᷅")], False)
                            ctx.prevent_default()
                            
                else:
                    
                    self.ap.logger.info("提取音乐名称失败")

    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext, **kwargs):
        receive_text = ctx.event.text_message
        if "#翻唱" in receive_text:
            print('开始翻唱.')
            # await ctx.event.query.adapter.reply_message(ctx.event.query.message_event, [(f"开始翻唱 ...请等待")], False)
            pattern = re.compile(r"\[(.*?)\]\[([-+]?\d+)\]\[(.+?)\]")
            match = pattern.search(receive_text)
            if match:
                music = match.group(1)  # 提取第一个方括号内的内容
                f0up = int(match.group(2))  # 提取第二个方括号内的内容
                model_name = match.group(3)  # 提取第三个方括号内的内容
                dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "music")
                wav_path = os.path.join(dir_path, f'{music}.wav')
                # 确保目录存在
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                id, artists, music_name = self.get_music_id(music)
                if id:
                    msg, url = self.get_music(id)
                    if msg != "success":
                        self.ap.logger.info(f"{music_name} {artists}", msg)
                        id, artists, music_name = self.get_music_id(music, 1)
                        if id:
                            msg, url = self.get_music(id)
                    if url:
                        music_name = music_name.replace('/', '&')
                        music_name = music_name.replace('"', '_')
                        music_name = music_name.replace("'", ' ')
                        music_name = music_name.replace(":", ' ')
                        music_name = music_name.replace("：", ' ')
                        artists = artists.replace('/', '&')
                        print('download_audio')
                        wav_path = self.download_audio(url, music_name, artists)
                        # await ctx.event.query.adapter.reply_message(ctx.event.query.message_event, [(f"正在学习 {music_name} {artists}......")], False)
                        try:
                            print('UVR5')
                            self.UVR5(f"{music_name} {artists}")
                            print('UVR5 down')
                            music_artists=f"{music_name} {artists}"
                            dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "music")
                            music_path = os.path.join(dir_path, f"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Vocals)_5_HP-Karaoke-UVR_(No Reverb)_UVR-DeEcho-DeReverb.wav")
                            
                            print('send_request')
                            gansheng_path = self.send_request(model_name, music_path, f"{music_artists}", int(f0up))
                            
                            if torch.cuda.is_available():
                                torch.cuda.empty_cache()
                                torch.cuda.synchronize()
                            print('send_request down')
                            hesheng_path = os.path.join(dir_path, f"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Instrumental)_5_HP-Karaoke-UVR.wav")
                            banzou_path = os.path.join(dir_path, f"{music_artists}_(Instrumental)_model_bs_roformer_ep_368_sdr_12.wav")  
                            print('伴奏与和声加载完毕')
                            print('干声路径：', gansheng_path)
                            try:
                                print('hesheng_path检验')
                                if not self.is_pcm_s16le(hesheng_path):
                                    print(f"和声 不是 16 位 PCM 格式，正在转换...")
                                    output_path = os.path.splitext(hesheng_path)[0] + "_16bit.wav"
                                    self.convert_to_pcm_s16le(hesheng_path, output_path)
                                print('gansheng_path检验')
                                if not self.is_pcm_s16le(gansheng_path):
                                    print(f"干声 不是 16 位 PCM 格式，正在转换...")
                                    output_path = os.path.splitext(gansheng_path)[0] + "_16bit.wav"
                                    self.convert_to_pcm_s16le(gansheng_path, output_path)
                                print('banzou_path检验')
                                if not self.is_pcm_s16le(banzou_path):
                                    print(f"伴奏 不是 16 位 PCM 格式，正在转换...")
                                    output_path = os.path.splitext(banzou_path)[0] + "_16bit.wav"
                                    self.convert_to_pcm_s16le(banzou_path, output_path)
                            except Exception as e:
                                #输出错误：
                                print("错误：", e)
                            # 加载干声
                            print('加载干声')
                            dry_vocals = AudioSegment.from_wav(gansheng_path)
                            print('加载干声完毕')
                            dry_vocals = dry_vocals + 5
                            print('成功+ 5')
                            print('加载伴奏和和声')
                            accompaniment = AudioSegment.from_wav(banzou_path)
                            harmony = AudioSegment.from_wav(hesheng_path)
                             #加载混响
                            print('加载混响')
                            Reverb_vocal_path=os.path.join(dir_path, fr"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Vocals)_5_HP-Karaoke-UVR_(Reverb)_UVR-DeEcho-DeReverb.wav")
                            Reverb_vocal=AudioSegment.from_wav(Reverb_vocal_path)
                            #加载原唱的歌声，再-12
                            print('加载原唱的歌声')
                            raw_vocal_path=os.path.join(dir_path, fr"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12.wav")
                            print('开始转换')
                            raw_vocal=AudioSegment.from_wav(raw_vocal_path)
                            raw_vocal=raw_vocal-10
                            print('加载原唱的歌声，再-12db')
                            # 合并音轨(伴奏、原和声、翻唱干声、原唱-12db、混响)
                            print('开始合并音轨')
                
                            combined = accompaniment.overlay(harmony).overlay(dry_vocals).overlay(raw_vocal).overlay(Reverb_vocal)
                            print('合并音轨完毕')
                            RVC_Music_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "RVC_Music")
                            print('开始保存')
                            output_file_path = os.path.join(RVC_Music_path, f"{music_artists}_{model_name}.wav")
                            # 导出最终合成的歌曲
                            print('开始导出')
                            combined.export(output_file_path, format="wav")
                            print('导出完毕')
                            if not self.is_pcm_s16le(output_file_path):
                                print(f"伴奏 不是 16 位 PCM 格式，正在转换...")
                                output_path = os.path.splitext(output_file_path)[0] + "_16bit.wav"
                                self.convert_to_pcm_s16le(output_file_path, output_path)
                            print('开始转换silk')
                            silk_path = self.convert_to_silk(model_name, output_file_path, f"{music_artists}")
                            print('开始发送')
                            ctx.add_return("reply", [Voice(path=str(silk_path))])
                            # 删除临时文件
                            os.remove(os.path.join(dir_path, f'{music_artists} dry_vocals_temp.wav'))
                            os.remove(os.path.join(dir_path, f'{music_artists} dry_vocals_with_reverb.wav'))
                            os.remove(gansheng_path)
                            os.remove(hesheng_path)
                            os.remove(banzou_path)
                            os.remove(os.path.join(dir_path, fr"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12.wav"))
                            os.remove(os.path.join(dir_path, fr"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Vocals)_5_HP-Karaoke-UVR.wav"))
                            os.remove(os.path.join(dir_path, fr"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Vocals)_5_HP-Karaoke-UVR_(No Reverb)_UVR-DeEcho-DeReverb.wav"))
                            os.remove(os.path.join(dir_path, fr"{music_artists}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Vocals)_5_HP-Karaoke-UVR_(Reverb)_UVR-DeEcho-DeReverb.wav"))
                            #os.remove(silk_path)
                            os.remove(wav_path)
                            os.remove(output_file_path)
                            ctx.prevent_default()
                        except:
                            # await ctx.event.query.adapter.reply_message(ctx.event.query.message_event, [(f"出错啦！ •᷄ࡇ•᷅")], False)
                            ctx.prevent_default()
                            
                else:
                    
                    self.ap.logger.info("提取音乐名称失败")


    def get_music_id(self, music_name, i=0):
        url = "https://v2.alapi.cn/api/music/search"
        params = {
            "keyword": music_name,
            "token": token,
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()["data"]
            song_id = data['songs'][i]['id']
            artists = data['songs'][i]['artists'][0]['name']
            get_music_name = data['songs'][i]['name']
            return song_id, artists, get_music_name
        except httpx.HTTPStatusError as e:
            self.ap.logger.info(f"获取音乐 id 失败:" + str(e))
            return None
        

    def get_music(self, id):
        time.sleep(2)
        url = "https://v2.alapi.cn/api/music/url"
        params = {
            "id": id,
            "format": "json",
            "token": token,
            'cookie': cookie,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()["data"]
        msg = response.json()["message"]
        if data:
            url = data["url"]
            return msg, url
        else:
            url = None
            return msg, url

    def download_audio(self, audio_url, music_name, artists):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "music")
        mp3_path = os.path.join(dir_path, f"{music_name} {artists}.mp3")
        wav_path = os.path.join(dir_path, f"{music_name} {artists}.wav")
        flac_path = os.path.join(dir_path, f"{music_name} {artists}.flac")
        if re.search("flac", audio_url):
            file_type = "flac"
            file_path = flac_path
        elif re.search("mp3", audio_url):
            file_type = "mp3"
            file_path = mp3_path
        else:
            file_type = "wav"
            file_path = wav_path
        try:
            response = requests.get(audio_url)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    file.write(response.content)
                self.ap.logger.info(f"音频文件已成功保存为" + file_path)
                try:
                    # 加载 音频 文件
                    audio = AudioSegment.from_file(file_path, format=file_type)
                    # 导出为 WAV 格式
                    audio.export(wav_path, format="wav")
                    self.ap.logger.info(f"文件已成功从 {file_type} 转换为 WAV 并保存为 {wav_path}")
                    # 删除 原音频 文件
                    os.remove(file_path)
                    return wav_path
                except Exception as e:
                    self.ap.logger.info(f"转换音频文件发生异常: {str(e)}")
                    return False
            else:
                self.ap.logger.info(f"下载音频文件失败，状态码{response.status_code}")
                return False
        except Exception as e:
            self.ap.logger.info(f"下载音频文件发生异常" + str(e))
            return False
    def convert_to_silk(self,model_name, wav_path: str, name: str) -> str:
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "music")
        silk_path = os.path.join(dir_path, f"{name} {model_name}.silk")
        if os.path.exists(silk_path):
            os.remove(silk_path)
            time.sleep(0.1)
        silkcoder.encode(wav_path, silk_path)

        # print(f"已将 WAV 文件 {wav_path} 转换为 SILK 文件 {silk_path}")
        return silk_path

    def UVR5(self, music_name):
        #music_name:{music_name} {artists}
        # Initialize the Separator class (with optional configuration properties, below)
        try:
            dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "music")
            tmp_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp")
            models_path = os.path.join(tmp_path, "audio-separator-models")
            separator = Separator(output_dir=dir_path, model_file_dir=models_path, mdx_params=new_mdx_params, vr_params=new_vr_params)
            # music_name = music_name
            # 1、去伴奏
            # separator.output_single_stem = "Vocals"
            separator.load_model("model_bs_roformer_ep_368_sdr_12.9628.ckpt")
            # Perform the separation on specific audio files without reloading the model
            output_files = separator.separate(os.path.join(dir_path, f"{music_name}.wav"))
            print(f"Separation complete! Output file(s): {' '.join(output_files)}")
            # 2、去和声
            # 6_HP-Karaoke-UVR.pth 少激进
            # 5_HP-Karaoke-UVR.pth 多激进
            separator.load_model("5_HP-Karaoke-UVR.pth")
            # Perform the separation on specific audio files without reloading the model
            output_files = separator.separate(os.path.join(dir_path, f"{music_name}_(Vocals)_model_bs_roformer_ep_368_sdr_12.wav"))
            print(f"Separation complete! Output file(s): {' '.join(output_files)}")
            # 3、去混响
            # UVR-De-Echo-Normal.pth 少量混响
            # UVR-De-Echo-Aggressive.pth 中等混响
            # UVR-DeEcho-DeReverb.pth  大量混响/正常混响
            # separator.output_single_stem = "Vocals"
            separator.load_model("UVR-DeEcho-DeReverb.pth")
            # Perform the separation on specific audio files without reloading the model
            output_files = separator.separate(os.path.join(dir_path, f"{music_name}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Vocals)_5_HP-Karaoke-UVR.wav"))
            print(f"Separation complete! Output file(s): {' '.join(output_files)}")

            # # 4、降噪
            # # UVR-DeNoise.pth 降噪
            # separator.output_dir = r"F:\music\5jiangzao"
            # separator.output_single_stem = "Vocals"
            # # Load a machine learning model (if unspecified, defaults to 'model_mel_band_roformer_ep_3005_sdr_11.4360.ckpt')
            # separator.load_model("UVR-DeNoise.pth")
            # # Perform the separation on specific audio files without reloading the model
            # output_files = separator.separate(fr"F:\music\4无混响干声_混响\{music_name}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Vocals)_5_HP-Karaoke-UVR_(No Reverb)_UVR-DeEcho-DeReverb.wav")
            # print(f"Separation complete! Output file(s): {' '.join(output_files)}")
            # banzou_path = os.path.join(dir_path, f"{music_name}_(Instrumental)_model_bs_roformer_ep_368_sdr_12.wav")
            # hesheng_path = os.path.join(dir_path, f"{music_name}_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Instrumental)_5_HP-Karaoke-UVR.wav")
        # 最后确保清理所有显存
        finally:   # 清理 CUDA 缓存
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.synchronize()  # 确保所有 CUDA 操作完成
                import gc
                gc.collect()  # 触发 Python 垃圾回收

    

    def send_request(self,model_name, file_path, music_artists, f0up):
          #music_name={music_name} {artists}
            if any(keyword in model_name for keyword in ['闹闹', '东山', '奈央', '由比', '滨结衣', '结衣']):
                speaker = 'dongshan'
            elif any(keyword in model_name for keyword in ['花音', 'jelee', '李依原声', '水母']):
                speaker = 'jelee'
            else:
                speaker = 'liyi'
            url = "http://localhost:1145/wav2wav"
            # 准备请求参数
            data = {
                "audio_path": file_path,  # 直接传入文件路径
                "tran": f0up,               # 可以根据需要调整音调
                "spk": speaker,               # 可以根据需要指定说话人
                "wav_format": "wav"      # 输出格式
            }
            try:
                # 发送POST请求
                response = requests.post(url, data=data)
                response.raise_for_status()
                
                # 保存响应内容为.wav文件
                dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "music")
                output_file_path = os.path.join(dir_path, f"临时干声{music_artists}.wav")
                
                # 确保输出目录存在
                os.makedirs(dir_path, exist_ok=True)
                
                # 保存文件
                with open(output_file_path, "wb") as f:
                    f.write(response.content)
                print(f"文件已保存到: {output_file_path}")
                return output_file_path
                
            except requests.exceptions.RequestException as e:
                print(f"请求失败: {e}")
                return None
            except IOError as e:
                print(f"保存文件失败: {e}")
                return None
            # 保存响应内容为 .wav 文件
        

    def get_index(self, model_name):
        # 目标文件夹路径
        folder_path = os.path.join(RVC_logs_path, model_name)

        # 获取文件夹中的所有文件
        all_items = os.listdir(folder_path)

        # 过滤只获取文件（排除子文件夹），并获取文件的完整路径
        file_paths = [os.path.join(folder_path, f) for f in all_items if os.path.isfile(os.path.join(folder_path, f))]

        # 假设只有一个文件，获取该文件的路径
        if file_paths:
            file_path = file_paths[0]
            return file_path
        else:
            print("获取index文件失败")
            return None

    # def is_pcm_s16le(self, file_path):
    #     """检查 .wav 文件是否为 16 位 PCM (pcm_s16le)"""
    #     try:
    #         with wave.open(file_path, 'rb') as wf:
    #             sample_width = wf.getsampwidth()
    #             return sample_width == 2  # 16位音频每个采样点占用2字节
    #     except wave.Error:
    #         return False
    #---------------claude修改后-----------------
    def is_pcm_s16le(self, file_path):
    #检查 .wav 文件是否为 16 位 PCM (pcm_s16le)
        try:
            # 首先检查文件是否存在
            if not os.path.exists(file_path):
                print(f"文件不存在: {file_path}")
                return False
                
            # 检查文件大小
            if os.path.getsize(file_path) == 0:
                print(f"文件大小为0: {file_path}")
                return False
                
            # 设置超时时间
            import signal
            def timeout_handler(signum, frame):
                raise TimeoutError("读取文件超时")
            
            # 设置5秒超时
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(5)
            
            try:
                with wave.open(file_path, 'rb') as wf:
                    sample_width = wf.getsampwidth()
                    return sample_width == 2  # 16位音频每个采样点占用2字节
            finally:
                signal.alarm(0)  # 取消超时
            
        except wave.Error as e:
            print(f"Wave错误: {file_path} - {str(e)}")
            return False
        except TimeoutError as e:
            print(f"超时错误: {file_path} - {str(e)}")
            return False
        except Exception as e:
            print(f"未知错误: {file_path} - {str(e)}")
            return False

    def convert_to_pcm_s16le(self, input_path, output_path):
        """使用 ffmpeg 将 .wav 文件转换为 16 位 PCM 格式"""
        try:
            # 使用 ffmpeg 进行转换
            subprocess.run([
                'ffmpeg', '-i', input_path,
                '-acodec', 'pcm_s16le',  # 转换为 16 位 PCM
                output_path
            ], check=True)
            # 删除原文件
            os.remove(input_path)

            # 将转换后的文件重命名为原文件名
            os.rename(output_path, input_path)
            print(f"文件转换并替换成功: {input_path}")
        except subprocess.CalledProcessError as e:
            print(f"转换失败: {e}")

    # 插件卸载时触发
    def __del__(self):
        pass
