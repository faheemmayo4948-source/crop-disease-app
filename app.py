import streamlit as st

st.set_page_config(page_title="CropGuard", page_icon="🌾", layout="centered")

# --- Custom styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stButton > button {
        border-radius: 8px;
        border: none;
        background-color: #1F7A4D;
        color: white;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #16532F;
        transform: translateY(-1px);
    }

    h1, h2, h3 {
        color: #16532F;
    }

    [data-testid="stMetric"] {
        background-color: #EDF3ED;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #D4E4D8;
    }

    [data-testid="stPageLink"] {
        border-radius: 8px;
        background-color: #EDF3ED;
        padding: 0.3rem 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero banner ---
st.image("assets/hero-banner.png", use_container_width=True)

st.title("🌾 CropGuard")
st.subheader("Spot crop disease early, before it spreads across the field.")

st.write(
    """
    Upload a photo of an affected leaf and get an instant diagnosis.
    Every contribution also helps build an open dataset for researchers
    working on crop health.
    """
)

# --- Navigation ---
row1_col1, row1_col2, row1_col3, row1_col4, row1_col5 = st.columns(5)
with row1_col1:
    st.page_link("pages/1_Detect_Disease.py", label="🔍 Detect a disease", icon="🔍")
with row1_col2:
    st.page_link("pages/2_Contribute_Data.py", label="📤 Contribute a sample", icon="📤")
with row1_col3:
    st.page_link("pages/3_Disease_Database.py", label="🌍 Browse database", icon="🌍")
with row1_col4:
    st.page_link("pages/5_Account.py", label="👤 My account", icon="👤")
with row1_col5:
    st.page_link("pages/7_Disease_Forecast.py", label="🌤️ Weather forecast", icon="🌤️")

row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
with row2_col1:
    st.page_link("pages/8_Spray_Guide.py", label="💊 Spray guide", icon="💊")
with row2_col2:
    st.page_link("pages/9_Dealer_Locator.py", label="🏪 Find stores", icon="🏪")
with row2_col3:
    st.page_link("pages/10_Field_History.py", label="📈 Field history", icon="📈")
with row2_col4:
    st.page_link("pages/11_Research_Hub.py", label="📚 Research hub", icon="📚")

st.divider()

# --- Value proposition ---
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

st.divider()

# --- Share ---
st.subheader("📢 Doston ko share karen")
share_text = "Apni fasal ki bimari sirf ek photo se pehchanen — bilkul FREE! CropGuard app try karen"
share_url = "https://detect-diseas-faheem.streamlit.app"  # apna asal app URL confirm kar len
whatsapp_link = f"https://wa.me/?text={share_text}%20{share_url}"
st.link_button("📤 WhatsApp per Share karen", whatsapp_link, use_container_width=True)

st.divider()

# --- Footer ---
st.caption("CropGuard — built to help farmers and researchers.")
