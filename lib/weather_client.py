import requests


def geocode_city(city_name):
    """Convert a city/place name into latitude/longitude using free Open-Meteo geocoding."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    if not data.get("results"):
        return None, None, None

    result = data["results"][0]
    lat = result["latitude"]
    lon = result["longitude"]
    display_name = f"{result.get('name', city_name)}, {result.get('country', '')}"
    return lat, lon, display_name


def reverse_geocode(lat, lon):
    """Convert lat/lon coordinates into a city/area name using free OpenStreetMap Nominatim API."""
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"lat": lat, "lon": lon, "format": "json", "zoom": 10}
    headers = {"User-Agent": "CropGuard-App"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        address = data.get("address", {})
        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("county")
            or "Unknown location"
        )
        country = address.get("country", "")
        return f"{city}, {country}" if country else city
    except Exception:
        return "Unknown location"


def get_weather(lat, lon):
    """Fetch current weather using Open-Meteo (free, no API key needed)."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "timezone": "auto",
    }
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    return response.json()["current"]


def get_weekly_forecast(lat, lon):
    """Fetch a 7-day daily forecast: max/min temp, humidity, and rain."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_mean",
        "timezone": "auto",
        "forecast_days": 7,
    }
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    daily = response.json()["daily"]

    days = []
    for i in range(len(daily["time"])):
        days.append({
            "date": daily["time"][i],
            "temp_max": daily["temperature_2m_max"][i],
            "temp_min": daily["temperature_2m_min"][i],
            "humidity": daily["relative_humidity_2m_mean"][i],
            "precipitation": daily["precipitation_sum"][i],
        })
    return days


def assess_disease_risk(temperature, humidity, precipitation):
    """Simple rule-based risk assessment — not a scientific model, just general agronomy patterns."""
    risks = []

    if humidity >= 80 and temperature >= 20:
        risks.append(("Fungal diseases (blight, mildew, rust)", "High",
                       "Warm + very humid conditions favor fungal spore growth.", "Fungal"))
    elif humidity >= 60 and temperature >= 15:
        risks.append(("Fungal diseases (blight, mildew)", "Moderate",
                       "Humid conditions can support fungal development.", "Fungal"))

    if precipitation > 0 and humidity >= 70:
        risks.append(("Bacterial diseases (leaf blight, wilt)", "Moderate to High",
                       "Wet leaves and standing moisture help bacteria spread.", "Bacterial"))

    if temperature >= 30 and humidity < 40:
        risks.append(("Heat/drought stress", "Moderate",
                       "Hot, dry conditions can weaken plants and increase pest vulnerability.", "Pest/Insect"))

    if not risks:
        risks.append(("No major risk pattern detected", "Low",
                       "Current conditions don't strongly favor common disease triggers.", None))

    return risks


def categorize_disease(disease_name: str) -> str:
    """Roughly categorize a disease by keywords in its name."""
    name = disease_name.lower()

    if "virus" in name or "viral" in name or "mosaic" in name or "curl" in name:
        return "Viral"
    if "bacter" in name:
        return "Bacterial"
    if any(keyword in name for keyword in [
        "blight", "mildew", "rust", "rot", "wilt", "anthracnose",
        "scab", "smut", "mold", "mould", "leaf spot", "canker"
    ]):
        return "Fungal"
    if any(keyword in name for keyword in ["mite", "aphid", "borer", "weevil"]):
        return "Pest/Insect"

    return "General"


def predict_next_diseases(crop_diseases, weather_risks):
    """Given a crop's known diseases and today's weather-driven risk categories,
    return which specific diseases are at elevated risk of appearing next."""
    active_categories = {r[3] for r in weather_risks if r[3] is not None}
    matches = []
    for disease_name in crop_diseases:
        if categorize_disease(disease_name) in active_categories:
            matches.append(disease_name)
    return matches
