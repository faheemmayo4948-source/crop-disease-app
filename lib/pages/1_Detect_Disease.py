import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from lib.detect_disease import detect_disease

st.set_page_config(page_title="Detect Disease · CropGuard", page_icon="🔍")

st.title("🔍 Detect a crop disease")
st.write("Upload a photo of the affected leaf to get a likely diagnosis.")

st.subheader("📍 Share your location")
st.caption("Neeche pin icon par click karein aur browser mein **Allow Location** choose karein.")

# Geolocation component
location = streamlit_geolocation()

lat, lon = None, None

# Try auto location fetch
if location and location.get("latitude"):
    lat = location["latitude"]
    lon = location["longitude"]
    st.success(f"✅ GPS Location Captured: **{lat:.4f}, {lon:.4f}**")
else:
    st.warning("⚠️ GPS Access blocked ya unavailable hai. Manual coordinates enter karein:")
    
    # Fallback Manual Input
    col_lat, col_lon = st.columns(2)
    with col_lat:
        manual_lat = st.number_input("Latitude", value=31.5204, format="%.4f")
    with col_lon:
        manual_lon = st.number_input("Longitude", value=74.3587, format="%.4f")
    
    if st.checkbox("Use Manual Coordinates"):
        lat, lon = manual_lat, manual_lon
        st.info(f"Using Manual Location: {lat:.4f}, {lon:.4f}")

st.divider()

uploaded_file = st.file_uploader("Leaf photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded leaf", use_container_width=True)

    if st.button("Run detection", type="primary"):
        with st.spinner("Analyzing..."):
            try:
                image_bytes = uploaded_file.getvalue()
                content_type = uploaded_file.type or "image/jpeg"
                predictions = detect_disease(image_bytes, content_type)

                st.success("Diagnosis complete")
                st.subheader("Likely diagnosis")
                for pred in predictions[:3]:
                    label = pred.get("label", "Unknown")
                    score = pred.get("score", 0) * 100
                    st.write(f"**{label}** — {score:.1f}%")
                    st.progress(min(int(score), 100))
            except Exception as e:
                st.error(f"Detection failed: {e}")
