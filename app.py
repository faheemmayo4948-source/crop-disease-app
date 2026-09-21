import streamlit as st

st.set_page_config(page_title="CropGuard", page_icon="🌾", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

    .stButton > button, .stLinkButton > a {
        border-radius: 10px; border: none; background-color: #1F7A4D;
        color: white !important; font-weight: 600; padding: 0.6rem 1.5rem;
        transition: all 0.2s ease; box-shadow: 0 2px 6px rgba(31,122,77,0.25);
    }
    .stButton > button:hover, .stLinkButton > a:hover {
        background-color: #16532F; transform: translateY(-1px);
    }

    h1 { color: #16532F; font-weight: 700; }
    h2, h3 { color: #1F7A4D; font-weight: 600; }

    [data-testid="stMetric"] {
        background-color: #F1F7F3; border-radius: 12px;
        padding: 1rem; border: 1px solid #DCEAE1;
    }

    [data-testid="stPageLink"] {
        border-radius: 10px; background-color: #F1F7F3;
        padding: 0.5rem 0.9rem; border: 1px solid #DCEAE1;
        transition: all 0.2s ease;
    }
    [data-testid="stPageLink"]:hover { background-color: #E4F0E9; }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px !important;
    }

    hr { margin: 1.5rem 0; }

    @media (max-width: 640px) {
        h1 { font-size: 1.6rem !important; }
        h2 { font-size: 1.25rem !important; }
        h3 { font-size: 1.05rem !important; }
    }
</style>
""", unsafe_allow_html=True)

st.title("🌾 CropGuard")
st.subheader("Detect crop disease, get weather-based warnings, and shop trusted farm products — all in one place.")

st.write(
    "Upload a leaf photo for instant diagnosis, get treatment guidance, see what's "
    "coming next based on your local weather, and connect with verified sellers for "
    "the products your crops actually need."
)

st.divider()
st.subheader("🚀 Quick actions")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.page_link("pages/1_Detect_Disease.py", label="🔍 Detect Disease", icon="🔍")
with col2:
    st.page_link("pages/14_Marketplace.py", label="🛒 Marketplace", icon="🛒")
with col3:
    st.page_link("pages/12_Farmer_Profile.py", label="🚜 My Farm", icon="🚜")
with col4:
    st.page_link("pages/4_My_Account.py", label="👤 Account", icon="👤")

st.caption("More features — Contribute Data, Disease Database, Weather Forecast, and more — are in the sidebar menu. →")

st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**🧑‍🌾 For farmers**")
    st.caption("Diagnose disease, get treatment advice, and find the right products for your crops.")
with c2:
    st.markdown("**🏢 For sellers**")
    st.caption("Reach farmers directly with products matched to their actual crops.")
with c3:
    st.markdown("**🔬 For researchers**")
    st.caption("Access a growing, geo-tagged dataset of real crop disease images.")

st.divider()
st.subheader("📢 Share CropGuard")
share_text = "Detect crop diseases, get treatment tips, and shop farm products — try CropGuard, free!"
share_url = "https://detect-diseas-faheem.streamlit.app"
whatsapp_link = f"https://wa.me/?text={share_text}%20{share_url}"
st.link_button("📤 Share on WhatsApp", whatsapp_link, use_container_width=True)

st.divider()
st.caption("CropGuard — connecting farmers, research, and agriculture businesses.")
