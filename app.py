import streamlit as st

st.set_page_config(page_title="CropGuard", page_icon="🌾", layout="centered")

# Enhanced Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    
    /* Global Primary Buttons */
    .stButton > button {
        border-radius: 8px; border: none; background-color: #1F7A4D;
        color: white; font-weight: 600; padding: 0.5rem 1.5rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover { 
        background-color: #16532F; 
        transform: translateY(-2px); 
        box-shadow: 0px 4px 10px rgba(22, 83, 47, 0.25);
    }
    
    h1, h2, h3 { color: #16532F; }
    
    /* Metrics Styling */
    [data-testid="stMetric"] {
        background-color: #EDF3ED; border-radius: 10px;
        padding: 1rem; border: 1px solid #D4E4D8;
    }
    
    /* Navigation Page Links Base Style */
    [data-testid="stPageLink"] {
        border-radius: 10px;
        background-color: #EDF3ED;
        padding: 0.5rem 0.8rem;
        border: 1px solid #D4E4D8;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.05);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Navigation Page Links Hover Effect */
    [data-testid="stPageLink"]:hover {
        background-color: #FFFFFF;
        border-color: #1F7A4D;
        transform: translateY(-3px);
        box-shadow: 0px 6px 15px rgba(31, 122, 77, 0.18);
    }
    
    /* Page Link Text Styling Inside */
    [data-testid="stPageLink"] a {
        font-weight: 600;
        color: #16532F !important;
        text-decoration: none;
    }

    /* Custom Feature Cards Styling */
    .feature-card {
        background-color: #F8FAF8;
        border: 1px solid #D4E4D8;
        border-radius: 12px;
        padding: 1.2rem;
        height: 100%;
        box-shadow: 0px 3px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.25s ease;
    }
    .feature-card:hover {
        border-color: #1F7A4D;
        transform: translateY(-2px);
        box-shadow: 0px 6px 14px rgba(31, 122, 77, 0.12);
    }
    .feature-card h4 {
        color: #16532F;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .feature-card p {
        color: #4A5568;
        font-size: 0.88rem;
        margin-bottom: 0;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌾 CropGuard")
st.subheader("Spot crop disease early, before it spreads across the field.")

# Styled Hero Banner Image with reduced width (max-width: 500px)
hero_banner_url = "https://i.postimg.cc/s1BkM74n/hero-banner-png.png"
st.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <img src="{hero_banner_url}" 
             style="max-width: 500px; width: 100%; border-radius: 15px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.12); border: 1px solid #D4E4D8;" 
             alt="CropGuard Hero Banner">
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    """
    Upload a photo of an affected leaf and get an instant diagnosis.
    Every contribution also helps build an open dataset for researchers
    working on crop health.
    """
)

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/1_Detect_Disease.py", label="🔍 Detect a disease", icon="🔍")
with col2:
    st.page_link("pages/2_Contribute_Data.py", label="📤 Contribute a sample", icon="📤")
with col3:
    st.page_link("pages/3_Disease_Database.py", label="🌍 Browse database", icon="🌍")

col4, col5 = st.columns(2)
with col4:
    st.page_link("pages/5_Account.py", label="👤 My account", icon="👤")
with col5:
    st.page_link("pages/7_Disease_Forecast.py", label="🌤️ Weather forecast", icon="🌤️")

st.divider()

# Styled Feature Cards Columns
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🚜 For farmers</h4>
            <p>Take a photo of a sick leaf and get a likely diagnosis in seconds.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🔬 For researchers</h4>
            <p>Access a growing, labeled dataset of crop images from real fields.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        """
        <div class="feature-card">
            <h4>📊 For the data</h4>
            <p>Every contribution builds a global picture of crop health over time.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()
st.subheader("📢 Doston ko share karen")
share_text = "Apni fasal ki bimari sirf ek photo se pehchanen — bilkul FREE! CropGuard app try karen"
share_url = "https://detect-diseas-faheem.streamlit.app"
whatsapp_link = f"https://wa.me/?text={share_text}%20{share_url}"
st.link_button("📤 WhatsApp per Share karen", whatsapp_link, use_container_width=True)

st.divider()
st.caption("CropGuard — built to help farmers and researchers.")
