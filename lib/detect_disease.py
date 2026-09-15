import os
import base64
import requests
import streamlit as st
from gtts import gTTS
import io

def get_plant_id_api_key():
    return st.secrets.get("PLANT_ID_API_KEY", "xvkwB969s2vmuUinWlphpe4P4XKSAEUxvQ9hlcBtsWohj420rd")

def analyze_crop_image(image_bytes):
    """
    Sends crop leaf image to Plant.id v3 API for high-accuracy disease diagnosis.
    """
    api_key = get_plant_id_api_key()
    if not api_key:
        st.error("⚠️ Plant.id API Key is missing in Streamlit Secrets.")
        return None

    # Encode image to Base64 format required by Plant.id API
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    url = "https://plant.id/api/v3/health_assessment"
    headers = {
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "images": [f"data:image/jpeg;base64,{encoded_image}"],
        "latitude": 31.5204,
        "longitude": 74.3587,
        "similar_images": True
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code == 201 or response.status_code == 200:
            return response.json()
        else:
            st.error(f"Plant.id API Error ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Network error contacting Plant.id API: {e}")
        return None

def generate_voice_note(text, lang='ur'):
    """Generates Urdu/English voice note using gTTS"""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception:
        return None
