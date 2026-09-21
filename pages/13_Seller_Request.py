import streamlit as st
from lib.marketplace_client import request_seller_access, get_seller_status

st.set_page_config(page_title="Seller Access · CropGuard", page_icon="🏢")

st.title("🏢 Become a Seller")
st.caption("Sell your agricultural products (seeds, fertilizer, pesticides, equipment) directly to farmers.")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in first.")
    st.page_link("pages/5_Account.py", label="👤 Go to Account page", icon="👤")
    st.stop()

uid = st.session_state.user["uid"]
status = get_seller_status(uid)

if status:
    badge = {"Approved": "🟢", "Pending": "🟡", "Rejected": "🔴"}.get(status["status"], "⚪")
    st.info(f"{badge} Your seller request status: **{status['status']}**")
    if status["status"] == "Approved":
        st.page_link("pages/15_Seller_Dashboard.py", label="📦 Go to Seller Dashboard", icon="📦")
    st.stop()

st.subheader("Request Access")
business_name = st.text_input("Business/Company name*")
business_type = st.selectbox("Business type*", ["Seed supplier", "Fertilizer company", "Pesticide company", "Equipment dealer", "Other"])
contact = st.text_input("Contact email or phone*")

if st.button("Submit request", type="primary"):
    if not business_name or not contact:
        st.error("Please fill all required fields.")
    else:
        request_seller_access(uid, st.session_state.user["email"], business_name, business_type, contact)
        st.success("Request submitted! An admin will review it shortly.")
        st.rerun()
