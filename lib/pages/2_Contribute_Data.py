import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from PIL import Image
from streamlit_geolocation import streamlit_geolocation
from lib.cloudinary_client import upload_image_to_cloudinary
from lib.firebase_client import save_sample

st.set_page_config(page_title="Contribute Data · CropGuard", page_icon="🌾", layout="centered")

st.title("🌾 Contribute Crop Data")
st.write("Help us build a comprehensive research database. Your sample data will aid agri-researchers and local farmers.")

if not st.session_state.get("user"):
    st.warning("🔒 Please login via the Account page to submit data samples.")
    st.stop()

with st.form("contribute_form"):
    crop_name = st.text_input("Crop Name (e.g., Wheat, Cotton, Rice):")
    disease_name = st.text_input("Observed Disease / Issue Name (Optional):")
    farmer_name = st.text_input("Farmer / Contributor Name:")
    phone_number = st.text_input("Contact Number (Optional):")
    
    st.subheader("📍 Location Details")
    location = streamlit_geolocation()
    
    st.subheader("📷 Upload Sample Photo")
    uploaded_file = st.file_uploader("Choose a clear leaf or crop image", type=["jpg", "jpeg", "png"])
    
    st.divider()
    
    # GDPR & Ethical Consent Checkbox for Masters/Research Portfolio
    consent = st.checkbox(
        "I hereby agree to share this crop image, location, and diagnosis data for agricultural research, disease mapping, and AI model training.",
        value=True
    )
    
    submitted = st.form_submit_button("Submit Data Sample", type="primary")

if submitted:
    if not crop_name or not uploaded_file:
        st.error("Please provide both the Crop Name and an Image.")
    elif not consent:
        st.error("You must agree to the data sharing consent to contribute to the research dataset.")
    else:
        with st.spinner("Uploading image and saving record to database..."):
            image_bytes = uploaded_file.getvalue()
            image_url = upload_image_to_cloudinary(image_bytes)

            if image_url:
                lat = location.get("latitude") if isinstance(location, dict) else None
                lon = location.get("longitude") if isinstance(location, dict) else None

                sample_data = {
                    "user_email": st.session_state.user.get("email"),
                    "crop_name": crop_name,
                    "disease_name": disease_name or "Unspecified",
                    "farmer_name": farmer_name or "Anonymous",
                    "phone": phone_number or "N/A",
                    "image_url": image_url,
                    "latitude": lat,
                    "longitude": lon,
                    "consent_granted": consent
                }

                doc_id = save_sample(sample_data)
                if doc_id:
                    st.success("🎉 Sample submitted successfully! Thank you for contributing to agricultural research.")
                else:
                    st.error("Failed to save data record. Please check Firebase configuration.")
            else:
                st.error("Failed to upload image. Please check Cloudinary setup.")
