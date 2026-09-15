import os
import streamlit as st
import pandas as pd
from PIL import Image

# 1. Page Configuration (Responsive & Clean)
st.set_page_config(
    page_title="CropGuard - Smart Plant Health",
    page_icon="🌾",
    layout="centered", # Touch devices par behtar dikhta hai
    initial_sidebar_state="collapsed"
)

# Custom CSS for Big Touch Controls & Better Spacing
st.markdown("""
    <style>
    /* Touch friendly big buttons */
    .stButton>button {
        width: 100%;
        height: 3.5rem;
        font-size: 1.2rem !important;
        font-weight: bold;
        border-radius: 12px;
    }
    /* Better spacing for mobile screens */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Header / Hero Banner
hero_path = "assets/hero-banner.png"
if os.path.exists(hero_path):
    st.image(hero_path, use_container_width=True)
else:
    st.title("🌾 CropGuard")

st.markdown("### 🌿 Fasal Ki Bimari Ki Pehchan Karein")
st.caption("Aapni fasal ki tasveer upload karein aur fawri elaj paayein.")

st.divider()

# 3. Touch-Friendly Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📸 Detect Disease", "📖 Database", "👤 Account"])

# --- TAB 1: Disease Detection ---
with tab1:
    st.subheader("Tasveer Upload Karein")
    
    # Touch Input Option: File Upload or Camera
    input_method = st.radio(
        "Zariya chunein:", 
        ["📂 File Upload", "📷 Camera Capture"], 
        horizontal=True
    )
    
    uploaded_image = None
    if input_method == "📂 File Upload":
        uploaded_image = st.file_uploader("Fasal ki tasveer chunien", type=["jpg", "jpeg", "png"])
    else:
        uploaded_image = st.camera_input("Tasveer kheenchein")

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Aap ki tasveer", use_container_width=True)
        
        # Large Touch Action Button
        if st.button("🔍 Check Bimari (Analyze)", type="primary"):
            with st.spinner("Bimari ki ਜਾਂਚ ho rahi hai..."):
                # Simulated detection logic
                st.success("✅ Pehchan Mukammal!")
                
                st.markdown("""
                ---
                ### 📊 Nateeja (Result):
                * **Fasal:** Wheat (Gandum)
                * **Bimari:** Leaf Rust
                * **Confidence:** 94%
                
                💉 **Tajweez Karda Elaj:**  
                Fawri tor par munasib fungicide ka spray karein aur pani ki miqdar ko munasib rakhein.
                ---
                """)

# --- TAB 2: Quick Database Lookup ---
with tab2:
    st.subheader("📖 Disease Database")
    
    db_path = "data/disease_database.csv"
    if os.path.exists(db_path):
        try:
            df = pd.read_csv(db_path)
            st.dataframe(df, use_container_width=True)
        except Exception:
            st.warning("CSV File parhne mein masla hai.")
    else:
        st.info("Database file filhal mojood nahi hai.")

# --- TAB 3: Simple User Account ---
with tab3:
    st.subheader("👤 User Profile")
    st.text_input("Aapka Naam / Name")
    st.text_input("Mobile Number")
    
    if st.button("Save Profile"):
        st.toast("Profile successfully save ho gayi hai! 🎉")
