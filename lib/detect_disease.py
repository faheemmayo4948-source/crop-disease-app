import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from lib.detect_disease import detect_disease

# Page Config
st.set_page_config(page_title="Detect Disease · CropGuard", page_icon="🔍", layout="centered")

# Custom UI Styling
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        max-width: 800px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔍 Detect a crop disease")
st.write("Upload a photo of the affected leaf to get a likely diagnosis.")

st.divider()

# Location Section
st.subheader("📍 Share your location (optional)")
st.caption("Click the pin icon below and allow location access to improve disease mapping.")
location = streamlit_geolocation()

lat, lon = None, None
if location and location.get("latitude"):
    lat = location["latitude"]
    lon = location["longitude"]
    st.success(f"📍 Location captured: **{lat:.4f}, {lon:.4f}**")

st.divider()

# Image Upload Section
st.subheader("📸 Upload Leaf Image")
uploaded_file = st.file_uploader("Choose a leaf photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Leaf Sample", use_container_width=True)

    if st.button("Run Detection", type="primary"):
        with st.spinner("Analyzing leaf patterns..."):
            try:
                image_bytes = uploaded_file.getvalue()
                content_type = uploaded_file.type or "image/jpeg"
                predictions = detect_disease(image_bytes, content_type)

                st.success("Diagnosis Complete")
                st.subheader("📊 Likely Diagnosis Results")
                
                for pred in predictions[:3]:
                    label = pred.get("label", "Unknown")
                    score = pred.get("score", 0) * 100
                    
                    st.markdown(f"**{label}** — `{score:.1f}%` confidence")
                    st.progress(min(int(score), 100))
                    
            except Exception as e:
                st.error(f"Detection failed: {e}")
