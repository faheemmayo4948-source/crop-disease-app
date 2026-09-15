import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st

try:
    from lib.firebase_client import save_sample
except ModuleNotFoundError:
    st.error("⚠️ Could not import `lib.firebase_client`. Please update `lib/firebase_client.py` in your GitHub repo.")
    st.stop()

st.set_page_config(page_title="Contribute Data · CropGuard", page_icon="🌾", layout="centered")

st.title("🌾 Contribute Crop Disease Sample")
st.write("Help expand our open-access agricultural pathology dataset for scientific research.")

crop_name = st.text_input("Crop Name (e.g., Wheat, Rice, Cotton):")
disease_name = st.text_input("Observed Symptoms / Disease Name (Optional):")
farmer_name = st.text_input("Your Name / Contributor Name:")
phone = st.text_input("Contact Number (Optional):")

uploaded_img = st.file_uploader("Upload Leaf Sample Image:", type=["jpg", "jpeg", "png"])

col1, col2 = st.columns(2)
with col1:
    lat = st.number_input("Latitude (Optional):", value=0.0, format="%.4f")
with col2:
    lon = st.number_input("Longitude (Optional):", value=0.0, format="%.4f")

consent_granted = st.checkbox("I consent to sharing this data for research and AI model training purposes.", value=True)

if st.button("Submit Sample", type="primary"):
    if not crop_name:
        st.error("Please specify the Crop Name before submitting.")
    elif not consent_granted:
        st.warning("Consent is required to include your sample in the research database.")
    else:
        with st.spinner("Saving sample submission..."):
            success = save_sample(
                crop_name=crop_name,
                disease_name=disease_name,
                farmer_name=farmer_name,
                phone=phone,
                consent_granted=consent_granted,
                lat=lat if lat != 0.0 else None,
                lon=lon if lon != 0.0 else None,
                image_file=uploaded_img
            )
            if success:
                st.success("🎉 Thank you! Your crop sample has been successfully recorded in the dataset.")
