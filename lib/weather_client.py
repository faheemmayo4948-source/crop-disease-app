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


def assess_disease_risk(temperature, humidity, precipitation):
    """Simple rule-based risk assessment — not a scientific model, just general agronomy patterns."""
    risks = []

    if humidity >= 80 and temperature >= 20:
        risks.append(("Fungal diseases (blight, mildew, rust)", "High",
                       "Warm + very humid conditions favor fungal spore growth."))
    elif humidity >= 60 and temperature >= 15:
        risks.append(("Fungal diseases (blight, mildew)", "Moderate",
                       "Humid conditions can support fungal development."))

    if precipitation > 0 and humidity >= 70:
        risks.append(("Bacterial diseases (leaf blight, wilt)", "Moderate to High",
                       "Wet leaves and standing moisture help bacteria spread."))

    if temperature >= 30 and humidity < 40:
        risks.append(("Heat/drought stress", "Moderate",
                       "Hot, dry conditions can weaken plants and increase pest vulnerability."))

    if not risks:
        risks.append(("No major risk pattern detected", "Low",
                       "Current conditions don't strongly favor common disease triggers."))

    return risks
