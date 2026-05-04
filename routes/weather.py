from fastapi import APIRouter, HTTPException
from services.weather import get_weather

router = APIRouter()

@router.get("/brief", summary="Get weather brief",
            description="Returns today's temperature range, humidity, rain forecast by latitude and longitude.",
            responses={
        200: {
            "description": "Successful weather fetch",
            "content": {
                "application/json": {
                    "example": {
                        "temp_min": 18.0,
                        "temp_max": 34.0,
                        "temp_current": 22.1,
                        "humidity": 65,
                        "has_rain": True,
                        "has_storm": False,
                        "conditions": ["Rain", "Clouds"],
                        "summary": "light rain"
                    }
                }
            }
        },
        500: {
            "description": "Weather fetch failed",
            "content": {
                "application/json": {
                    "example": {"detail": "Client error '401 Unauthorized' — invalid API key"}
                }
            }
        }
    }
    )
async def weather_brief(lat: float, lon: float):
    try:
        weather = await get_weather(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return weather