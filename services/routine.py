# Product database with Amazon links
PRODUCT_LINKS = {
    "niacinamide": {
        "name": "TruSkin Niacinamide Serum",
        "amazon_url": "https://www.amazon.com/s?k=niacinamide+serum",
        "reason": "Reduces acne and controls oil production"
    },
    "vitamin_c": {
        "name": "TruSkin Vitamin C Serum",
        "amazon_url": "https://www.amazon.com/s?k=vitamin+c+serum+face",
        "reason": "Brightens dark spots and evens skin tone"
    },
    "hyaluronic_acid": {
        "name": "Neutrogena Hyaluronic Acid Serum",
        "amazon_url": "https://www.amazon.com/s?k=hyaluronic+acid+serum",
        "reason": "Deeply hydrates dry skin"
    },
    "rich_moisturizer": {
        "name": "CeraVe Moisturizing Cream",
        "amazon_url": "https://www.amazon.com/s?k=cerave+moisturizing+cream",
        "reason": "Low humidity will dry your skin out today"
    },
    "oil_free_moisturizer": {
        "name": "Neutrogena Oil-Free Moisturizer",
        "amazon_url": "https://www.amazon.com/s?k=oil+free+moisturizer+face",
        "reason": "Lightweight formula for oily skin"
    },
    "cica_cream": {
        "name": "Dr. Jart+ Cicapair Cream",
        "amazon_url": "https://www.amazon.com/s?k=cica+cream+redness",
        "reason": "Calms redness and irritation"
    },
    "aha_bha": {
        "name": "Paula's Choice BHA Exfoliant",
        "amazon_url": "https://www.amazon.com/s?k=aha+bha+exfoliant",
        "reason": "Smooths rough texture"
    },
    "spf_50": {
        "name": "EltaMD UV Clear SPF 46",
        "amazon_url": "https://www.amazon.com/s?k=spf+50+sunscreen+face",
        "reason": "High UV expected today, reapply every 2 hours"
    },
    "spf_30": {
        "name": "Neutrogena Ultra Sheer SPF 30",
        "amazon_url": "https://www.amazon.com/s?k=spf+30+sunscreen+face",
        "reason": "Daily sun protection"
    },
    "cleanser": {
        "name": "CeraVe Hydrating Cleanser",
        "amazon_url": "https://www.amazon.com/s?k=cerave+hydrating+cleanser",
        "reason": "Gentle cleanse morning and night"
    },
    "waterproof_mascara": {
        "name": "Maybelline Waterproof Mascara",
        "amazon_url": "https://www.amazon.com/s?k=waterproof+mascara",
        "reason": "Rain expected today"
    }
}


def generate_skincare_routine(skin_concerns: dict, weather: dict) -> list:
    routine = []
    temp_max = weather["temp_max"]
    humidity = weather["humidity"]
    has_rain = weather["has_rain"]

    # Base routine
    routine.append(PRODUCT_LINKS["cleanser"])

    # Acne
    acne = skin_concerns.get("acne", {})
    if acne and acne.get("ui_score", 100) < 90:
        routine.append(PRODUCT_LINKS["niacinamide"])

    # Dark spots
    age_spot = skin_concerns.get("age_spot", {})
    if age_spot and age_spot.get("ui_score", 100) < 85:
        routine.append(PRODUCT_LINKS["vitamin_c"])

    # Dryness
    moisture = skin_concerns.get("moisture", {})
    if moisture and moisture.get("ui_score", 100) < 75:
        routine.append(PRODUCT_LINKS["hyaluronic_acid"])
    if humidity < 40:
        routine.append(PRODUCT_LINKS["rich_moisturizer"])

    # Oiliness
    oiliness = skin_concerns.get("oiliness", {})
    if oiliness and oiliness.get("ui_score", 100) < 70:
        routine.append(PRODUCT_LINKS["oil_free_moisturizer"])

    # Redness
    redness = skin_concerns.get("redness", {})
    if redness and redness.get("ui_score", 100) < 85:
        routine.append(PRODUCT_LINKS["cica_cream"])

    # Texture
    texture = skin_concerns.get("texture", {})
    if texture and texture.get("ui_score", 100) < 75:
        routine.append(PRODUCT_LINKS["aha_bha"])

    # SPF
    if temp_max >= 25:
        routine.append(PRODUCT_LINKS["spf_50"])
    else:
        routine.append(PRODUCT_LINKS["spf_30"])

    # Rain
    if has_rain:
        routine.append(PRODUCT_LINKS["waterproof_mascara"])

    return routine

OUTFIT_LINKS = {
    "linen_top": {
        "name": "Linen Breathable Top",
        "amazon_url": "https://www.amazon.com/s?k=linen+top+women"
    },
    "light_tshirt": {
        "name": "Light Cotton T-Shirt",
        "amazon_url": "https://www.amazon.com/s?k=light+cotton+tshirt"
    },
    "light_jacket": {
        "name": "Light Layer Jacket",
        "amazon_url": "https://www.amazon.com/s?k=light+jacket+women"
    },
    "warm_coat": {
        "name": "Warm Winter Coat",
        "amazon_url": "https://www.amazon.com/s?k=warm+winter+coat+women"
    },
    "scarf": {
        "name": "Cozy Scarf",
        "amazon_url": "https://www.amazon.com/s?k=cozy+scarf+women"
    },
    "gloves": {
        "name": "Winter Gloves",
        "amazon_url": "https://www.amazon.com/s?k=winter+gloves+women"
    },
    "removable_jacket": {
        "name": "Zip-Up Removable Jacket",
        "amazon_url": "https://www.amazon.com/s?k=zip+up+jacket+women"
    },
    "waterproof_jacket": {
        "name": "Waterproof Rain Jacket",
        "amazon_url": "https://www.amazon.com/s?k=waterproof+rain+jacket+women"
    },
    "umbrella": {
        "name": "Compact Travel Umbrella",
        "amazon_url": "https://www.amazon.com/s?k=compact+travel+umbrella"
    },
}


def generate_outfit_suggestions(weather: dict) -> list:
    suggestions = []
    temp_min = weather["temp_min"]
    temp_max = weather["temp_max"]
    has_rain = weather["has_rain"]
    has_storm = weather["has_storm"]

    temp_diff = temp_max - temp_min

    # Temperature based suggestions
    if temp_max >= 30:
        suggestions.append({
            **OUTFIT_LINKS["linen_top"],
            "reason": "Light breathable fabrics — it will be hot today (linen or cotton)"
        })
    elif temp_max >= 20:
        suggestions.append({
            **OUTFIT_LINKS["light_tshirt"],
            "reason": "Light layers — comfortable t-shirt or blouse weather"
        })
    elif temp_max >= 10:
        suggestions.append({
            **OUTFIT_LINKS["light_jacket"],
            "reason": "Medium layers — bring a jacket for cooler parts of the day"
        })
    else:
        suggestions.append({
            **OUTFIT_LINKS["warm_coat"],
            "reason": "Warm layers — coat recommended"
        })
        suggestions.append({
            **OUTFIT_LINKS["scarf"],
            "reason": "Scarf recommended for cold weather"
        })
        suggestions.append({
            **OUTFIT_LINKS["gloves"],
            "reason": "Gloves recommended for cold weather"
        })

    # Big temperature swing
    if temp_diff >= 10:
        suggestions.append({
            **OUTFIT_LINKS["removable_jacket"],
            "reason": f"Big temperature swing today ({temp_min}°C → {temp_max}°C) — wear removable layers you can adjust throughout the day"
        })

    # Rain / storm
    if has_storm:
        suggestions.append({
            **OUTFIT_LINKS["waterproof_jacket"],
            "reason": "Thunderstorms expected — waterproof jacket essential"
        })
        suggestions.append({
            **OUTFIT_LINKS["umbrella"],
            "reason": "Thunderstorms expected — carry an umbrella and avoid open areas"
        })
    elif has_rain:
        suggestions.append({
            **OUTFIT_LINKS["waterproof_jacket"],
            "reason": "Rain expected — waterproof jacket recommended"
        })
        suggestions.append({
            **OUTFIT_LINKS["umbrella"],
            "reason": "Rain expected — don't forget your umbrella"
        })

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