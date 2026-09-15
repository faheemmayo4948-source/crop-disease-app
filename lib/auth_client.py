import os
import requests
import streamlit as st

def get_firebase_api_key():
    # Fetch API Key from Streamlit Secrets or Environment Variables
    return st.secrets.get("FIREBASE_API_KEY", os.getenv("FIREBASE_API_KEY", ""))

def login_user(email, password):
    api_key = get_firebase_api_key()
    if not api_key:
        st.error("⚠️ Firebase API Key missing in Streamlit Secrets.")
        return None

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}

    try:
        response = requests.post(url, json=payload)
        res_data = response.json()
        if response.status_code == 200:
            return {"email": res_data.get("email"), "idToken": res_data.get("idToken"), "localId": res_data.get("localId")}
        else:
            error_msg = res_data.get("error", {}).get("message", "Authentication failed.")
            st.error(f"Login Error: {error_msg}")
            return None
    except Exception as e:
        st.error(f"Network error during login: {e}")
        return None

def signup_user(email, password):
    api_key = get_firebase_api_key()
    if not api_key:
        st.error("⚠️ Firebase API Key missing in Streamlit Secrets.")
        return None

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}

    try:
        response = requests.post(url, json=payload)
        res_data = response.json()
        if response.status_code == 200:
            return {"email": res_data.get("email"), "localId": res_data.get("localId")}
        else:
            error_msg = res_data.get("error", {}).get("message", "Signup failed.")
            st.error(f"Signup Error: {error_msg}")
            return None
    except Exception as e:
        st.error(f"Network error during signup: {e}")
        return None
