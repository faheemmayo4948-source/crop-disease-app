import streamlit as st
import pandas as pd
from lib.farmer_profile_client import save_farmer_profile, get_farmer_profile

st.set_page_config(page_title="My Farm Profile · CropGuard", page_icon="🚜")

st.title("🚜 My Farm Profile")
st.caption("Tell us about your land and crops so companies can suggest relevant products to you.")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in first.")
    st.page_link("pages/5_Account.py", label="👤 Go to Account page", icon="👤")
    st.stop()

uid = st.session_state.user["uid"]
existing = get_farmer_profile(uid)


@st.cache_data
def load_crop_options():
    return sorted(pd.read_csv("data/disease_database.csv")["Crop"].unique().tolist())


crop_options = load_crop_options()

land_size = st.number_input(
    "Land size", min_value=0.0, step=0.5,
    value=float(existing.get("landSize", 0)) if existing else 0.0,
)
land_unit = st.selectbox(
    "Unit", ["Acres", "Kanal", "Marla", "Hectares"],
    index=["Acres", "Kanal", "Marla", "Hectares"].index(existing.get("landUnit", "Acres")) if existing else 0,
)
crops = st.multiselect(
    "Crops you grow", crop_options,
    default=existing.get("crops", []) if existing else [],
)
location = st.text_input(
    "Location (city/area)", value=existing.get("location", "") if existing else "",
    placeholder="e.g. Multan, Faisalabad",
)

if st.button("Save profile", type="primary"):
    if not crops:
        st.error("Please select at least one crop.")
    else:
        save_farmer_profile(uid, land_size, land_unit, crops, location)
        st.success("Profile saved!")
        st.page_link("pages/14_Marketplace.py", label="🛒 See recommended products", icon="🛒")
