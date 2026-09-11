import streamlit as st
import firebase_admin
from firebase_admin import credentials, storage, firestore


def _init_app():
    if not firebase_admin._apps:
        service_account_info = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(
            cred,
            {"storageBucket": st.secrets["firebase_storage_bucket"]},
        )
    return firebase_admin.get_app()


def get_bucket():
    _init_app()
    return storage.bucket()


def get_db():
    _init_app()
    return firestore.client()


def upload_sample(file_bytes, file_name, content_type, crop_name, disease_label):
    bucket = get_bucket()
    blob = bucket.blob(f"samples/{file_name}")
    blob.upload_from_string(file_bytes, content_type=content_type)
    blob.make_public()

    db = get_db()
    db.collection("samples").add(
        {
            "cropName": crop_name,
            "diseaseLabel": disease_label,
            "imageUrl": blob.public_url,
        }
    )
    return blob.public_url
