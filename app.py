import streamlit as st

st.set_page_config(
    page_title="CropGuard — AI Agriculture Diagnostics",
    page_icon="🌱",
    layout="centered"
)

# Custom Styling for Clean Professional Look
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    .block-container { padding-top: 2rem !important; max-width: 700px !important; }
    .main-header {
        background: linear-gradient(135deg, #0F766E 0%, #0D9488 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .feature-card {
        background-color: white;
        padding: 18px;
        border-radius: 8px;
        border-left: 5px solid #0D9488;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Main Banner
st.markdown("""
<div class="main-header">
    <h1 style="color: white; margin: 0;">🌱 CropGuard AI</h1>
    <p style="margin-top: 8px; font-size: 1.1em; opacity: 0.9;">
        Smart Agricultural Diagnostics, Weather Risk Analysis & Farmer Research Network
    </p>
</div>
""", unsafe_allow_html=True)

# Researcher & Platform Info
st.markdown("""
<div style="background-color: #EFF6FF; padding: 12px 16px; border-radius: 8px; border: 1px solid #BFDBFE; margin-bottom: 20px;">
    <b>👨‍🔬 Project Lead & Research Director:</b> Muhammad Faheem (Graduate in Biological Sciences)<br/>
    <b>🎯 Mission:</b> Empowering local farmers with instant AI plant pathology, localized chemical/biological treatment plans, and multilingual voice assistance.
</div>
""", unsafe_allow_html=True)

st.subheader("🚀 Platform Capabilities")

st.markdown("""
<div class="feature-card">
    <h4>🔍 1. Instant Disease Detection & Audio Guide</h4>
    <p>Upload a leaf image to get accurate plant disease diagnosis, local market spray dosages, downloadable PDF reports, and <b>Urdu/English voice notes</b> for farmers.</p>
</div>

<div class="feature-card">
    <h4>🌾 2. Farmer Data Contribution & Research Dataset</h4>
    <p>Logged-in farmers can submit geotagged crop samples with ethical consent to help build a comprehensive research database for agri-pathology.</p>
</div>

<div class="feature-card">
    <h4>🌤️ 3. Weather-Based Disease Forecast</h4>
    <p>Get real-time weather analytics and automated fungal/bacterial outbreak warnings based on temperature and relative humidity thresholds.</p>
</div>

<div class="feature-card">
    <h4>📖 4. Crop Disease Knowledge Base</h4>
    <p>Access an extensive reference database covering top crop diseases, scientific pathogen classifications, symptoms, and preventive protocols.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("📌 Quick Navigation")
col1, col2 = st.columns(2)

with col1:
    st.info("🔍 **Detect Disease**\n\nUpload leaf photo for diagnosis and audio guides.")
    st.info("🌤️ **Disease Forecast**\n\nCheck weather-based outbreak risk for your region.")

with col2:
    st.success("🌾 **Contribute Data**\n\nShare sample data to support agricultural research.")
    st.success("📖 **Disease Database**\n\nExplore treatments & scientific symptoms.")

st.divider()
st.caption("© 2026 CropGuard AI Platform — Developed by Muhammad Faheem | Biological Sciences & AgriTech Research")
