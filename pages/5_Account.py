import sys
import os

# Root directory path safety
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st

try:
    from lib.auth_client import login_user, signup_user
except ModuleNotFoundError:
    st.error("⚠️ Could not import `lib.auth_client`. Please verify `lib/auth_client.py` exists in your GitHub repository.")
    st.stop()

st.set_page_config(page_title="Farmer Account · CropGuard", page_icon="👤", layout="centered")

st.title("👤 Farmer Account Portal")

if "user" in st.session_state and st.session_state.user:
    user = st.session_state.user
    st.success(f"✅ Logged in as: **{user.get('email')}**")
    
    if st.button("Log Out", type="secondary"):
        st.session_state.user = None
        st.rerun()
else:
    tab1, tab2 = st.tabs(["🔐 Log In", "📝 Sign Up"])

    with tab1:
        st.subheader("Login to Your Account")
        login_email = st.text_input("Email:", key="login_email")
        login_pass = st.text_input("Password:", type="password", key="login_pass")

        if st.button("Log In", type="primary"):
            if not login_email or not login_pass:
                st.error("Please enter both email and password.")
            else:
                with st.spinner("Authenticating..."):
                    user_data = login_user(login_email, login_pass)
                    if user_data:
                        st.session_state.user = user_data
                        st.success("Login successful!")
                        st.rerun()

    with tab2:
        st.subheader("Create a New Farmer Account")
        signup_email = st.text_input("Email:", key="signup_email")
        signup_pass = st.text_input("Password (min 6 characters):", type="password", key="signup_pass")

        if st.button("Create Account", type="primary"):
            if not signup_email or not signup_pass:
                st.error("Please enter both email and password.")
            elif len(signup_pass) < 6:
                st.error("Password must be at least 6 characters long.")
            else:
                with st.spinner("Creating account..."):
                    res = signup_user(signup_email, signup_pass)
                    if res:
                        st.success("Account created successfully! You can now log in.")
