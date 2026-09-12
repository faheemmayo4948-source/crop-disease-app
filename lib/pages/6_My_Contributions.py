import streamlit as st
from lib.firebase_client import get_db

st.set_page_config(page_title="My Contributions · CropGuard", page_icon="📊")

st.title("📊 My Contributions")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in first.")
    st.page_link("pages/5_Account.py", label="👤 Go to Account page", icon="👤")
    st.stop()

uid = st.session_state.user["uid"]


@st.cache_data(ttl=30)
def load_my_samples(uid):
    db = get_db()
    docs = db.collection("samples").where("farmerUid", "==", uid).stream()
    return [doc.to_dict() for doc in docs]


samples = load_my_samples(uid)

st.metric("Total samples you've contributed", len(samples))

if samples:
    st.divider()
    cols = st.columns(3)
    for i, sample in enumerate(samples):
        with cols[i % 3]:
            if sample.get("imageUrl"):
                st.image(sample["imageUrl"], use_container_width=True)
            st.markdown(f"**{sample.get('cropName', 'Unknown')}**")
            st.caption(sample.get("diseaseLabel", "No label"))
