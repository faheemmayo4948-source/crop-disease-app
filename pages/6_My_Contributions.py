import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from lib.firebase_client import get_all_samples

st.set_page_config(page_title="My Contributions · CropGuard", page_icon="🌾", layout="centered")

st.title("🌾 My Data Contributions")

if not st.session_state.get("user"):
    st.warning("🔒 Please login via the **Account** page to view your submitted samples.")
    st.stop()

current_email = st.session_state.user.get("email")
st.write(f"Logged in user: **{current_email}**")

all_samples = get_all_samples()

# Filter samples for current user
user_samples = [s for s in all_samples if s.get("user_email") == current_email]

if not user_samples:
    st.info("You haven't submitted any crop data samples yet. Visit the **Contribute Data** page to submit your first sample!")
else:
    st.success(f"🎉 Total Contributions: **{len(user_samples)}** samples")
    st.divider()

    for item in user_samples:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            img_url = item.get("image_url")
            if img_url:
                st.image(img_url, use_container_width=True)
        
        with col2:
            st.markdown(f"### {item.get('crop_name', 'Crop')}")
            st.write(f"**Disease/Issue:** {item.get('disease_name', 'Unspecified')}")
            st.write(f"**Contributor Name:** {item.get('farmer_name', 'N/A')}")
            
            consent = item.get('consent_granted', False)
            st.caption(f"Consent Status: {'✅ Granted' if consent else '❌ Declined'}")
            
            lat = item.get('latitude')
            lon = item.get('longitude')
            if lat and lon:
                st.caption(f"📍 Location: {lat:.4f}, {lon:.4f}")
        
        st.divider()
