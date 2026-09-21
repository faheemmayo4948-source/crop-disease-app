import streamlit as st
from lib.marketplace_client import get_all_sellers, update_seller_status

st.set_page_config(page_title="Admin: Sellers · CropGuard", page_icon="🔒")

if "seller_admin_authenticated" not in st.session_state:
    st.session_state.seller_admin_authenticated = False

if not st.session_state.seller_admin_authenticated:
    st.title("🔒 Admin Access Required")
    password = st.text_input("Enter admin password", type="password")
    if st.button("Unlock"):
        if password == st.secrets.get("admin_password"):
            st.session_state.seller_admin_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

st.title("🔒 Review Seller Requests")

sellers = get_all_sellers()
pending = [s for s in sellers if s.get("status") == "Pending"]
approved = [s for s in sellers if s.get("status") == "Approved"]

tab1, tab2 = st.tabs([f"Pending ({len(pending)})", f"Approved ({len(approved)})"])

with tab1:
    if not pending:
        st.info("No pending requests.")
    for s in pending:
        with st.container(border=True):
            st.markdown(f"**{s.get('businessName')}** — {s.get('businessType')}")
            st.caption(f"{s.get('email')} · {s.get('contact')}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve", key=f"appr_{s['id']}"):
                    update_seller_status(s["id"], "Approved")
                    st.rerun()
            with col2:
                if st.button("❌ Reject", key=f"rej_{s['id']}"):
                    update_seller_status(s["id"], "Rejected")
                    st.rerun()

with tab2:
    if not approved:
        st.info("No approved sellers.")
    for s in approved:
        st.markdown(f"🟢 **{s.get('businessName')}** — {s.get('email')}")

if st.button("🔒 Lock again"):
    st.session_state.seller_admin_authenticated = False
    st.rerun()
