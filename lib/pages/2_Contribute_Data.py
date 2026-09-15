import streamlit as st
from lib.auth_client import is_logged_in, get_user_info
from lib.firebase_client import fetch_user_samples

st.set_page_config(page_title="My Contributions - CropGuard", page_icon="🖼️", layout="wide")
st.title("🖼️ My Contributions")

if not is_logged_in():
    st.warning("🔒 Apne submissions dekhne ke liye **Account** page par ja kar login karein.")
    st.stop()

user_info = get_user_info()
user_id = user_info.get("localId", "")

samples = fetch_user_samples(user_id)

if samples:
    st.write(f"Aap ke total contributions: **{len(samples)}**")
    st.markdown("---")
    
    cols = st.columns(3)
    for idx, sample in enumerate(samples):
        with cols[idx % 3]:
            st.image(sample.get("image_url", ""), use_container_width=True)
            st.write(f"**Crop:** {sample.get('crop_name')}")
            st.write(f"**Disease:** {sample.get('disease_name')}")
            st.write(f"**Consent Given:** {'✅ Yes' if sample.get('farmer_consent') else '❌ No'}")
            st.write(f"**Submitted Date:** {sample.get('timestamp', '')[:10]}")
            st.markdown("---")
else:
    st.info("Aap ne abhi tak koi sample submit nahi kiya.")
