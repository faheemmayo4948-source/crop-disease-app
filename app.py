import streamlit as st

# Page Configuration (Wide layout banner ko full view dene ke liye)
st.set_page_config(
    page_title="CropGuard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Padding fix aur Clean Styling ke liye
st.markdown(
    """
    <style>
    /* Top whitespace kam karne ke liye */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }
    
    /* Image scaling fix */
    img {
        border-radius: 8px;
        object-fit: cover;
    }

    /* Page Link Buttons ko Box Container Card jaisa look dene ke liye */
    div[data-testid="stPageLink"] > a {
        border: 1px solid #d3d3d3;
        border-radius: 8px;
        padding: 15px 10px;
        text-align: center;
        justify-content: center;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    div[data-testid="stPageLink"] > a:hover {
        border-color: #2e7d32;
        background-color: #f4f9f4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 1. Full Banner Image (No Cropping)
st.image("https://i.postimg.cc/P5wr1nqM/hero-banner-png.png", use_container_width=True)

# 2. Main Title & Description Section
st.markdown("## 🌾 **CropGuard**")
st.markdown("### Spot crop disease early, before it spreads across the field.")

st.write(
    """
    Upload a photo of an affected leaf and get an instant diagnosis. 
    Every contribution also helps build an open dataset for researchers 
    working on crop health.
    """
)

st.write("")  # Extra spacing

# 3. Interactive Cards / Navigation Links
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.page_link("pages/1_Detect_Disease.py", label="Detect a disease", icon="🔍")
with col2:
    st.page_link("pages/2_Contribute_Data.py", label="Contribute a sample", icon="📤")
with col3:
    st.page_link("pages/3_Disease_Database.py", label="Browse database", icon="🌍")
with col4:
    st.page_link("pages/5_Account.py", label="My account", icon="👤")
with col5:
    st.page_link("pages/7_Disease_Forecast.py", label="Weather forecast", icon="🌤️")

# 4. Proper Horizontal Line (Divider)
st.divider()

# 5. Three Column Information Cards
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
