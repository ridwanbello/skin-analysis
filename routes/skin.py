from fastapi import APIRouter, UploadFile, File, HTTPException
from services.perfectcorp import analyze_skin

router = APIRouter()

@router.post("/analyze", summary="Analyze skin from photo", 
             description="Upload a face photo to get skin concern scores including acne, dark spots, redness, texture and more.")
async def analyze(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG or PNG accepted")

    image_bytes = await file.read()

    try:
        result = await analyze_skin(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Parse the output list into a clean dict
    skin_concerns = {}
    overall_score = None

    output = result.get("output", [])
    for item in output:
        concern_type = item.get("type")
        if concern_type:
            skin_concerns[concern_type] = {
                "ui_score": item.get("ui_score"),
                "raw_score": item.get("raw_score"),
                "mask_url": item.get("mask_urls", [None])[0]
            }

    overall_score = result.get("all", {})
    if isinstance(overall_score, dict):
        overall_score = overall_score.get("score")

    return {
        "skin_concerns": skin_concerns,
        "overall_score": overall_score,
        "skin_age": result.get("skin_age")
}