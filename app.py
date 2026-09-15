import streamlit as st

st.set_page_config(
    page_title="CropGuard — AI Agriculture Diagnostics",
    page_icon="🌱",
    layout="centered"
)

# Custom Styling with Clickable Card Links
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
    
    /* Clickable Link Cards Styling */
    .feature-link {
        text-decoration: none !important;
        color: inherit !important;
        display: block;
    }
    
    .feature-card {
        background-color: white;
        padding: 18px;
        border-radius: 10px;
        border-left: 6px solid #0D9488;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 16px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        cursor: pointer;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(13, 148, 136, 0.15);
        border-left-color: #0F766E;
    }

    .feature-card h4 {
        margin: 0 0 8px 0;
        color: #0F766E;
        font-size: 1.15em;
    }

    .feature-card p {
        margin: 0;
        color: #475569;
        font-size: 0.95em;
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

# Researcher Info
st.markdown("""
<div style="background-color: #EFF6FF; padding: 12px 16px; border-radius: 8px; border: 1px solid #BFDBFE; margin-bottom: 20px;">
    <b>👨‍🔬 Project Lead & Research Director:</b> Muhammad Faheem (Graduate in Biological Sciences)<br/>
    <b>🎯 Mission:</b> Empowering local farmers with instant AI plant pathology, localized chemical/biological treatment plans, and multilingual voice assistance.
</div>
""", unsafe_allow_html=True)

st.subheader("🚀 Choose a Feature (Click any option)")

# Clickable Feature Cards
st.markdown("""
<a href="/Detect_Disease" target="_self" class="feature-link">
    <div class="feature-card">
        <h4>🔍 1. Detect Disease & Audio Guide ➔</h4>
        <p>Upload a leaf image for diagnosis, local spray recommendations, downloadable PDF report, and voice notes.</p>
    </div>
</a>

<a href="/Contribute_Data" target="_self" class="feature-link">
    <div class="feature-card">
        <h4>🌾 2. Contribute Data ➔</h4>
        <p>Submit crop samples with location details to support agricultural pathology research.</p>
    </div>
</a>

<a href="/Disease_Forecast" target="_self" class="feature-link">
    <div class="feature-card">
        <h4>🌤️ 3. Weather & Disease Forecast ➔</h4>
        <p>Get live weather updates and automatic fungal outbreak warnings for your city.</p>
    </div>
</a>

<a href="/Disease_Database" target="_self" class="feature-link">
    <div class="feature-card">
        <h4>📖 4. Crop Disease Database ➔</h4>
        <p>Search standard reference records, symptoms, and treatment protocols.</p>
    </div>
</a>

<a href="/Account" target="_self" class="feature-link">
    <div class="feature-card">
        <h4>👤 5. Farmer Account Portal ➔</h4>
        <p>Log in or create an account to manage your submissions and track contributions.</p>
    </div>
</a>
""", unsafe_allow_html=True)

st.divider()

# Direct Button Navigation (Alternative Quick Actions)
st.subheader("⚡ Quick Action Buttons")
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Open Disease Detector", type="primary", use_container_width=True):
        st.switch_page("pages/1_Detect_Disease.py")
    if st.button("🌤️ Open Disease Forecast", use_container_width=True):
        st.switch_page("pages/7_Disease_Forecast.py")

with col2:
    if st.button("🌾 Contribute Sample Data", use_container_width=True):
        st.switch_page("pages/2_Contribute_Data.py")
    if st.button("📖 Search Disease Database", use_container_width=True):
        st.switch_page("pages/3_Disease_Database.py")

st.divider()
st.caption("© 2026 CropGuard AI Platform — Developed by Muhammad Faheem | Biological Sciences & AgriTech Research")
