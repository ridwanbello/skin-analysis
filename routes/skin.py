from fastapi import APIRouter, UploadFile, File, HTTPException
from services.perfectcorp import analyze_skin

router = APIRouter()

@router.post("/analyze", summary="Analyze skin from photo", 
             description="Upload a face photo to get skin concern scores including acne, dark spots, redness, texture and more.",
             responses={
        200: {
            "description": "Successful skin analysis",
            "content": {
                "application/json": {
                    "example": {
                        "skin_concerns": {
                            "acne": {"ui_score": 99, "raw_score": 100.0, "mask_url": "https://yce-us.s3.amazonaws.com/...acne_output.png"},
                            "age_spot": {"ui_score": 97, "raw_score": 99.1, "mask_url": "https://yce-us.s3.amazonaws.com/...age_spot_output.png"},
                            "redness": {"ui_score": 76, "raw_score": 68.3, "mask_url": "https://yce-us.s3.amazonaws.com/...redness_output.png"},
                            "texture": {"ui_score": 70, "raw_score": 66.3, "mask_url": "https://yce-us.s3.amazonaws.com/...texture_output.png"},
                            "oiliness": {"ui_score": 72, "raw_score": 60.7, "mask_url": "https://yce-us.s3.amazonaws.com/...oiliness_output.png"},
                        },
                        "overall_score": 75.7,
                        "skin_age": 37
                    }
                }
            }
        },
        400: {
            "description": "Invalid image format",
            "content": {
                "application/json": {
                    "example": {"detail": "Only JPEG or PNG accepted"}
                }
            }
        },
        500: {
            "description": "Skin analysis failed",
            "content": {
                "application/json": {
                    "examples": {
                        "image_too_small": {
                            "summary": "Image too small",
                            "value": {"detail": "Skin analysis failed — error: error_below_min_image_size"}
                        },
                        "no_face": {
                            "summary": "No face detected",
                            "value": {"detail": "Skin analysis failed — error: error_no_face"}
                        },
                        "task_failed": {
                            "summary": "Analysis task failed",
                            "value": {"detail": "Skin analysis task failed"}
                        }
                    }
                }
            }
        }
    }
)
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