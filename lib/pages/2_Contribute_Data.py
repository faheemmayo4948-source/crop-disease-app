import time
import streamlit as st
from lib.cloudinary_client import upload_image
from lib.firebase_client import save_sample
from lib.location_client import get_location_widget, read_location_from_query

st.set_page_config(page_title="Contribute Data · CropGuard", page_icon="📤")

st.title("📤 Contribute a labeled sample")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in first to contribute a sample.")
    st.page_link("pages/5_Account.py", label="👤 Go to Account page", icon="👤")
    st.stop()

st.write(f"Contributing as: **{st.session_state.user['email']}**")
st.write("Help grow the dataset used for research and future model training.")

st.subheader("📍 Location (optional but helps research)")
get_location_widget()
lat, lon = read_location_from_query()
if lat and lon:
    st.success(f"Location captured: {lat:.4f}, {lon:.4f}")
else:
    st.caption("Click the button above to attach your field's location.")

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
                save_sample(
                    crop_name,
                    disease_label,
                    image_url,
                    farmer_uid=st.session_state.user["uid"],
                    farmer_email=st.session_state.user["email"],
                    latitude=lat,
                    longitude=lon,
                )

                st.success("Thank you — your sample has been added.")
            except Exception as e:
                st.error(f"Upload failed: {e}")
