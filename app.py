import base64
import streamlit as st

# Page config must be the very first Streamlit command
st.set_page_config(page_title="CropGuard", page_icon="🌾", layout="centered")

# Inline Base64 Banner Code (Muhammad Faheem Image)
BANNER_HTML = """
<div style="width: 100%; border-radius: 10px; overflow: hidden; margin-bottom: 25px;">
    <img src="https://i.ibb.co/6R2S38s/hero-banner.png" style="width: 100%; height: auto; display: block;" alt="Muhammad Faheem - CropGuard Banner">
</div>
"""

# Alternative via Direct File Embed (Safe fallback protection)
def load_embedded_banner():
    # Render direct banner styling
    st.markdown(
        """
        <style>
        .banner-img {
            width: 100%;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

load_embedded_banner()

# Attempt to load local/cloud image, fallback gracefully
try:
    st.image("assets/hero-banner.png", use_container_width=True)
except Exception:
    # If file isn't uploaded yet, show stylized header card
    st.info("💡 **Developer Note:** Photo ko `assets/hero-banner.png` par upload karein. App layout ready hai.")

# Header Section
st.title("🌾 CropGuard")
st.subheader("Spot crop disease early, before it spreads across the field.")

st.write(
    """
    Upload a photo of an affected leaf and get an instant diagnosis.
    Every contribution also helps build an open dataset for researchers
    working on crop health.
    """
)

# Navigation Links
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.page_link("pages/1_Detect_Disease.py", label="🔍 Detect a disease")
with col2:
    st.page_link("pages/2_Contribute_Data.py", label="📤 Contribute a sample")
with col3:
    st.page_link("pages/3_Disease_Database.py", label="🌍 Browse database")
with col4:
    st.page_link("pages/5_Account.py", label="👤 My account")
with col5:
    st.page_link("pages/7_Disease_Forecast.py", label="🌤️ Weather forecast")

st.divider()

# Information Grid
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**For farmers**")
    st.caption("Take a photo of a sick leaf and get a likely diagnosis in seconds.")
with c2:
    st.markdown("**For researchers**")
    st.caption("Access a growing, labeled dataset of crop images from real fields.")
with c3:
    st.markdown("**For the data**")
    st.caption("Every contribution builds a global picture of crop health over time.")
