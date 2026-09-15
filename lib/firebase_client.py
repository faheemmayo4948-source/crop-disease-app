import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

def init_firebase():
    if not firebase_admin._apps:
        service_account_info = dict(st.secrets["firebase_service_account"])
        # Fix private key formatting issue in Streamlit secrets
        if "private_key" in service_account_info:
            service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred)

def get_db():
    init_firebase()
    return firestore.client()

def save_sample(sample_data):
    try:
        db = get_db()
        sample_data["timestamp"] = datetime.utcnow().isoformat()
        db.collection("samples").add(sample_data)
        return True
    except Exception as e:
        st.error(f"Firestore Save Error: {str(e)}")
        return False

def fetch_all_samples():
    try:
        db = get_db()
        docs = db.collection("samples").stream()
        samples = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            samples.append(data)
        return samples
    except Exception as e:
        st.error(f"Firestore Fetch Error: {str(e)}")
        return []

def fetch_user_samples(user_id):
    try:
        db = get_db()
        docs = db.collection("samples").where("user_id", "==", user_id).stream()
        samples = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            samples.append(data)
        return samples
    except Exception as e:
        st.error(f"User Samples Fetch Error: {str(e)}")
        return []
