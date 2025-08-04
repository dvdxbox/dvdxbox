import json
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import urlopen
from zoneinfo import ZoneInfo


class WeatherTimeAvatar:
    """Fetch weather and local time for a given location."""

    GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

    def get_weather_and_time(self, location: str) -> dict:
        # Geocode the location to get coordinates and timezone
        geo_params = urlencode({"name": location, "count": 1})
        with urlopen(f"{self.GEOCODE_URL}?{geo_params}", timeout=10) as resp:
            geo_data = json.load(resp)
        if not geo_data.get("results"):
            raise ValueError(f"Location '{location}' not found")
        result = geo_data["results"][0]
        lat = result["latitude"]
        lon = result["longitude"]
        timezone = result["timezone"]

        # Fetch current weather
        forecast_params = urlencode({"latitude": lat, "longitude": lon, "current_weather": True})
        with urlopen(f"{self.FORECAST_URL}?{forecast_params}", timeout=10) as resp:
            weather_data = json.load(resp).get("current_weather", {})

        # Get local time
        now = datetime.now(ZoneInfo(timezone))

        return {
            "location": result["name"],
            "timezone": timezone,
            "time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": weather_data.get("temperature"),
            "windspeed": weather_data.get("windspeed"),
        }


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        print("Usage: python avatar.py <location>")
        return
    location = " ".join(sys.argv[1:])
    avatar = WeatherTimeAvatar()
    try:
        info = avatar.get_weather_and_time(location)
    except Exception as exc:
        print(f"Error: {exc}")
        return
    print(f"Weather in {info['location']}: {info['temperature']}°C, wind {info['windspeed']} km/h")
    print(f"Local time: {info['time']} ({info['timezone']})")


if __name__ == "__main__":
    main()
