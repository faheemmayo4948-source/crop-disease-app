import streamlit as st
import pandas as pd
from streamlit_geolocation import streamlit_geolocation
from lib.detect_disease import detect_disease
from lib.spray_guide import get_spray_recommendation
from lib.weather_client import (
    geocode_city, reverse_geocode, get_weather,
    get_weekly_forecast, assess_disease_risk, predict_next_diseases,
)

st.set_page_config(page_title="Detect Disease · CropGuard", page_icon="🔍")

st.title("🔍 Detect a crop disease")
st.write("Upload a photo of the affected leaf to get a likely diagnosis.")

crop_name = st.text_input("Crop name*", placeholder="e.g. Wheat, Cotton, Rice")
uploaded_file = st.file_uploader("Leaf photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded leaf", use_container_width=True)

    if st.button("Run detection", type="primary"):
        if not crop_name:
            st.error("Please enter the crop name first.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    image_bytes = uploaded_file.getvalue()
                    content_type = uploaded_file.type or "image/jpeg"
                    predictions = detect_disease(image_bytes, content_type)
                    st.session_state["last_predictions"] = predictions
                    st.session_state["last_crop"] = crop_name
                except Exception as e:
                    st.error(f"Detection failed: {e}")

# --- Show diagnosis result ---
if "last_predictions" in st.session_state:
    predictions = st.session_state["last_predictions"]
    crop_for_result = st.session_state.get("last_crop", "")

    if not predictions:
        st.warning("No disease detected with confidence — the leaf may be healthy, or try a clearer photo.")
    else:
        st.success("Diagnosis complete")
        st.subheader("Likely diagnosis")
        top_disease = predictions[0]["label"]

        for pred in predictions[:3]:
            label = pred.get("label", "Unknown")
            score = pred.get("score", 0) * 100
            st.write(f"**{label}** — {score:.1f}%")
            st.progress(min(int(score), 100))

        # --- Treatment suggestion ---
        st.divider()
        st.subheader("💊 Suggested treatment")
        try:
            rec = get_spray_recommendation(top_disease)
            st.markdown(f"**Category:** {rec['category']}")
            st.markdown(f"**Treatment type:** {rec['treatment_class']}")
            st.markdown(f"**Guidance:** {rec['guidance']}")
            st.markdown(f"**Best timing:** {rec['timing']}")
            st.error(f"**Precautions:** {rec['precautions']}")
            st.caption(
                "⚠️ General guidance only — confirm exact product and dosage with your "
                "local agriculture store or extension officer."
            )
        except Exception as e:
            st.warning(f"Could not load treatment suggestions: {e}")

        # --- Weather + next disease forecast, shown automatically ---
        st.divider()
        st.subheader("🌤️ Weather & What Might Come Next")
        st.caption("Tap the pin to auto-detect your location, or type your city manually.")

        location = streamlit_geolocation()
        lat, lon, display_name = None, None, None

        if location and location.get("latitude"):
            lat = location["latitude"]
            lon = location["longitude"]
            with st.spinner("Detecting city..."):
                display_name = reverse_geocode(lat, lon)
        else:
            city_input = st.text_input("Or type your city/area", placeholder="e.g. Multan, Faisalabad, Lahore")
            if city_input:
                with st.spinner("Finding location..."):
                    try:
                        lat, lon, display_name = geocode_city(city_input)
                    except Exception as e:
                        st.error(f"Could not fetch location: {e}")

        if lat is not None:
            st.success(f"📍 {display_name}")

            try:
                current = get_weather(lat, lon)
                col1, col2, col3 = st.columns(3)
                col1.metric("Temperature", f"{current['temperature_2m']}°C")
                col2.metric("Humidity", f"{current['relative_humidity_2m']}%")
                col3.metric("Precipitation", f"{current['precipitation']} mm")

                risks = assess_disease_risk(
                    current["temperature_2m"], current["relative_humidity_2m"], current["precipitation"]
                )

                st.subheader("⚠️ Next disease risk for this crop")

                @st.cache_data
                def load_database():
                    return pd.read_csv("data/disease_database.csv")

                df = load_database()
                crop_disease_list = df[df["Crop"].str.lower() == crop_for_result.lower()]["Disease"].tolist()

                next_diseases = predict_next_diseases(crop_disease_list, risks)

                if next_diseases:
                    for d in next_diseases:
                        st.warning(f"⚠️ **{d}** — current weather conditions may favor this disease next")
                else:
                    st.info("No specific elevated disease risk detected for this crop right now.")

                with st.expander("See general weather-based risk breakdown"):
                    for label, level, reason, _ in risks:
                        color = {"High": "🔴", "Moderate to High": "🟠", "Moderate": "🟡", "Low": "🟢"}.get(level, "⚪")
                        st.markdown(f"{color} **{label}** — Risk: *{level}*")
                        st.caption(reason)

            except Exception as e:
                st.error(f"Could not fetch weather: {e}")

            try:
                weekly = get_weekly_forecast(lat, lon)
                with st.expander("📅 7-day weather outlook"):
                    for day in weekly:
                        cond = "🌧️ Rain expected" if day["precipitation"] > 1 else "☀️ Dry"
                        st.write(
                            f"{day['date']}: {day['temp_min']:.0f}°–{day['temp_max']:.0f}°C, "
                            f"humidity {day['humidity']:.0f}%, {cond}"
                        )
            except Exception as e:
                st.error(f"Could not fetch 7-day forecast: {e}")
