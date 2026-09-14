import base64
import requests
import streamlit as st

def detect_disease(image_bytes: bytes, content_type: str = "image/jpeg", latitude: float = None, longitude: float = None):
    """
    Sends image to Plant.id API v3 for high-accuracy disease diagnosis and treatment tips.
    """
    api_key = st.secrets.get("PLANT_ID_API_KEY", "")
    if not api_key:
        st.warning("⚠️ PLANT_ID_API_KEY missing in Streamlit Secrets!")
        return []

    url = "https://plant.id/api/v3/health_assessment"
    
    # Base64 encode leaf image
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    headers = {
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "images": [f"data:{content_type};base64,{encoded_image}"],
        "latitude": latitude or 31.5204,
        "longitude": longitude or 74.3587,
        "similar_images": True
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=25)
        if response.status_code == 201 or response.status_code == 200:
            data = response.json()
            suggestions = data.get("result", {}).get("disease", {}).get("suggestions", [])
            
            parsed_results = []
            for item in suggestions[:3]:
                disease_name = item.get("name", "Unknown Disease")
                probability = item.get("probability", 0.0)
                details = item.get("details", {})
                treatment = details.get("treatment", {})
                
                # Extract biological/chemical/prevention treatments if available
                biological = treatment.get("biological", [])
                chemical = treatment.get("chemical", [])
                prevention = treatment.get("prevention", [])

                parsed_results.append({
                    "label": disease_name,
                    "score": probability,
                    "description": details.get("description", "No details available."),
                    "treatment_biological": biological,
                    "treatment_chemical": chemical,
                    "prevention": prevention
                })
            return parsed_results
        else:
            st.error(f"Plant.id API Error Status: {response.status_code}")
    except Exception as e:
        st.error(f"Failed to reach Plant.id API: {e}")

    return []
