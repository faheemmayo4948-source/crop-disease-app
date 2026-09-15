import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from lib.detect_disease import analyze_crop_image, generate_voice_note

st.set_page_config(page_title="Detect Disease · CropGuard", page_icon="🔍", layout="centered")

st.title("🔍 AI Crop Health & Disease Diagnostic")
st.write("Upload a clear photo of the infected crop leaf to identify diseases and receive instant treatment advice.")

uploaded_file = st.file_uploader("Choose a leaf image (JPG/PNG):", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Crop Leaf Sample", use_container_width=True)
    
    if st.button("Run AI Diagnosis", type="primary"):
        with st.spinner("Analyzing pathogen features via Plant.id API..."):
            image_bytes = uploaded_file.getvalue()
            result = analyze_crop_image(image_bytes)
            
            if result:
                health_res = result.get("result", {}).get("disease", {})
                suggestions = health_res.get("suggestions", [])
                
                if suggestions:
                    top_match = suggestions[0]
                    disease_name = top_match.get("name", "Unknown Issue")
                    probability = top_match.get("probability", 0.0) * 100
                    
                    st.success(f"✅ Primary Diagnosis: **{disease_name}** ({probability:.1f}% confidence)")
                    
                    details = top_match.get("details", {})
                    if "treatment" in details:
                        st.subheader("💊 Recommended Treatment & Spray Protocol")
                        st.write(details.get("treatment"))
                    
                    # Urdu Voice Note Generation
                    voice_text = f"Fasal ki bemari ki tashkhees ho gayi hai. Bemari ka naam {disease_name} hai."
                    audio_fp = generate_voice_note(voice_text, lang='ur')
                    if audio_fp:
                        st.subheader("🔊 Urdu Voice Guidance Note")
                        st.audio(audio_fp, format="audio/mp3")
                else:
                    st.info("🌱 The plant appears healthy or no strong pathogen pattern was detected.")
