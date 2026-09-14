import base64
import requests
import streamlit as st

def detect_disease(image_bytes: bytes, content_type: str = "image/jpeg", latitude: float = None, longitude: float = None):
    """
    Sends image to Plant.id API v3 requesting detailed treatment & prevention information.
    """
    api_key = st.secrets.get("PLANT_ID_API_KEY", "")
    if not api_key:
        st.warning("⚠️ PLANT_ID_API_KEY missing in Streamlit Secrets!")
        return []

    url = "https://plant.id/api/v3/health_assessment"
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    headers = {
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }

    # Added explicit details parameters for treatment data fetching
    payload = {
        "images": [f"data:{content_type};base64,{encoded_image}"],
        "latitude": latitude or 31.5204,
        "longitude": longitude or 74.3587,
        "similar_images": True,
        "health": "all"
    }

    # Parameters to force API to send full treatment and description data
    params = {
        "details": "cause,common_names,description,treatment,type,url"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, params=params, timeout=25)
        if response.status_code in [200, 201]:
            data = response.json()
            suggestions = data.get("result", {}).get("disease", {}).get("suggestions", [])
            
            parsed_results = []
            for item in suggestions[:3]:
                disease_name = item.get("name", "Unknown Disease")
                probability = item.get("probability", 0.0)
                details = item.get("details", {}) or {}
                treatment = details.get("treatment", {}) or {}
                
                parsed_results.append({
                    "label": disease_name,
                    "score": probability,
                    "description": details.get("description", {}).get("value", "No description available.") if isinstance(details.get("description"), dict) else details.get("description", "No description available."),
                    "treatment_biological": treatment.get("biological", []),
                    "treatment_chemical": treatment.get("chemical", []),
                    "prevention": treatment.get("prevention", [])
                })
            return parsed_results
        else:
            st.error(f"Plant.id API Error Status: {response.status_code}")
    except Exception as e:
        st.error(f"Failed to reach Plant.id API: {e}")

    return []
