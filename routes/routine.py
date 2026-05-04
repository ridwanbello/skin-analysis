from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.routine import (
    generate_skincare_routine,
    generate_outfit_suggestions,
    generate_weather_brief
)
from services.weather import get_weather
from services.perfectcorp import analyze_skin
from fastapi import UploadFile, File

router = APIRouter()

class SkinConcerns(BaseModel):
    acne: dict | None = None
    age_spot: dict | None = None
    moisture: dict | None = None
    oiliness: dict | None = None
    redness: dict | None = None
    texture: dict | None = None

@router.post("/daily" , summary="Get daily routine",
             description="Combines skin analysis and weather data to generate a personalized skincare routine and outfit suggestions.",
             responses={
        200: {
            "description": "Successful daily routine",
            "content": {
                "application/json": {
                    "example": {
                        "weather_brief": "Today's temperature ranges from 18.0°C to 34.0°C with light rain. Rain is expected — plan accordingly.",
                        "weather": {
                            "temp_min": 18.0,
                            "temp_max": 34.0,
                            "temp_current": 22.1,
                            "humidity": 35,
                            "has_rain": True,
                            "has_storm": False
                        },
                        "skin_concerns": {
                            "acne": {"ui_score": 99, "raw_score": 100.0},
                            "redness": {"ui_score": 76, "raw_score": 68.3}
                        },
                        "skincare_routine": [
                            "Gentle cleanser — cleanse morning and night",
                            "Niacinamide serum — reduces acne and controls oil production",
                            "SPF 50 sunscreen — high UV expected today, reapply every 2 hours",
                            "Waterproof mascara and setting spray — rain expected today"
                        ],
                        "outfit_suggestions": [
                            "Light breathable fabrics — it will be hot today (linen or cotton)",
                            "Big temperature swing today (18.0°C → 34.0°C) — wear removable layers",
                            "Rain expected — waterproof jacket or umbrella recommended"
                        ]
                    }
                }
            }
        },
        500: {
            "description": "Routine generation failed",
            "content": {
                "application/json": {
                    "examples": {
                        "weather_error": {
                            "summary": "Weather fetch failed",
                            "value": {"detail": "Weather error: Client error 401 Unauthorized"}
                        },
                        "skin_error": {
                            "summary": "Skin analysis failed",
                            "value": {"detail": "Skin analysis error: error_no_face detected"}
                        }
                    }
                }
            }
        }
    })
async def daily_routine(
    lat: float,
    lon: float,
    file: UploadFile = File(...)
):
    # Step 1: Get weather
    try:
        weather = await get_weather(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather error: {str(e)}")

    # Step 2: Analyze skin
    try:
        image_bytes = await file.read()
        raw_result = await analyze_skin(image_bytes)

        skin_concerns = {}
        for item in raw_result.get("output", []):
            concern_type = item.get("type")
            if concern_type:
                skin_concerns[concern_type] = {
                    "ui_score": item.get("ui_score"),
                    "raw_score": item.get("raw_score")
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skin analysis error: {str(e)}")

    # Step 3: Generate combined brief
    return {
        "weather_brief": generate_weather_brief(weather),
        "weather": weather,
        "skin_concerns": skin_concerns,
        "skincare_routine": generate_skincare_routine(skin_concerns, weather),
        "outfit_suggestions": generate_outfit_suggestions(weather)
    }