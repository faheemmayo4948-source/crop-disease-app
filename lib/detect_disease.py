import base64
import requests
import streamlit as st

PLANT_ID_ENDPOINT = "https://api.plant.id/v2/health_assessment"


def detect_disease(image_bytes, content_type="image/jpeg"):
    api_key = st.secrets.get("plant_id_api_key")
    if not api_key:
        raise ValueError("Plant.id API key missing. Add plant_id_api_key in secrets.")

    encoded_image = base64.b64encode(image_bytes).decode("ascii")

    payload = {
        "images": [encoded_image],
        "modifiers": ["health_all"],
        "disease_details": ["description", "treatment", "common_names"],
    }

    response = requests.post(
        PLANT_ID_ENDPOINT,
        json=payload,
        headers={
            "Content-Type": "application/json",
            "Api-Key": api_key,
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Plant.id request failed: {response.text}")

    data = response.json()
    diseases = data.get("health_assessment", {}).get("diseases", [])

    # Convert Plant.id's format into the same {label, score} shape the app already expects
    predictions = [
        {"label": d.get("name", "Unknown"), "score": d.get("probability", 0)}
        for d in diseases
    ]
    return predictions
