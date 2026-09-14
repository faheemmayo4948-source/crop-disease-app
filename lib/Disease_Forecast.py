import streamlit as st
import requests
from streamlit_geolocation import streamlit_geolocation

# Page Configuration
st.set_page_config(page_title="Disease Forecast · CropGuard", page_icon="🌤️", layout="centered")

st.title("🌤️ Weather-Based Disease Forecast")
st.write("Aap ki location ke weather forecast ke mutabiq aane wale dino mein crop diseases ka risk detect karein.")

st.divider()

# 1. Location Access Section
st.subheader("📍 Step 1: Location Share Karein")
st.caption("Aap ki jagah ka weather fetch karne ke liye location access zaroori hai.")

location = streamlit_geolocation()

lat, lon = None, None
if location and location.get("latitude"):
    lat = location["latitude"]
    lon = location["longitude"]
    st.success(f"📍 Location captured: **{lat:.4f}, {lon:.4f}**")

st.divider()

# 2. Weather Fetching & Disease Risk Detection Function
def get_weather_forecast(lat, lon):
    # Open-Meteo Free Weather API (No API Key Required)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,relative_humidity_2m_mean,precipitation_sum&timezone=auto"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Weather data fetch karne mein masla aaya: {e}")
    return None

def analyze_disease_risk(avg_temp, avg_humidity, total_rain):
    """
    Weather parameters ke hisab se disease risk detect karne ka rules engine logic.
    """
    risks = []
    
    # High Humidity + Warm Temp = High Blight / Fungal Risk
    if avg_humidity > 70 and 20 <= avg_temp <= 30:
        risks.append({
            "disease": "Late Blight / Fungal Leaf Spot",
            "risk_level": "High 🔴",
            "reason": "Ziyada nami (humidity > 70%) aur darmiyana darja hararat fungal disease ke liye favorable hain."
        })
    
    # High Rain + High Temp = Bacterial Spot / Wilt Risk
    if total_rain > 10 and avg_temp > 25:
        risks.append({
            "disease": "Bacterial Spot / Root Rot",
            "risk_level": "Medium 🟡",
            "reason": "Baarish aur pani khada hone se bacterial infection failne ka khatra hai."
        })
        
    # Low Humidity + High Temp = Mildew / Pest Risk
    if avg_humidity < 40 and avg_temp > 32:
        risks.append({
            "disease": "Powdery Mildew & Insect Attack (Aphids/Mites)",
            "risk_level": "Medium 🟡",
            "reason": "Khushk weather aur garam darja hararat mein keede aur powdery mildew ziyada phailte hain."
        })

    if not risks:
        risks.append({
            "disease": "No Major Disease Outbreak Expected",
            "risk_level": "Low 🟢",
            "reason": "Mausam filhal kisi bari crop disease ke liye favorable nahi hai."
        })

    return risks

# 3. Forecast Execution Section
st.subheader("🔮 Step 2: Weather Disease Forecast")

if lat and lon:
    if st.button("Run Weather Disease Forecast", type="primary"):
        with st.spinner("Fetching 7-day weather forecast and calculating risks..."):
            weather_data = get_weather_forecast(lat, lon)
            
            if weather_data and "daily" in weather_data:
                daily = weather_data["daily"]
                
                # Calculate 7-day averages
                avg_temp = sum(daily["temperature_2m_max"]) / len(daily["temperature_2m_max"])
                avg_humidity = sum(daily["relative_humidity_2m_mean"]) / len(daily["relative_humidity_2m_mean"])
                total_rain = sum(daily["precipitation_sum"])
                
                # Display Weather Summary Metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Avg Max Temp", f"{avg_temp:.1f} °C")
                col2.metric("Avg Humidity", f"{avg_humidity:.0f} %")
                col3.metric("7-Day Rain", f"{total_rain:.1f} mm")
                
                st.divider()
                st.markdown("### ⚠️ Predicted Disease Risks (Next 7 Days)")
                
                # Analyze Risk
                forecast_results = analyze_disease_risk(avg_temp, avg_humidity, total_rain)
                
                for item in forecast_results:
                    st.markdown(f"#### **{item['disease']}** — `{item['risk_level']}`")
                    st.write(f"**Wajah:** {item['reason']}")
                    st.divider()
            else:
                st.error("Weather forecast load nahi ho saka.")
else:
    st.info("👆 Pehle upar diye gaye button se apni location share karein taake forecast nikala ja sake.")
