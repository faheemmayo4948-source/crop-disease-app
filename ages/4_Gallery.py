import streamlit as st
import pandas as pd
from lib.firebase_client import fetch_all_samples

st.set_page_config(page_title="Admin Gallery - CropGuard", page_icon="🔒", layout="wide")
st.title("🔒 Admin Gallery & Data Export")

admin_pass = st.secrets.get("admin_password", "")
user_pass = st.text_input("Enter Admin Password", type="password")

if user_pass == admin_pass and admin_pass != "":
    st.success("Access Granted!")
    
    samples = fetch_all_samples()
    if samples:
        df = pd.DataFrame(samples)
        
        st.subheader("Dataset Summary & CSV Export")
        st.write(f"Total Contributions: **{len(df)}**")
        
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data CSV (For Commercial & Research Partners)",
            data=csv_data,
            file_name="cropguard_contributions.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        st.subheader("Submitted Samples Gallery")
        
        cols = st.columns(3)
        for idx, sample in enumerate(samples):
            with cols[idx % 3]:
                st.image(sample.get("image_url", ""), use_container_width=True)
                st.write(f"**Crop:** {sample.get('crop_name')}")
                st.write(f"**Disease:** {sample.get('disease_name')}")
                st.write(f"**User Email:** {sample.get('user_email')}")
                st.write(f"**Farmer Consent:** {'✅ Yes' if sample.get('farmer_consent') else '❌ No'}")
                st.write(f"**Location:** {sample.get('latitude')}, {sample.get('longitude')}")
                st.markdown("---")
    else:
        st.info("No submissions found in Firestore database.")
elif user_pass:
    st.error("Incorrect Admin Password!")
