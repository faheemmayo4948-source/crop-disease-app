import sys
import os

# Ensure Root Directory is in Python Path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import pandas as pd

try:
    from lib.firebase_client import get_all_samples
except ModuleNotFoundError:
    st.error("⚠️ Could not import `lib.firebase_client`. Please ensure `lib/firebase_client.py` exists in your repository.")
    st.stop()

st.set_page_config(page_title="Admin Data Gallery · CropGuard", page_icon="🔒", layout="wide")

st.title("🔒 Admin Research & Data Gallery")
st.write("Password-protected administration panel for reviewing farmer contributions and exporting research datasets.")

# Password Authentication
admin_pass = st.secrets.get("admin_password", "admin123")
input_pass = st.text_input("Enter Admin Password:", type="password")

if input_pass != admin_pass:
    if input_pass:
        st.error("❌ Incorrect Password.")
    else:
        st.info("🔑 Please enter the admin password configured in Streamlit Secrets.")
    st.stop()

st.success("✅ Admin Access Granted")
st.divider()

samples = get_all_samples()

if not samples:
    st.warning("No dataset samples found.")
else:
    df = pd.DataFrame(samples)

    st.subheader("📊 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Samples Collected", len(df))
    
    consent_count = df["consent_granted"].sum() if "consent_granted" in df.columns else len(df)
    col2.metric("Consent Approved Samples", consent_count)
    col3.metric("Unique Crops", df["crop_name"].nunique() if "crop_name" in df.columns else "N/A")

    st.divider()

    # Consent Filter
    only_consent = st.checkbox("Show ONLY samples with farmer consent (Recommended for Export)", value=True)

    export_df = df.copy()
    if only_consent and "consent_granted" in export_df.columns:
        export_df = export_df[export_df["consent_granted"] == True]

    # CSV Export Button
    csv_data = export_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Dataset CSV (For Research/Companies)",
        data=csv_data,
        file_name="CropGuard_Consented_Research_Data.csv",
        mime="text/csv",
        type="primary"
    )

    st.divider()
    st.subheader("🖼️ Sample Gallery View")

    cols = st.columns(3)
    for index, row in export_df.reset_index(drop=True).iterrows():
        col_idx = index % 3
        with cols[col_idx]:
            img_url = row.get("image_url", "")
            if img_url:
                st.image(img_url, use_container_width=True)
            
            st.markdown(f"**Crop:** {row.get('crop_name', 'N/A')}")
            st.markdown(f"**Disease:** {row.get('disease_name', 'N/A')}")
            st.markdown(f"**Contributor:** {row.get('farmer_name', 'Anonymous')}")
            
            has_consent = row.get('consent_granted', False)
            consent_badge = "✅ Consented" if has_consent else "❌ No Consent"
            st.caption(f"Consent Status: **{consent_badge}** | Phone: {row.get('phone', 'N/A')}")
            
            lat = row.get('latitude')
            lon = row.get('longitude')
            if lat and lon:
                st.caption(f"📍 GPS: {lat:.4f}, {lon:.4f}")
            st.divider()
