import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore


def _init_app():
    if not firebase_admin._apps:
        service_account_info = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred)
    return firebase_admin.get_app()


def get_db():
    _init_app()
    return firestore.client()


def save_sample(crop_name, disease_label, image_url, farmer_uid=None, farmer_email=None):
    db = get_db()
    db.collection("samples").add(
        {
            "cropName": crop_name,
            "diseaseLabel": disease_label,
            "imageUrl": image_url,
            "farmerUid": farmer_uid,
            "farmerEmail": farmer_email,
        }
    )
