import os
import base64
import requests
import streamlit as st
from gtts import gTTS
import io

def get_plant_id_api_key():
    return st.secrets.get("PLANT_ID_API_KEY", "xvkwB969s2vmuUinWlphpe4P4XKSAEUxvQ9hlcBtsWohj420rd")

def analyze_crop_image(image_bytes, lang="ur"):
    """Sends crop leaf image to Plant.id v3 API with valid API modifiers."""
    api_key = get_plant_id_api_key()
    if not api_key:
        st.error("⚠️ Plant.id API Key is missing in Streamlit Secrets.")
        return None

    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    url = "https://plant.id/api/v3/health_assessment"
    headers = {
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }
    
    # Valid Plant.id v3 payload parameters
    payload = {
        "images": [f"data:image/jpeg;base64,{encoded_image}"],
        "latitude": 31.5204,
        "longitude": 74.3587,
        "health": "all",
        "disease_model": "full",
        "similar_images": True
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            st.error(f"Plant.id API Error ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Network error contacting Plant.id API: {e}")
        return None

def parse_disease_results(api_response):
    """Safely extracts disease suggestions and confidence scores from API output."""
    if not api_response or not isinstance(api_response, dict):
        return []

    result = api_response.get("result", {})
    disease = result.get("disease", {})
    suggestions = disease.get("suggestions", [])

    if not suggestions:
        # Fallback to health_assessment object if nested differently
        health_assessment = result.get("health_assessment", {})
        suggestions = health_assessment.get("diseases", [])

    clean_suggestions = []
    
    if isinstance(suggestions, list):
        for item in suggestions[:3]:
            if isinstance(item, dict):
                name = item.get("name", "Unknown Issue")
                prob = float(item.get("probability", 0.0)) * 100
                details = item.get("details", {})
                
                treatment = {}
                if isinstance(details, dict):
                    treatment = details.get("treatment", {})
                
                clean_suggestions.append({
                    "name": name,
                    "probability": prob,
                    "treatment": treatment,
                    "description": details.get("description", "") if isinstance(details, dict) else ""
                })

    return clean_suggestions

def detect_disease(image_bytes, lang="ur", *args, **kwargs):
    raw_response = analyze_crop_image(image_bytes, lang=lang)
    if raw_response:
        return parse_disease_results(raw_response)
    return []

def generate_voice_note(text, lang='ur'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception:
        return None
