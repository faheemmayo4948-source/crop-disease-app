import sys
import os

# Root directory ko Python path mein add karne ke liye (Fixes ImportError)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from lib.detect_disease import detect_disease, generate_pdf_report

st.set_page_config(page_title="Detect Disease · CropGuard", page_icon="🔍", layout="centered")

# Mobile-First Custom Styling
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    .block-container { padding-top: 1.5rem !important; max-width: 550px !important; }
</style>
""", unsafe_allow_html=True)

st.title("🔍 Detect Crop Disease")
st.write("Upload a leaf photo for high-accuracy diagnosis, treatments, and localized spray recommendations.")

# Language Toggle
lang = st.radio("🌐 Language / زبان:", ["English", "اردو (Urdu)"], horizontal=True)

st.divider()

# Location Section
if lang == "English":
    st.subheader("📍 Share Location (Optional)")
    st.caption("Location helps match local spray brands available in your area.")
else:
    st.subheader("📍 لوکیشن شیئر کریں (اختیاری)")
    st.caption("لوکیشن سے آپ کے علاقے میں دستیاب مقامی اسپرے کی معلومات ملتی ہے۔")

location = streamlit_geolocation()

lat, lon = None, None
if location and location.get("latitude"):
    lat = location["latitude"]
    lon = location["longitude"]
    st.success(f"✅ Location Captured: {lat:.4f}, {lon:.4f}")

st.divider()

# File Upload
upload_label = "Upload Leaf Photo" if lang == "English" else "پتے کی تصویر اپلوڈ کریں"
uploaded_file = st.file_uploader(upload_label, type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Leaf Preview", use_container_width=True)

    btn_label = "Run Diagnostics & Spray Guide" if lang == "English" else "تشخیص اور اسپرے کی معلومات حاصل کریں"
    
    if st.button(btn_label, type="primary", use_container_width=True):
        with st.spinner("Analyzing plant health & finding local treatments..."):
            image_bytes = uploaded_file.getvalue()
            content_type = uploaded_file.type or "image/jpeg"
            
            predictions = detect_disease(image_bytes, content_type, latitude=lat, longitude=lon)

            if predictions:
                st.success("Diagnosis Complete!" if lang == "English" else "تشخیص مکمل ہو گئی!")
                st.divider()

                # PDF Download Button for Top Prediction
                top_pred = predictions[0]
                pdf_file = generate_pdf_report(top_pred, lat=lat, lon=lon)
                
                st.download_button(
                    label="📄 Download Official PDF Report" if lang == "English" else "📄 پی ڈی ایف رپورٹ ڈاؤن لوڈ کریں",
                    data=pdf_file,
                    file_name=f"CropGuard_Report_{top_pred['label'].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                st.divider()

                # Render Diagnostic Details
                for i, pred in enumerate(predictions):
                    label = pred["label"]
                    score = pred["score"] * 100

                    st.markdown(f"### {i+1}. {label} (`{score:.1f}% Match`)")
                    st.progress(min(int(score), 100))
                    
                    st.write(f"**Description:** {pred['description']}")

                    # Treatments UI Block
                    st.markdown("#### 💊 Treatment & Prevention Protocol" if lang == "English" else "#### 💊 علاج اور بچاؤ کی تدابیر")
                    
                    bio = [b for b in pred["biological"] if b]
                    chem = [c for c in pred["chemical"] if c]
                    prev = [p for p in pred["prevention"] if p]

                    if bio:
                        st.markdown("**🌱 Biological / Organic Treatment:**" if lang == "English" else "**🌱 حیاتیاتی / نامیاتی علاج:**")
                        for item in bio:
                            st.write(f"- {item}")

                    if chem:
                        st.markdown("**🧪 Standard Chemical Control:**" if lang == "English" else "**🧪 کیمیائی کنٹرول:**")
                        for item in chem:
                            st.write(f"- {item}")

                    # Location-based Spray Recommendations
                    st.markdown("#### 🎯 Location-based Recommended Sprays" if lang == "English" else "#### 🎯 علاقائی اور مقامی اسپرے")
                    st.info("Recommended sprays for your region:" if lang == "English" else "آپ کے علاقے کے لیے تجویز کردہ مقامی اسپرے:")
                    for spray in pred["local_sprays"]:
                        st.write(f"👉 **{spray}**")

                    if prev:
                        st.markdown("**🛡️ Future Prevention:**" if lang == "English" else "**🛡️ آئندہ بچاؤ کی تدابیر:**")
                        for item in prev:
                            st.write(f"- {item}")

                    # Fallback Advice
                    if not bio and not chem and not prev:
                        st.info("Prune affected leaves, ensure adequate sunlight, and avoid over-watering." if lang == "English" else "متاثرہ پتے کاٹ دیں، مناسب دھوپ کو یقینی بنائیں اور زیادہ پانی دینے سے گریز کریں۔")

                    st.divider()
            else:
                st.error("Diagnosis failed. Verify your PLANT_ID_API_KEY in Streamlit Secrets.")
