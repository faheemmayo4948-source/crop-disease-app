import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from PIL import Image
from streamlit_geolocation import streamlit_geolocation
from lib.detect_disease import detect_disease, generate_pdf_report

st.set_page_config(page_title="Detect Disease · CropGuard", page_icon="🔍", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    .block-container { padding-top: 1.5rem !important; max-width: 550px !important; }
</style>
""", unsafe_allow_html=True)

st.title("🔍 Detect Crop Disease")
st.write("Upload a leaf photo for high-accuracy diagnosis, treatments, and localized spray recommendations.")

lang = st.radio("🌐 Language / زبان:", ["English", "اردو (Urdu)"], horizontal=True)

st.divider()

if lang == "English":
    st.subheader("📍 Share Location (Optional)")
    st.caption("Location helps match local spray brands available in your area.")
else:
    st.subheader("📍 لوکیشن شیئر کریں (اختیاری)")
    st.caption("لوکیشن سے آپ کے علاقے میں دستیاب مقامی اسپرے کی معلومات ملتی ہے۔")

location = streamlit_geolocation()

lat, lon = None, None
if location and isinstance(location, dict) and location.get("latitude"):
    lat = location["latitude"]
    lon = location["longitude"]
    st.success(f"✅ Location Captured: {lat:.4f}, {lon:.4f}")

st.divider()

upload_label = "Upload Leaf Photo" if lang == "English" else "پتے کی تصویر اپلوڈ کریں"
uploaded_file = st.file_uploader(upload_label, type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Leaf Preview")

    btn_label = "Run Diagnostics & Spray Guide" if lang == "English" else "تشخیص اور اسپرے کی معلومات حاصل کریں"
    
    if st.button(btn_label, type="primary"):
        with st.spinner("Analyzing plant health & finding local treatments..."):
            image_bytes = uploaded_file.getvalue()
            content_type = uploaded_file.type or "image/jpeg"
            
            predictions = detect_disease(image_bytes, content_type, latitude=lat, longitude=lon)

            if predictions:
                st.success("Diagnosis Complete!" if lang == "English" else "تشخیص مکمل ہو گئی!")
                st.divider()

                top_pred = predictions[0]
                pdf_file = generate_pdf_report(top_pred, lat=lat, lon=lon)
                
                st.download_button(
                    label="📄 Download Official PDF Report" if lang == "English" else "📄 پی ڈی ایف رپورٹ ڈاؤن لوڈ کریں",
                    data=pdf_file,
                    file_name=f"CropGuard_Report_{top_pred['label'].replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
                
                st.divider()

                for i, pred in enumerate(predictions):
                    label = pred.get("label", "Crop Health Issue")
                    score = pred.get("score", 0.0) * 100

                    st.markdown(f"### {i+1}. {label} (`{score:.1f}% Match`)")
                    st.progress(min(int(score), 100))
                    
                    st.write(f"**Description:** {pred.get('description', 'Pathogen detected.')}")

                    # Spray Recommendations (Guaranteed Output)
                    st.markdown("#### 🎯 Recommended Chemical & Market Sprays" if lang == "English" else "#### 🎯 تجویز کردہ کیمیائی اسپرے")
                    st.info("Recommended dosages for your region:" if lang == "English" else "آپ کے علاقے کے لیے تجویز کردہ اسپرے:")
                    
                    sprays = pred.get("local_sprays", [])
                    for spray in sprays:
                        st.write(f"👉 **{spray}**")

                    # Biological Treatments
                    bio = pred.get("biological", [])
                    if bio:
                        st.markdown("**🌱 Organic / Biological Control:**" if lang == "English" else "**🌱 حیاتیاتی علاج:**")
                        for item in bio:
                            st.write(f"- {item}")

                    # Prevention Protocol
                    prev = pred.get("prevention", [])
                    if prev:
                        st.markdown("**🛡️ Preventive Protocol:**" if lang == "English" else "**🛡️ بچاؤ کی تدابیر:**")
                        for item in prev:
                            st.write(f"- {item}")

                    st.divider()
            else:
                st.error("Diagnosis failed. Please check your API key or image clarity.")
