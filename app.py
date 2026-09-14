import streamlit as st

st.set_page_config(
    page_title="CropGuard · Smart Disease Diagnostics",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Mobile-First Custom Styling
st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
    }
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 500px !important;
    }
    .app-title {
        color: #1E293B;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .app-subtitle {
        color: #0F766E;
        font-size: 1.25rem;
        font-weight: 700;
        line-height: 1.35;
        margin-bottom: 0.8rem;
    }
    .app-description {
        color: #475569;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 1.5rem;
    }
    .action-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        text-decoration: none !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .icon-box {
        font-size: 1.4rem;
        margin-right: 14px;
        width: 38px;
        height: 38px;
        background: #F0FDF4;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .card-text {
        color: #1E293B;
        font-weight: 600;
        font-size: 1rem;
        flex-grow: 1;
    }
    .arrow-icon {
        color: #94A3B8;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Hero Image Header
st.image("https://images.unsplash.com/photo-1592982537447-7440770cbfc9?q=80&w=1000&auto=format&fit=crop", use_container_width=True)

# Main Title & Subtitle
st.markdown('<div class="app-title">🌱 CropGuard</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Spot crop disease early, before it spreads across the field.</div>', unsafe_allow_html=True)
st.markdown('<div class="app-description">Upload a photo of an affected leaf to get AI diagnostics, localized treatment protocols, spray recommendations, and downloadable PDF reports.</div>', unsafe_allow_html=True)

st.divider()

# Interactive Action Cards for Mobile Navigation
st.markdown("### 🚀 Quick Services")

st.markdown("""
<a href="/Detect_Disease" target="_self" class="action-card">
    <div class="icon-box">🔍</div>
    <div class="card-text">Detect a Disease</div>
    <div class="arrow-icon">❯</div>
</a>

<a href="#" target="_self" class="action-card">
    <div class="icon-box">🧱</div>
    <div class="card-text">Contribute a Sample</div>
    <div class="arrow-icon">❯</div>
</a>

<a href="#" target="_self" class="action-card">
    <div class="icon-box">🌐</div>
    <div class="card-text">Browse Database</div>
    <div class="arrow-icon">❯</div>
</a>

<a href="#" target="_self" class="action-card">
    <div class="icon-box">👤</div>
    <div class="card-text">My Account</div>
    <div class="arrow-icon">❯</div>
</a>
""", unsafe_allow_html=True)
