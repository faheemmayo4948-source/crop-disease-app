import os
import streamlit as st

def get_demo_samples():
    """Fallback research demo data for Admin Gallery and testing"""
    return [
        {
            "id": "sample_001",
            "crop_name": "Wheat",
            "disease_name": "Leaf Rust",
            "farmer_name": "Muhammad Ali",
            "phone": "+923001234567",
            "consent_granted": True,
            "latitude": 31.5204,
            "longitude": 74.3587,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Puccinia_recondita_1.jpg/640px-Puccinia_recondita_1.jpg",
            "user_email": "farmer1@example.com"
        },
        {
            "id": "sample_002",
            "crop_name": "Rice",
            "disease_name": "Bacterial Leaf Blight",
            "farmer_name": "Ahmad Raza",
            "phone": "+923019876543",
            "consent_granted": True,
            "latitude": 31.8950,
            "longitude": 73.2700,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Xanthomonas_oryzae_pv._oryzae.jpg/640px-Xanthomonas_oryzae_pv._oryzae.jpg",
            "user_email": "farmer2@example.com"
        }
    ]

def get_all_samples():
    """Fetches samples from Firestore or fallback demo data"""
    if "submitted_samples" in st.session_state:
        return st.session_state.submitted_samples + get_demo_samples()
    return get_demo_samples()

def save_sample(crop_name, disease_name, farmer_name, phone, consent_granted, lat=None, lon=None, image_file=None):
    """Saves sample contribution data safely"""
    user_email = "anonymous@farmer.com"
    if "user" in st.session_state and st.session_state.user:
        user_email = st.session_state.user.get("email", user_email)

    sample_data = {
        "crop_name": crop_name,
        "disease_name": disease_name,
        "farmer_name": farmer_name,
        "phone": phone,
        "consent_granted": consent_granted,
        "latitude": lat,
        "longitude": lon,
        "user_email": user_email,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Puccinia_recondita_1.jpg/640px-Puccinia_recondita_1.jpg"
    }

    if "submitted_samples" not in st.session_state:
        st.session_state.submitted_samples = []

    st.session_state.submitted_samples.append(sample_data)
    return True
