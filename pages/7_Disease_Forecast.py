import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from lib.weather_client import get_weather_forecast

st.set_page_config(page_title="Disease Forecast · CropGuard", page_icon="🌤️", layout="centered")

st.title("🌤️ Weather & Disease Risk Forecast")
st.write("Enter your city name to fetch live weather analytics and rule-based fungal/bacterial outbreak risk warnings.")

city_name = st.text_input("Enter City Name (e.g., Lahore, Multan, Faisalabad):", value="Lahore")

if st.button("Check Outbreak Risk", type="primary"):
    with st.spinner(f"Fetching live weather data for {city_name}..."):
        weather_data = get_weather_forecast(city_name)
        
        if weather_data:
            st.success(f"✅ Weather Data Updated for **{weather_data.get('city_name', city_name)}**")
            st.divider()

            col1, col2, col3 = st.columns(3)
            temp = weather_data.get('temperature', 'N/A')
            humidity = weather_data.get('humidity', 'N/A')
            risk = weather_data.get('risk_level', 'Low')

            col1.metric("Temperature", f"{temp} °C")
            col2.metric("Relative Humidity", f"{humidity} %")
            col3.metric("Outbreak Risk Level", risk)

            st.divider()

            if risk == "High Risk":
                st.error("⚠️ **HIGH FUNGAL OUTBREAK RISK DETECTED**\n\nHigh humidity and warm temperatures create optimal conditions for rapid fungal spore germination (e.g., Rust, Blight, Downy Mildew). Proactive protective foliar spray is highly recommended.")
            elif risk == "Moderate Risk":
                st.warning("⚡ **MODERATE DISEASE RISK**\n\nConditions are favorable for leaf spot and mild pathogens. Monitor fields closely and avoid over-irrigation.")
            else:
                st.info("✅ **LOW DISEASE OUTBREAK RISK**\n\nCurrent atmospheric humidity is relatively low. Pathogen pressure is minimal.")
        else:
            st.error("Could not fetch weather data. Please check the city name spelling and try again.")
