import streamlit as st
from lib.detect_disease import detect_disease

st.set_page_config(page_title="Detect Disease · CropGuard", page_icon="🔍")

st.title("🔍 Detect a crop disease")
st.write("Upload a photo of the affected leaf to get a likely diagnosis.")

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
