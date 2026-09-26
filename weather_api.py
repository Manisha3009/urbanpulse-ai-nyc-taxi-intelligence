
import requests

def get_live_weather():

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 40.7128,
        "longitude": -74.0060,

        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "rain",
            "weather_code",
            "wind_speed_10m"
        ],

        "timezone": "America/New_York"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    return response.json()["current"]
