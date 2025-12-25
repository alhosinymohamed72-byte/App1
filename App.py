import streamlit as st
import torch
import torchaudio
from demucs.apply import apply_model
from demucs.pretrained import get_model
import os
import subprocess
import shutil
import time
import yt_dlp

# إعداد الصفحة
st.set_page_config(page_title="عازل الموسيقى الذكي", page_icon="🎵")

# دالة تحميل الموديل (تخزين مؤقت لتسريع التطبيق)
@st.cache_resource
def load_demucs_model():
    return get_model("htdemucs_6s").to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

def download_video(url, cookies_content):
    output_path = "input_file.mp4"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    if cookies_content:
        with open("cookies.txt", "w") as f:
            f.write(cookies_content)
        ydl_opts['cookiefile'] = "cookies.txt"
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

# واجهة المستخدم
st.title("🎵 عازل الموسيقى الاحترافي")
st.markdown("ارفع ملفك أو ضع رابط يوتيوب لفصل الموسيقى عن الصوت.")

tab1, tab2 = st.tabs(["🔗 رابط", "📂 رفع ملف"])

source_path = None

with tab1:
    url = st.text_input("ضع رابط المقطع هنا")
with tab2:
    uploaded_file = st.file_uploader("اختر ملف صوت أو فيديو", type=["mp3", "wav", "mp4", "m4a"])

quality = st.select_slider("جودة الفصل", options=["أسرع", "أدق"])

if st.button("🚀 ابدأ المعالجة"):
    try:
        if url:
            with st.spinner("جارٍ جلب المقطع..."):
                # جلب الكوكيز من Secrets الخاصة بـ Streamlit
                cookies = st.secrets.get("coce", "")
                source_path = download_video(url, cookies)
        elif uploaded_file:
            source_path = uploaded_file.name
            with open(source_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        if source_path:
            with st.spinner("جارٍ فصل الموسيقى بالذكاء الاصطناعي..."):
                model = load_demucs_model()
                # (هنا نضع نفس منطق Demucs السابق للمعالجة)
                # ...
                st.success("اكتملت العملية!")
                st.audio("vocals.mp3") # مثال للنتيجة
    except Exception as e:
        st.error(f"خطأ: {e}")
