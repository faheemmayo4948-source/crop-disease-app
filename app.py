import streamlit as st

st.set_page_config(
    page_title="CropGuard - AI Crop Disease Detection",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 CropGuard: AI-Powered Plant Disease Diagnostic App")
st.subheader("Pakistani Kisaano Aur Researchers Ke Liye Ek Aasaan Solution")

st.markdown("""
### Welcome to CropGuard!
CropGuard ek free platform hai jo farmers aur agricultural research community ki madad karta hai:

1. **🔬 Disease Detection**: Apni crop image upload karein aur AI se bimari ka shinaakht karein.
2. **🤝 Contribute Data**: Crop samples upload karein aur research network ka hissa banein.
3. **📚 Reference Database**: Common plant diseases, unke symptoms aur treatments search karein.
4. **🌤️ Weather Forecast & Risk**: Weather alerts aur disease outbreak warnings check karein.

---
**Side Navigation Bar** se kisi bhi page par jaayein aur features utilize karein.
""")

col1, col2, col3 = st.columns(3)
col1.metric("Supported Diseases", "70+")
col2.metric("AI Model", "MobileNetV2")
col3.metric("Backend Status", "Active (Firestore & Cloudinary)")
