import requests
import streamlit as st

def get_api_key():
    return st.secrets.get("firebase_web_api_key", "")

def sign_up(email, password):
    api_key = get_api_key()
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    return response.json()

def sign_in(email, password):
    api_key = get_api_key()
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    res_data = response.json()
    if "idToken" in res_data:
        st.session_state["user_info"] = res_data
        st.session_state["is_logged_in"] = True
    return res_data

def sign_out():
    st.session_state["user_info"] = None
    st.session_state["is_logged_in"] = False

def is_logged_in():
    return st.session_state.get("is_logged_in", False)

def get_user_info():
    return st.session_state.get("user_info", {})
