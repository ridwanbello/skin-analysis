import asyncio
from services.routine import (
    generate_skincare_routine,
    generate_outfit_suggestions,
    generate_weather_brief
)

# Mock weather data — no API key needed
mock_weather = {
    "temp_min": 18.0,
    "temp_max": 34.0,
    "temp_current": 22.0,
    "humidity": 35,
    "has_rain": True,
    "has_storm": False,
    "conditions": ["Rain", "Clouds"],
    "summary": "light rain"
}

# Mock skin concerns — use scores from your earlier test
mock_skin = {
    "acne": {"ui_score": 99, "raw_score": 100},
    "age_spot": {"ui_score": 97, "raw_score": 99.1},
    "redness": {"ui_score": 76, "raw_score": 68.3},
    "moisture": {"ui_score": 60, "raw_score": 55.0},
    "oiliness": {"ui_score": 72, "raw_score": 60.7},
    "texture": {"ui_score": 70, "raw_score": 66.3},
}

# Run the generators
print("=== WEATHER BRIEF ===")
print(generate_weather_brief(mock_weather))

print("\n=== SKINCARE ROUTINE ===")
for step in generate_skincare_routine(mock_skin, mock_weather):
    print(f"• {step}")

print("\n=== OUTFIT SUGGESTIONS ===")
for suggestion in generate_outfit_suggestions(mock_weather):
    print(f"• {suggestion}")