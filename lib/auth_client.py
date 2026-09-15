import os
import requests
import streamlit as st

def get_firebase_api_key():
    if "FIREBASE_API_KEY" in st.secrets:
        return st.secrets["FIREBASE_API_KEY"]
    return os.getenv("FIREBASE_API_KEY", "AIzaSyAYJIJdsqMMaSegPxGj5-XGVoWPfgX5d6E")

def login_user(email, password):
    api_key = get_firebase_api_key()
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}

    try:
        response = requests.post(url, json=payload, timeout=10)
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
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}

    try:
        response = requests.post(url, json=payload, timeout=10)
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

def reset_password(email):
    """Firebase Identity Toolkit API ke zariye Password Reset Link bhejta hai"""
    api_key = get_firebase_api_key()
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        res_data = response.json()
        if response.status_code == 200:
            return True, "Password reset email sent! Please check your inbox/spam folder."
        else:
            error_msg = res_data.get("error", {}).get("message", "Failed to send reset link.")
            if error_msg == "EMAIL_NOT_FOUND":
                error_msg = "Is email par koi account majood nahi hai."
            return False, error_msg
    except Exception as e:
        return False, f"Network error: {e}"
