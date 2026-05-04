from fastapi import APIRouter, HTTPException
from services.weather import get_weather

router = APIRouter()

@router.get("/brief", summary="Get weather brief",
            description="Returns today's temperature range, humidity, rain forecast by latitude and longitude.")
async def weather_brief(lat: float, lon: float):
    try:
        weather = await get_weather(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return weather