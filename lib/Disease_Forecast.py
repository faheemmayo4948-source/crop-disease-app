import streamlit as st
from lib.weather_client import get_weather_forecast

st.set_page_config(page_title="Disease Forecast - CropGuard", page_icon="🌤️")
st.title("🌤️ Weather & Crop Disease Forecast")

city = st.text_input("City ka naam likhein (e.g. Multan, Lahore, Faisalabad)", "Lahore")

if st.button("Get Forecast"):
    with st.spinner("Weather aur risk data fetch ho raha hai..."):
        weather_data, error = get_weather_forecast(city)
        
    if error:
        st.error(f"Error: {error}")
    elif weather_data:
        st.subheader(f"Weather for {weather_data['city']}, {weather_data['country']}")
        col1, col2 = st.columns(2)
        col1.metric("Temperature", f"{weather_data['temp']} °C")
        col2.metric("Wind Speed", f"{weather_data['wind']} km/h")
        
        st.markdown("---")
        st.subheader("Disease Risk Assessment")
        
        risk = weather_data["risk_level"]
        if risk == "High":
            st.error(f"⚠️ Risk Level: **{risk}**")
        elif risk == "Medium":
            st.warning(f"⚡ Risk Level: **{risk}**")
        else:
            st.success(f"✅ Risk Level: **{risk}**")
            
        st.info(weather_data["warning"])
