def generate_skincare_routine(skin_concerns: dict, weather: dict) -> list:
    routine = []
    temp_max = weather["temp_max"]
    humidity = weather["humidity"]
    has_rain = weather["has_rain"]

    # Base routine always included
    routine.append("Gentle cleanser — cleanse morning and night")

    # Acne
    acne = skin_concerns.get("acne", {})
    if acne and acne.get("ui_score", 100) < 80:
        routine.append("Niacinamide serum — reduces acne and controls oil production")

    # Dark spots / age spots
    age_spot = skin_concerns.get("age_spot", {})
    if age_spot and age_spot.get("ui_score", 100) < 85:
        routine.append("Vitamin C serum — brightens dark spots and evens skin tone")

    # Dryness / moisture
    moisture = skin_concerns.get("moisture", {})
    if moisture and moisture.get("ui_score", 100) < 75:
        routine.append("Hyaluronic acid serum — deeply hydrates dry skin")
    if humidity < 40:
        routine.append("Rich moisturizer — low humidity will dry your skin out today")

    # Oiliness
    oiliness = skin_concerns.get("oiliness", {})
    if oiliness and oiliness.get("ui_score", 100) < 70:
        routine.append("Oil-free moisturizer — lightweight formula for oily skin")

    # Redness
    redness = skin_concerns.get("redness", {})
    if redness and redness.get("ui_score", 100) < 75:
        routine.append("Centella Asiatica (Cica) cream — calms redness and irritation")

    # Texture
    texture = skin_concerns.get("texture", {})
    if texture and texture.get("ui_score", 100) < 75:
        routine.append("AHA/BHA exfoliant — smooths rough texture (use 2-3x per week)")

    # SPF based on temperature
    if temp_max >= 25:
        routine.append("SPF 50 sunscreen — high UV expected today, reapply every 2 hours")
    else:
        routine.append("SPF 30 sunscreen — always protect your skin")

    # Rain
    if has_rain:
        routine.append("Waterproof mascara and setting spray — rain expected today")

    return routine


def generate_outfit_suggestions(weather: dict) -> list:
    suggestions = []
    temp_min = weather["temp_min"]
    temp_max = weather["temp_max"]
    has_rain = weather["has_rain"]
    has_storm = weather["has_storm"]

    # Temperature layering advice
    temp_diff = temp_max - temp_min

    if temp_max >= 30:
        suggestions.append("Light, breathable fabrics — it will be hot today (linen or cotton)")
    elif temp_max >= 20:
        suggestions.append("Light layers — comfortable t-shirt or blouse weather")
    elif temp_max >= 10:
        suggestions.append("Medium layers — bring a jacket for cooler parts of the day")
    else:
        suggestions.append("Warm layers — coat, scarf and gloves recommended")

    if temp_diff >= 10:
        suggestions.append(
            f"Big temperature swing today ({temp_min}°C → {temp_max}°C) "
            "— wear removable layers you can adjust throughout the day"
        )

    if has_storm:
        suggestions.append("Thunderstorms expected — carry an umbrella and avoid open areas")
    elif has_rain:
        suggestions.append("Rain expected — waterproof jacket or umbrella recommended")

    return suggestions


def generate_weather_brief(weather: dict) -> str:
    temp_min = weather["temp_min"]
    temp_max = weather["temp_max"]
    temp_current = weather["temp_current"]
    summary = weather["summary"]
    has_rain = weather["has_rain"]

    brief = (
        f"Today's temperature ranges from {temp_min}°C to {temp_max}°C "
        f"with {summary}."
    )

    if has_rain:
        brief += " Rain is expected — plan accordingly."

    return brief