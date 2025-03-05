import time
import asyncio


import os
import requests
import httpx
import logging
import re
from queue import Queue, Empty
from mirai import Image, MessageChain,Plain,Voice,Plain
import numpy
import json
import wave
from pydub import AudioSegment
import pyaudio
from audio_separator.separator import Separator
import subprocess
from graiax import silkcoder
import torch
token = 'xqm8k0vw6cvlapuboxveg51fy6ypus'  # 请将这里的'YOUR_TOKEN'替换为你实际获取的token
cookie = ""  # 请将这里的'YOUR_COOKIE'替换为你实际获取的cookie
# cookie = "MUSIC_A_T=1530460507262; MUSIC_R_T=1530460560810; WEVNSM=1.0.0; ntes_utid=tid._.Ki6xp1srQ01BRhEURReRw%252BbuQt8E7ywR._.0; WM_TID=K%2BR1KH6XMtdFRUBARVKUxufqQsoSEx4c; __snaker__id=Q6dpCLdOzKrD4Q8l; ntes_kaola_ad=1; MUSIC_U=00EF144CEBBADDEEAEAEF007AA91772EF3A5333EAEAE668B6AE686DB0DE0047939ADA85FFCE3C4A1790E953A39DF3200743E82CD9BE6E6921EE4DE82A3B2CE5DDAF9F8EEBC0B74719FA0184195229661999811E62D1F02D5A16126EFBF55D43A17490C61B50CE1A872528C380E50C0C07A8B77B77119AFD0F3CB7DD38C499B84526E892E350AE7F00F6D05481789DB245F5CB8608BAD2A44C9AAB3DE31E329C696C91930D5C2489E2E8CEC253562A0F42F6816271F4F2FE4BE2169BB2F36DDD94824375DA04C0FBB9F9AB6CD34185D6E3D620AA420BFD3729189AA48F12E2964849D1F379831E0972F6E677724895E292073890101880D3EA07294BF5A158E82F794075B550609A7FD23B09C918C34B00876E3387E47C9BC8478798E6CC1643503FCF7697A232C21A6E4A90E4C1F0E9CD7FFE6943ACBB1B8BACB4716649B06CE88920E94F9C15B43FB7EDE1606FAE46EFAFC994C3264EC488B9DFEF36EFFA0C71EBD9D3C1A90D70EC35973A5EA780CCBA6; __remember_me=true; _iuqxldmzr_=32; Qs_lvt_382223=1729659434; _ga=GA1.1.1827349827.1729659438; _clck=157rtwz%7C2%7Cfq9%7C0%7C1757; Qs_pv_382223=242568461296104060%2C3639316680175065600%2C1385077227331153700%2C1648293200579800000%2C1844064905126289700; _ga_C6TGHFPQ1H=GS1.1.1729665682.2.1.1729665683.0.0.0; NMTID=00Ouy-pAgHxl_qSZk1fvJLKyTYaB7sAAAGUhOPEog; _ntes_nnid=9cc4f49323cb65cc46edd1f0944279ed,1737396306891; _ntes_nuid=9cc4f49323cb65cc46edd1f0944279ed; WNMCID=kfqbit.1737396308198.01.0; sDeviceId=YD-E%2FlZUDXLzC5AVlAFQAeVh%2BO7E45EqixJ; __csrf=c4df95f69a8ce19848500778adc9a0f1; __csrf=c4df95f69a8ce19848500778adc9a0f1; JSESSIONID-WYYY=%2BE0f5%5C0Rv7o02vot0bKMOJFV%2BNZXTWbTOI7bglxuYBR13r1PoAgw2dnsv2ziuArZ7Fm2gE9NGKOKTCbV%2B71nzUJppZQIfkGBpJuq1O5HnprHib8ir9jzlgGbk4x9TYhSq0XlXBqNvweP0ph72X7qafZVBjc2aJ6SJ1Yac2HB25FAO0Pa%3A1740846924031; WM_NI=cIycOSFt3DhNvxZ7sS8Mcchf%2FdKjMUySh7VpM5SkVzwgviHY3hUIkQScpC%2BfVpC%2B2hlKCZYV37TP5NSpsZxUpFkVP8kMp5JC%2FGcq5AWYOmoYawh5fCVNG7nOWMQg76pdM1E%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb7d43d979dfbb7e145f8b48aa6d54a978a8eadd752ab969682b24485a698d9f02af0fea7c3b92aa197b784ce5986acfda5eb46b6a896d8f259fc93ad84eb6eedbc858bd05fbb8da8d8d57c8feb9d8cd572b5b9ba8acb53f1b89baaea5b91bdc0a4aa6e96b08dccb164b0958dbbdc5ef1e99cb1b84691b0bdbbfb5fb49aa5b7d334a993c0d6c949ed99ad92b84b9587818eee53a3a9a8d6e549969289d8ed4595939f88b63eb4bc83d2c837e2a3"  # 请将这里的'YOUR_COOKIE'替换为你实际获取的cookie
RVC_logs_path = r"D:\AI\AIvoice\RVC1006Nvidia\logs"  # 请将这里的"F:\RVC\RVC1006Nvidia\logs"替换为你部署的RVC项目的logs文件夹的路径
if os.getenv('PATH').find('ffmpeg') == -1:
    os.environ['PATH'] += ';D:\\AI\\ffmpeg\\bin'
def send_request(model_name,file_path, music_name,f0up, port=1145):
    url = f"http://localhost:{port}/wav2wav"
    # 准备请求参数
    data = {
        "audio_path": file_path,  # 直接传入文件路径
        "tran": f0up,               # 可以根据需要调整音调
        "spk": model_name,               # 可以根据需要指定说话人
        "wav_format": "wav"      # 输出格式
    }
    try:
        # 发送POST请求
        response = requests.post(url, data=data)
        response.raise_for_status()
        
        # 保存响应内容为.wav文件
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "music")
        output_file_path = os.path.join(dir_path, f"临时干声{music_name}.wav")
        
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
    dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "music")
    output_file_path = os.path.join(dir_path, f"临时干声{music_name}_{model_name}.wav")
    try:
        with open(output_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # 过滤保持活跃的块
                    f.write(chunk)
        print(f"文件已保存到: {output_file_path}")
    except IOError as e:
        print(f"保存文件失败: {e}")
        return None
    return output_file_path
if __name__ == "__main__":
    model_name='jelee'
    file_path=r'D:\AI\AIchatbot\QChatGPT\plugins\LangBot_RVC_Music\music\Love Song 方大同_(Vocals)_model_bs_roformer_ep_368_sdr_12_(Vocals)_5_HP-Karaoke-UVR_(No Reverb)_UVR-DeEcho-DeReverb.wav'
    music_name='Love Song'
    f0up=0
    send_request(model_name,file_path, music_name,f0up)