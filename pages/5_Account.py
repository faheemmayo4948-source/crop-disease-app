import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from lib.auth_client import login_user, signup_user

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
                    else:
                        st.error("Invalid email or password.")

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
                    else:
                        st.error("Signup failed. Email might already be in use.")
