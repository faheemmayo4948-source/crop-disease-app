import os
import streamlit as st

def get_all_samples():
    """
    Fetches samples from Firebase Firestore if configured,
    or returns sample demo data for research review.
    """
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore

        if not firebase_admin._apps:
            # Check secrets for Firebase config
            if "firebase" in st.secrets:
                cred_dict = dict(st.secrets["firebase"])
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
            else:
                st.warning("⚠️ Firebase credentials missing in Streamlit Secrets. Showing local sample data.")
                return get_demo_samples()

        db = firestore.client()
        docs = db.collection("crop_samples").stream()
        
        samples = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            samples.append(data)
            
        return samples if samples else get_demo_samples()

    except Exception as e:
        # Fallback to demo dataset if Firebase is not yet configured
        return get_demo_samples()

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
        },
        {
            "id": "sample_003",
            "crop_name": "Cotton",
            "disease_name": "Cotton Leaf Curl Virus",
            "farmer_name": "Tariq Mahmood",
            "phone": "+923025551234",
            "consent_granted": False,
            "latitude": 30.1575,
            "longitude": 71.5249,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Cotton_plant_disease.jpg/640px-Cotton_plant_disease.jpg",
            "user_email": "farmer3@example.com"
        }
    ]
