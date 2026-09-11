import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import gdown
import os
import json
import traceback
from datetime import datetime

st.set_page_config(page_title="Crop Disease Detection", page_icon="🌾", layout="wide")

MODEL_PATH = "model.h5"
MODEL_URL = "https://drive.google.com/uc?id=1jSvI1XBTMB1SyeBy-rYm1nUy2f3YdbnM"

CLASSES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry___Powdery_mildew', 'Cherry___healthy',
    'Corn___Cercospora_leaf_spot', 'Corn___Common_rust', 'Corn___Northern_Leaf_Blight', 'Corn___healthy',
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper_bell___Bacterial_spot', 'Pepper_bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites',
    'Tomato___Target_Spot', 'Tomato___Yellow_Leaf_Curl_Virus', 'Tomato___mosaic_virus', 'Tomato___healthy'
]

REMEDIES = {
    'Apple___Apple_scab': 'Fungicide spray karein, gire hue patte hata dein',
    'Apple___Black_rot': 'Infected branches prune karein, fungicide lagayein',
    'Potato___Early_blight': 'Resistant varieties use karein, fungicide spray karein',
    'Potato___Late_blight': 'Infected plants nikal dein, copper fungicide use karein',
    'Tomato___Bacterial_spot': 'Copper spray karein, crop rotation follow karein',
    'Corn___Common_rust': 'Resistant hybrid lagayein, fungicide use karein',
    'Grape___Black_rot': 'Pruning karein, fungicide spray karein',
    'Peach___Bacterial_spot': 'Bactericide use karein, resistant varieties lagayein',
    'Strawberry___Leaf_scorch': 'Fungicide spray, infected leaves hatayein',
}

def get_remedy(disease):
    return REMEDIES.get(disease, "Local agricultural expert se mashwara karein")


@st.cache_resource(show_spinner=False)
def load_model():
    """Download (if needed) and load the model. Raises with a clear message on failure."""
    try:
        if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 1024:
            # fuzzy=True fixes Google Drive's "can't scan large file for viruses" page
            # showing up instead of the actual file, which was silently corrupting model.h5
            gdown.download(MODEL_URL, MODEL_PATH, quiet=False, fuzzy=True)

        if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 1024:
            raise RuntimeError(
                "Model file download nahi hua ya corrupt hai (size too small). "
                "Google Drive link check karein — file 'Anyone with the link' access pe honi chahiye."
            )

        model = tf.keras.models.load_model(MODEL_PATH)
        return model
    except Exception as e:
        raise RuntimeError(f"Model load karne mein fail: {e}")


def preprocess(image: Image.Image, target_size=(224, 224)):
    """Convert any uploaded image (RGBA, grayscale, palette, etc.) into a clean
    (1, H, W, 3) normalized array. This was the main cause of silent detect
    failures — PNGs with transparency or grayscale JPEGs broke the old shape logic."""
    img = image.convert("RGB")          # forces 3 channels no matter the input mode
    img = img.resize(target_size)
    arr = np.array(img).astype("float32") / 255.0
    arr = np.expand_dims(arr, axis=0)   # shape: (1, 224, 224, 3)
    return arr


def save_data(filename, disease, confidence):
    record = {
        'filename': filename,
        'disease': disease,
        'confidence': confidence,
        'timestamp': datetime.now().isoformat()
    }
    data = []
    try:
        if os.path.exists('dataset.json'):
            with open('dataset.json', 'r') as f:
                data = json.load(f)
    except (json.JSONDecodeError, OSError):
        data = []  # corrupted/missing file shouldn't crash the app
    data.append(record)
    try:
        with open('dataset.json', 'w') as f:
            json.dump(data, f, indent=2)
    except OSError as e:
        st.warning(f"Data save nahi ho saka (storage issue): {e}")


st.title("Crop Disease Detection")
st.markdown("**Apni fasal ke patte ki photo upload karein aur disease detect karein**")

with st.sidebar:
    st.header("Research Info")
    st.info("Yeh platform AI se disease detect karta hai aur data research ke liye save karta hai.")
    if os.path.exists('dataset.json'):
        try:
            with open('dataset.json', 'r') as f:
                data = json.load(f)
            st.metric("Total Records", len(data))
        except (json.JSONDecodeError, OSError):
            st.metric("Total Records", 0)

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Leaf image upload karein", type=['jpg', 'jpeg', 'png'])
    image = None
    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
        except Exception as e:
            st.error(f"Image open nahi ho saki: {e}")
            image = None

with col2:
    if uploaded_file and image is not None and st.button("Detect Disease", type="primary"):
        try:
            with st.spinner("Model load ho raha hai (pehli baar thora time lagega)..."):
                model = load_model()

            with st.spinner("AI analyze kar raha hai..."):
                img_array = preprocess(image)

                # sanity check: does the array shape match what the model expects?
                expected_shape = model.input_shape[1:]  # e.g. (224, 224, 3)
                if img_array.shape[1:] != expected_shape:
                    st.error(
                        f"Image shape {img_array.shape[1:]} model ke expected input "
                        f"{expected_shape} se match nahi karti. preprocess() mein target_size adjust karein."
                    )
                    st.stop()

                preds = model.predict(img_array, verbose=0)[0]

                if len(preds) != len(CLASSES):
                    st.error(
                        f"Model {len(preds)} classes predict kar raha hai lekin CLASSES list mein "
                        f"{len(CLASSES)} hain — dono match nahi karte. Class list model ke training order se check karein."
                    )
                    st.stop()

                top_idx = int(np.argmax(preds))
                top_class = CLASSES[top_idx]
                confidence = float(preds[top_idx]) * 100

                disease_name = top_class.replace('_', ' ')
                st.success(f"### {disease_name}")
                st.metric("Confidence", f"{confidence:.2f}%")
                st.warning(f"**Remedy:** {get_remedy(top_class)}")

                st.subheader("Top 3 Predictions")
                top3 = np.argsort(preds)[-3:][::-1]
                for i in top3:
                    st.progress(float(preds[i]), text=f"{CLASSES[i].replace('_', ' ')}: {preds[i]*100:.2f}%")

                save_data(uploaded_file.name, top_class, confidence)
                st.info("Data research ke liye save ho gaya!")

        except Exception as e:
            st.error("Detection ke doran error aaya:")
            st.code(str(e))
            with st.expander("Full error details (debugging ke liye)"):
                st.code(traceback.format_exc())

st.markdown("---")
st.markdown("Crop Disease Detection Platform | PlantVillage Dataset | 38 Disease Classes")
