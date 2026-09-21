import time
import streamlit as st
import pandas as pd
from lib.cloudinary_client import upload_image
from lib.marketplace_client import get_seller_status, add_product, get_products_by_seller

st.set_page_config(page_title="Seller Dashboard · CropGuard", page_icon="📦")

st.title("📦 Seller Dashboard")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in first.")
    st.page_link("pages/5_Account.py", label="👤 Go to Account page", icon="👤")
    st.stop()

uid = st.session_state.user["uid"]
status = get_seller_status(uid)

if not status or status["status"] != "Approved":
    st.warning("You need an approved seller account to access this page.")
    st.page_link("pages/13_Seller_Request.py", label="🏢 Request seller access", icon="🏢")
    st.stop()

st.success(f"Selling as: **{status['businessName']}**")


@st.cache_data
def load_crop_options():
    return ["All crops"] + sorted(pd.read_csv("data/disease_database.csv")["Crop"].unique().tolist())


tab1, tab2 = st.tabs(["➕ Add Product", "📋 My Products"])

with tab1:
    title = st.text_input("Product name*")
    category = st.selectbox("Category*", ["Seed", "Fertilizer", "Pesticide", "Equipment", "Other"])
    crop_target = st.selectbox("Target crop*", load_crop_options())
    price = st.text_input("Price*", placeholder="e.g. PKR 1500 per bag")
    description = st.text_area("Description*")
    image = st.file_uploader("Product image", type=["jpg", "jpeg", "png"])

    if image:
        st.image(image, caption="Preview", use_container_width=True)

    if st.button("List product", type="primary"):
        if not all([title, price, description]):
            st.error("Please fill all required fields.")
        else:
            with st.spinner("Publishing..."):
                try:
                    image_url = None
                    if image:
                        image_url = upload_image(image.getvalue(), f"product_{int(time.time())}_{image.name}")
                    add_product(
                        uid, status["businessName"], title, category,
                        "" if crop_target == "All crops" else crop_target,
                        price, description, image_url,
                    )
                    st.success("Product listed!")
                except Exception as e:
                    st.error(f"Failed: {e}")

with tab2:
    products = get_products_by_seller(uid)
    if not products:
        st.info("You haven't listed any products yet.")
    for p in products:
        with st.container(border=True):
            if p.get("imageUrl"):
                st.image(p["imageUrl"], width=150)
            st.markdown(f"**{p.get('title')}** — {p.get('price')}")
            st.caption(f"{p.get('category')} · Target: {p.get('cropTarget') or 'All crops'}")
