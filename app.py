import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import gdown
import os
import json
from datetime import datetime

st.set_page_config(page_title="Crop Disease Detection", page_icon="🌾", layout="wide")

MODEL_PATH = "model.h5"
MODEL_URL = "https://drive.google.com/uc?id=1jSvI1XBTMB1SyeBy-rYm1nUy2f3YdbnM"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        with st.spinner("📥 Model download ho raha hai..."):
            gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
    model = tf.keras.models.load_model(MODEL_PATH)
    return model

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
    return REMEDIES.get(disease, "🌱 Local agricultural expert se mashwara karein")

def preprocess(image):
    img = image.resize((224, 224))
    arr = np.array(img) / 255.0
    if len(arr.shape) == 2:
        arr = np.stack([arr] * 3, axis=-1)
    elif arr.shape[-1] == 4:
        arr = arr[:, :, :3]
    return np.expand_dims(arr, axis=0)

def save_data(filename, disease, confidence):
    record = {
        'filename': filename,
        'disease': disease,
        'confidence': confidence,
        'timestamp': datetime.now().isoformat()
    }
    data = []
    if os.path.exists('dataset.json'):
        with open('dataset.json', 'r') as f:
            data = json.load(f)
    data.append(record)
    with open('dataset.json', 'w') as f:
        json.dump(data, f, indent=2)

st.title("🌾 Crop Disease Detection")
st.markdown("**Apni fasal ke patte ki photo upload karein aur disease detect karein**")

with st.sidebar:
    st.header("📊 Research Info")
    st.info("Yeh platform AI se disease detect karta hai aur data research ke liye save karta hai.")
    if os.path.exists('dataset.json'):
        with open('dataset.json', 'r') as f:
            data = json.load(f)
        st.metric("Total Records", len(data))

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📤 Leaf image upload karein", type=['jpg', 'jpeg', 'png'])
    if uploaded_file:
        image = Image.open(uploaded_file)
   st.image(image, caption="Uploaded Image", use_container_width=True)

with col2:
    if uploaded_file and st.button("🔬 Detect Disease", type="primary"):
        with st.spinner("AI analyze kar raha hai..."):
            model = load_model()
            img_array = preprocess(image)
            preds = model.predict(img_array)[0]
            
            top_idx = np.argmax(preds)
            top_class = CLASSES[top_idx]
            confidence = float(preds[top_idx]) * 100
            
            disease_name = top_class.replace('_', ' ')
            st.success(f"### 🦠 {disease_name}")
            st.metric("Confidence", f"{confidence:.2f}%")
            st.warning(f"**💊 Remedy:** {get_remedy(top_class)}")
            
            st.subheader("📊 Top 3 Predictions")
            top3 = np.argsort(preds)[-3:][::-1]
            for i in top3:
                st.progress(float(preds[i]), text=f"{CLASSES[i].replace('_', ' ')}: {preds[i]*100:.2f}%")
            
            save_data(uploaded_file.name, top_class, confidence)
            st.info("✅ Data research ke liye save ho gaya!")

st.markdown("---")
st.markdown("🌾 **Crop Disease Detection Platform** | PlantVillage Dataset | 38 Disease Classes")
