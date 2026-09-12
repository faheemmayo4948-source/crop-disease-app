import streamlit as st

st.set_page_config(page_title="CropGuard", page_icon="🌾", layout="centered")

st.title("🌾 CropGuard")
st.subheader("Spot crop disease early, before it spreads across the field.")

st.write(
    """
    Upload a photo of an affected leaf and get an instant diagnosis.
    Every contribution also helps build an open dataset for researchers
    working on crop health.
    """
)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.page_link("pages/1_Detect_Disease.py", label="🔍 Detect a disease", icon="🔍")
with col2:
    st.page_link("pages/2_Contribute_Data.py", label="📤 Contribute a sample", icon="📤")
with col3:
    st.page_link("pages/3_Disease_Database.py", label="🌍 Browse database", icon="🌍")
with col4:
    st.page_link("pages/5_Account.py", label="👤 My account", icon="👤")
with col5:
    st.page_link("pages/7_Disease_Forecast.py", label="🌤️ Weather forecast", icon="🌤️")

st.divider()

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
