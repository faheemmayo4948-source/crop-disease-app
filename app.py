import os
import sys
import streamlit as st

# Setup ROOT directory path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

st.set_page_config(
    page_title="CropGuard · Smart Agriculture",
    page_icon="🌾",
    layout="wide"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        color: #2E7D32;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #4CAF50;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Safe Hero Banner Rendering (Only if image file exists)
banner_path = os.path.join(ROOT_DIR, "assets", "hero-banner.png")
if os.path.exists(banner_path):
    st.image(banner_path, use_container_width=True)

st.markdown('<h1 class="main-title">🌾 CropGuard Platform</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">AI-driven Crop Disease Detection & Climate Advisory</p>', unsafe_allow_html=True)

st.info("👋 **Welcome to CropGuard!** Select a feature below or use the sidebar menu to navigate.")

# Interactive Quick Navigation Buttons
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔍 AI Diagnostics")
    st.write("Upload leaf photos to instantly detect pathogens and receive treatment guidance.")
    st.page_link("pages/1_Detect_Disease.py", label="Go to Disease Detection ➔", icon="🔍")

    st.subheader("📚 Knowledge Base")
    st.write("Explore symptoms, remedies, and treatment advice for various crop diseases.")
    st.page_link("pages/3_Disease_Database.py", label="Open Disease Database ➔", icon="📚")

with col2:
    st.subheader("🌤️ Weather & Risk Forecast")
    st.write("Check local weather conditions and disease risk alerts.")
    st.page_link("pages/2_Weather_Risk.py", label="View Weather Forecast ➔", icon="🌤️")

    st.subheader("👤 Farmer Portal")
    st.write("Log in to manage your field history or request password resets.")
    st.page_link("pages/5_Account.py", label="Access Farmer Account ➔", icon="👤")
