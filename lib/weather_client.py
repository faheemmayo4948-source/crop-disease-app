import requests

def get_weather_forecast(city_name):
    # 1. Geocoding
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    try:
        geo_res = requests.get(geo_url).json()
        if not geo_res.get("results"):
            return None, "City not found"
        
        location = geo_res["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        city = location["name"]
        country = location.get("country", "")

        # 2. Current Weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        w_res = requests.get(weather_url).json()
        current = w_res.get("current_weather", {})
        
        temp = current.get("temperature")
        wind = current.get("windspeed")
        
        # Rule-based risk logic
        risk_level = "Low"
        warning = "Weather conditions are currently normal for most crops."
        
        if temp is not None:
            if temp > 32:
                risk_level = "High"
                warning = "High temperature warning! High risk of Heat Stress, Rust, and Pest infestations."
            elif temp < 15:
                risk_level = "Medium"
                warning = "Cool conditions detected. Watch out for Mildew and Fungal infections."

        return {
            "city": city,
            "country": country,
            "temp": temp,
            "wind": wind,
            "risk_level": risk_level,
            "warning": warning
        }, None
    except Exception as e:
        return None, str(e)
