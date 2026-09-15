import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from lib.detect_disease import detect_disease, generate_voice_note

st.set_page_config(page_title="Detect Disease · CropGuard", page_icon="🔍", layout="centered")

st.title("🔍 AI Crop Health & Disease Diagnostic")
st.write("Upload a clear photo of the infected crop leaf to identify diseases and receive instant treatment advice.")

uploaded_file = st.file_uploader("Choose a leaf image (JPG/PNG):", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Crop Leaf Sample", use_container_width=True)
    
    if st.button("Run AI Diagnosis", type="primary"):
        with st.spinner("Analyzing pathogen features via Plant.id API..."):
            image_bytes = uploaded_file.getvalue()
            matches = detect_disease(image_bytes)
            
            if matches and len(matches) > 0:
                top_match = matches[0]
                disease_name = top_match.get("name", "Unspecified Pathogen")
                confidence = top_match.get("probability", 0.0)
                
                st.success(f"✅ Primary Diagnosis: **{disease_name}** ({confidence:.1f}% confidence)")
                
                treatment = top_match.get("treatment")
                if treatment:
                    st.subheader("💊 Recommended Treatment & Spray Protocol")
                    if isinstance(treatment, dict):
                        for k, v in treatment.items():
                            st.write(f"**{k.capitalize()}:** {v}")
                    else:
                        st.write(str(treatment))
                
                # Urdu Voice Note Generation
                voice_text = f"Fasal ki bemari ki tashkhees ho gayi hai. Bemari ka naam {disease_name} hai."
                audio_fp = generate_voice_note(voice_text, lang='ur')
                if audio_fp:
                    st.subheader("🔊 Urdu Voice Guidance Note")
                    st.audio(audio_fp, format="audio/mp3")
            else:
                st.info("🌱 Plant appears healthy or no strong pathogen pattern was detected.")
