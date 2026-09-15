import requests
import streamlit as st

def upload_image_to_cloudinary(image_bytes):
    cloud_name = st.secrets.get("cloudinary_cloud_name")
    upload_preset = st.secrets.get("cloudinary_upload_preset")
    
    if not cloud_name or not upload_preset:
        st.error("Cloudinary secrets are missing in secrets.toml")
        return None
        
    url = f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload"
    files = {"file": image_bytes}
    data = {"upload_preset": upload_preset}
    
    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            return response.json().get("secure_url")
        else:
            st.error(f"Cloudinary upload failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Cloudinary Exception: {str(e)}")
        return None
