import requests
import streamlit as st

MODEL_ID = "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"

def predict_crop_disease(image_bytes):
    hf_token = st.secrets.get("hf_api_token")
    headers = {}
    if hf_token:
        headers["Authorization"] = f"Bearer {hf_token}"
        
    try:
        response = requests.post(API_URL, headers=headers, data=image_bytes)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Hugging Face API Error ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Inference Exception: {str(e)}")
        return None
