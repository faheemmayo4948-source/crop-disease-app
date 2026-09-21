import streamlit as st
from lib.marketplace_client import get_all_products, get_products_for_crop
from lib.farmer_profile_client import get_farmer_profile

st.set_page_config(page_title="Marketplace · CropGuard", page_icon="🛒", layout="wide")

st.title("🛒 Marketplace")
st.caption("Seeds, fertilizers, pesticides, and equipment from verified sellers.")


def render_product(p):
    with st.container(border=True):
        if p.get("imageUrl"):
            st.image(p["imageUrl"], use_container_width=True)
        st.markdown(f"**{p.get('title')}**")
        st.caption(f"{p.get('category')} · by {p.get('sellerName')}")
        st.markdown(f"💰 {p.get('price')}")
        st.write(p.get("description", ""))


user = st.session_state.get("user")
profile = get_farmer_profile(user["uid"]) if user else None

if profile and profile.get("crops"):
    st.subheader(f"🎯 Recommended for your crops ({', '.join(profile['crops'])})")
    recommended = []
    for crop in profile["crops"]:
        recommended.extend(get_products_for_crop(crop))
    seen_ids = set()
    unique_recommended = []
    for p in recommended:
        if p["id"] not in seen_ids:
            seen_ids.add(p["id"])
            unique_recommended.append(p)

    if unique_recommended:
        cols = st.columns(3)
        for i, p in enumerate(unique_recommended):
            with cols[i % 3]:
                render_product(p)
    else:
        st.info("No products matched to your crops yet — check all products below.")
    st.divider()
else:
    st.info("💡 Set up your Farm Profile to see products recommended for your specific crops.")
    st.page_link("pages/12_Farmer_Profile.py", label="🚜 Set up my farm profile", icon="🚜")
    st.divider()

st.subheader("📋 All Products")
all_products = get_all_products()

if not all_products:
    st.info("No products listed yet.")
else:
    categories = ["All categories"] + sorted({p.get("category", "Other") for p in all_products})
    category_filter = st.selectbox("Filter by category", categories)
    filtered = all_products if category_filter == "All categories" else [
        p for p in all_products if p.get("category") == category_filter
    ]

    cols = st.columns(3)
    for i, p in enumerate(filtered):
        with cols[i % 3]:
            render_product(p)
