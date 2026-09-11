import time
import streamlit as st
from lib.cloudinary_client import upload_image
from lib.firebase_client import save_sample

st.set_page_config(page_title="Contribute Data · CropGuard", page_icon="📤")

st.title("📤 Contribute a labeled sample")
st.write("Help grow the dataset used for research and future model training.")

crop_name = st.text_input("Crop name", placeholder="e.g. Rice, Wheat, Tomato")
disease_label = st.text_input("Disease label", placeholder="e.g. Bacterial Leaf Blight")
uploaded_file = st.file_uploader("Leaf image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Preview", use_container_width=True)

if st.button("Submit sample", type="primary"):
    if not crop_name or not disease_label or not uploaded_file:
        st.error("Please fill every field and choose an image.")
    else:
        with st.spinner("Uploading..."):
            try:
                file_bytes = uploaded_file.getvalue()
                file_name = f"{int(time.time())}_{uploaded_file.name}"

                image_url = upload_image(file_bytes, file_name)
                save_sample(crop_name, disease_label, image_url)

                st.success("Thank you — your sample has been added.")
            except Exception as e:
                st.error(f"Upload failed: {e}")
