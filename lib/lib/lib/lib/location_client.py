import streamlit.components.v1 as components
import streamlit as st


def get_location_widget():
    """Renders a button that asks browser permission and returns lat/lon via query params."""
    components.html(
        """
        <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition((position) => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    const url = new URL(window.parent.location);
                    url.searchParams.set('lat', lat);
                    url.searchParams.set('lon', lon);
                    window.parent.location.href = url.toString();
                }, (err) => {
                    document.getElementById('loc-status').innerText = 'Location permission denied.';
                });
            }
        }
        </script>
        <button onclick="getLocation()" style="padding:8px 16px;border-radius:6px;border:none;background:#4C7A5A;color:white;cursor:pointer;">
            📍 Share my location
        </button>
        <p id="loc-status"></p>
        """,
        height=80,
    )


def read_location_from_query():
    """Reads lat/lon that were set in the URL by the widget above."""
    lat = st.query_params.get("lat")
    lon = st.query_params.get("lon")
    if lat and lon:
        return float(lat), float(lon)
    return None, None
