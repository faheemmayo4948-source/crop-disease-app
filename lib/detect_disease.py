import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from lib.detect_disease import predict_crop_disease

st.set_page_config(page_title="Detect Disease - CropGuard", page_icon="🔍")
st.title("🔍 Plant Disease Detection")

st.write("Apni mutasirah crop ki image upload karein taake AI disease scan kar sake.")

uploaded_file = st.file_uploader("Upload Image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Crop Image", use_container_width=True)
    
    if st.button("Detect Disease"):
        with st.spinner("AI disease analyze kar raha hai..."):
            image_bytes = uploaded_file.getvalue()
            predictions = predict_crop_disease(image_bytes)
            
        if predictions:
            st.subheader("Inference Results:")
            if isinstance(predictions, list) and len(predictions) > 0:
                top_pred = predictions[0]
                label = top_pred.get("label", "Unknown")
                score = round(top_pred.get("score", 0) * 100, 2)
                
                st.success(f"**Detected Disease**: {label}")
                st.info(f"**Confidence Score**: {score}%")
                
                with st.expander("Show Detailed Predictions"):
                    st.json(predictions)
            else:
                st.write(predictions)
        else:
            st.error("Prediction me koi masla aya. Token ya network connection check karein.")

st.markdown("---")
st.subheader("Optional: Capture GPS Location")
location = streamlit_geolocation()
if location and location.get("latitude"):
    st.write(f"📍 GPS Location: Lat {location.get('latitude')}, Lon {location.get('longitude')}")
