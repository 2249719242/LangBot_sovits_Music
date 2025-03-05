import io

import numpy as np
import soundfile
from flask import Flask, request, send_file
import torchaudio
import torch
from inference import infer_tool, slicer

app = Flask(__name__)



@app.route("/wav2wav", methods=["POST"])
def wav2wav():
    request_form = request.form
    audio_path = request_form.get("audio_path", None)  # wav文件地址
    tran = int(float(request_form.get("tran", 0)))  # 音调
    spk = request_form.get("spk", 0)  # 说话人(id或者name都可以,具体看你的config)
    if spk=='liyi':
        model_name = "models/G_56800.pth"  # 模型地址
        config_name = "configs/config.json"  # config地址
        diffusion_path="models/diffusion/model_7000.pt"
        # svc_model = infer_tool.Svc(model_name, config_name,diffusion_model_path=diffusion_path)
    if torch.cuda.is_available():
        torch.cuda.empty_cache()  # 清空CUDA缓存
    svc_model = infer_tool.Svc(model_name, config_name,diffusion_model_path=diffusion_path)
    # 初始化音频重采样转换器
    svc_model = infer_tool.Svc(model_name, config_name,diffusion_model_path=diffusion_path)
    svc_model.audio16k_resample_transform = torchaudio.transforms.Resample(
        svc_model.target_sample, 16000).to(svc_model.dev)
    svc_model.audio_resample_transform = torchaudio.transforms.Resample(
        svc_model.target_sample, svc_model.target_sample).to(svc_model.dev)    
    wav_format = request_form.get("wav_format", 'wav')  # 范围文件格式
    # 添加切片相关参数
    slice_db = -40      # 切片的音量阈值，可以调整，值越大切片越多
    pad_seconds = 0.3   # 减小填充时间
    clip_seconds = 10   # 强制按固定时长切片，这是最关键的参数



    infer_tool.format_wav(audio_path)
    chunks = slicer.cut(audio_path, db_thresh=-40)
    audio_data, audio_sr = slicer.chunks2audio(audio_path, chunks)

    # 使用slice_inference方法替代原来的处理逻辑
    audio = svc_model.slice_inference(
        raw_audio_path=audio_path,
        spk=spk,
        tran=tran,
        slice_db=slice_db,
        cluster_infer_ratio=0,
        auto_predict_f0=False,
        noice_scale=0.4,
        pad_seconds=pad_seconds,
        clip_seconds=clip_seconds,  # 使用clip_seconds进行切片
        lg_num=0,
        lgr_num=0.75
    )
    # 输出处理
    out_wav_path = io.BytesIO()
    soundfile.write(out_wav_path, audio, svc_model.target_sample, format=wav_format)
    out_wav_path.seek(0)
    svc_model.clear_empty()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()  # 清空CUDA缓存
    return send_file(out_wav_path, download_name=f"temp.{wav_format}", as_attachment=True)
if __name__ == '__main__':
    app.run(port=1145, host="0.0.0.0", debug=False, threaded=False)



