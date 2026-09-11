import requests
import streamlit as st

MODEL_ID = "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
HF_ENDPOINT = f"https://api-inference.huggingface.co/models/{MODEL_ID}"


def detect_disease(image_bytes, content_type="image/jpeg"):
    """Send image bytes to a pretrained plant disease model and return predictions."""
    token = st.secrets.get("hf_api_token")
    if not token:
        raise ValueError("Hugging Face token missing. Add hf_api_token in .streamlit/secrets.toml")

    response = requests.post(
        HF_ENDPOINT,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": content_type,
        },
        data=image_bytes,
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Model request failed: {response.text}")

    return response.json()
