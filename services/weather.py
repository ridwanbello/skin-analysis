import httpx
import os

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

async def get_weather(lat: float, lon: float) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/forecast",
            params={
                "lat": lat,
                "lon": lon,
                "appid": API_KEY,
                "units": "metric",
                "cnt": 8  # 8 x 3hr intervals = 24 hours
            }
        )
        response.raise_for_status()
        data = response.json()

    forecasts = data["list"]

    # Extract key weather info for the day
    temps = [f["main"]["temp"] for f in forecasts]
    humidities = [f["main"]["humidity"] for f in forecasts]
    conditions = [f["weather"][0]["main"] for f in forecasts]
    descriptions = [f["weather"][0]["description"] for f in forecasts]

    has_rain = any("Rain" in c for c in conditions)
    has_storm = any("Thunderstorm" in c for c in conditions)

    return {
        "temp_min": round(min(temps), 1),
        "temp_max": round(max(temps), 1),
        "temp_current": round(temps[0], 1),
        "humidity": round(sum(humidities) / len(humidities)),
        "has_rain": has_rain,
        "has_storm": has_storm,
        "conditions": list(set(conditions)),
        "summary": descriptions[0]
    }