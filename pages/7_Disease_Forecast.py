import streamlit as st
import pandas as pd
from lib.weather_client import get_weather, assess_disease_risk
from lib.location_client import get_location_widget, read_location_from_query

st.set_page_config(page_title="Disease Forecast · CropGuard", page_icon="🌤️")

st.title("🌤️ Weather-Based Disease Risk")
st.caption(
    "This is a general risk indicator based on weather patterns and common agronomy "
    "rules — not a certified prediction. Always consult a local agriculture expert "
    "for serious cases."
)

st.subheader("📍 Step 1 — Share your field's location")
get_location_widget()
lat, lon = read_location_from_query()

if not lat or not lon:
    st.info("Click the button above to get weather-based risk for your location.")
    st.stop()

st.success(f"Location: {lat:.4f}, {lon:.4f}")

with st.spinner("Fetching weather..."):
    try:
        weather = get_weather(lat, lon)
    except Exception as e:
        st.error(f"Could not fetch weather: {e}")
        st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Temperature", f"{weather['temperature_2m']}°C")
col2.metric("Humidity", f"{weather['relative_humidity_2m']}%")
col3.metric("Precipitation", f"{weather['precipitation']} mm")

st.subheader("🌾 Step 2 — Select your crop")

@st.cache_data
def load_database():
    return pd.read_csv("data/disease_database.csv")

df = load_database()
crop = st.selectbox("Crop", sorted(df["Crop"].unique().tolist()))

st.subheader("⚠️ Risk Assessment")
risks = assess_disease_risk(
    weather["temperature_2m"], weather["relative_humidity_2m"], weather["precipitation"]
)
for disease_type, level, reason in risks:
    color = {"High": "🔴", "Moderate to High": "🟠", "Moderate": "🟡", "Low": "🟢"}.get(level, "⚪")
    st.markdown(f"{color} **{disease_type}** — Risk: *{level}*")
    st.caption(reason)

st.divider()
st.subheader(f"📋 Common diseases to watch for in {crop}")
crop_diseases = df[df["Crop"] == crop]
for _, row in crop_diseases.iterrows():
    with st.expander(row["Disease"]):
        st.write(f"**Symptoms:** {row['Symptoms']}")
        st.write(f"**Treatment:** {row['Treatment']}")
