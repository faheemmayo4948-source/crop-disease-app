import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from lib.detect_disease import detect_disease

st.set_page_config(page_title="Detect Disease · CropGuard", page_icon="🔍")

st.title("🔍 Detect Crop Disease")
st.write("Upload a leaf photo for diagnosis and detailed treatment guidance.")

st.subheader("📍 Share location (optional)")
location = streamlit_geolocation()

lat, lon = None, None
if location and location.get("latitude"):
    lat = location["latitude"]
    lon = location["longitude"]
    st.success(f"Location captured: {lat:.4f}, {lon:.4f}")

uploaded_file = st.file_uploader("Leaf photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded leaf preview", use_container_width=True)

    if st.button("Run Advanced Detection", type="primary"):
        with st.spinner("Analyzing plant health..."):
            image_bytes = uploaded_file.getvalue()
            content_type = uploaded_file.type or "image/jpeg"
            
            predictions = detect_disease(image_bytes, content_type, latitude=lat, longitude=lon)

            if predictions:
                st.success("Diagnosis complete!")
                st.markdown("### 📋 Primary Diagnosis Results")

                for i, pred in enumerate(predictions):
                    label = pred["label"]
                    score = pred["score"] * 100

                    with st.expander(f"**{i+1}. {label}** — `{score:.1f}% Match`", expanded=(i == 0)):
                        st.progress(min(int(score), 100))
                        st.write(f"**Description:** {pred['description']}")

                        st.markdown("---")
                        st.markdown("#### 🛠️ Treatment Options")
                        
                        bio = pred.get("treatment_biological", [])
                        chem = pred.get("treatment_chemical", [])
                        prev = pred.get("prevention", [])

                        if bio:
                            st.markdown("**🌱 Biological Control:**")
                            for item in bio:
                                st.write(f"- {item}")
                        
                        if chem:
                            st.markdown("**🧪 Chemical Treatments:**")
                            for item in chem:
                                st.write(f"- {item}")
                                
                        if prev:
                            st.markdown("**🛡️ Prevention Strategy:**")
                            for item in prev:
                                st.write(f"- {item}")
                        
                        if not bio and not chem and not prev:
                            st.info("Is specific disease ke liye API database mein biological/chemical treatments mention nahi hain. (Leaf control/pruning recommended).")
            else:
                st.error("No predictions returned. Check your API key setup.")
