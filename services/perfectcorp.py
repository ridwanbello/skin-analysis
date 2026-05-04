from PIL import Image
import io
import httpx
import os

API_KEY = os.getenv("PERFECTCORP_API_KEY")
BASE_URL = "https://yce-api-01.makeupar.com"

async def analyze_skin(image_bytes: bytes, content_type: str = "image/jpeg") -> dict:
    image = Image.open(io.BytesIO(image_bytes))
    
    # Ensure short side is at least 480px
    width, height = image.size
    short_side = min(width, height)
    
    if short_side < 480:
        scale = 480 / short_side
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = image.resize((new_width, new_height), Image.LANCZOS)
    
    # Convert back to bytes
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()
    content_type = "image/jpeg"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60) as client:

        # Step 1: Register the file, get pre-signed upload URL
        file_size = len(image_bytes)
        register_resp = await client.post(
            f"{BASE_URL}/s2s/v2.0/file/skin-analysis",
            headers=headers,
            json={
                "files": [
                    {
                        "content_type": content_type,
                        "file_name": "selfie.jpg",
                        "file_size": file_size
                    }
                ]
            }
        )
        register_resp.raise_for_status()
        register_data = register_resp.json()

        file_info = register_data["data"]["files"][0]
        file_id = file_info["file_id"]
        upload_url = file_info["requests"][0]["url"]
        upload_headers = file_info["requests"][0]["headers"]

        # Step 2: Upload the actual image to the pre-signed URL
        upload_resp = await client.put(
            upload_url,
            content=image_bytes,
            headers=upload_headers
        )
        upload_resp.raise_for_status()

        # Step 3: Create the skin analysis task
        task_resp = await client.post(
            f"{BASE_URL}/s2s/v2.0/task/skin-analysis",
            headers=headers,
            json={
                "src_file_id": file_id,
                "dst_actions": ["acne", "moisture", "oiliness", "redness", "texture", "pore", "age_spot"],
                "format": "json"
            }
        )
        task_resp.raise_for_status()
        task_id = task_resp.json()["data"]["task_id"]
        task_resp.raise_for_status()
        task_data = task_resp.json()
        print("Task created:", task_data)  # ← check your terminal for this
        task_id = task_data["data"]["task_id"]

        # Step 4: Poll for results
        import asyncio
        for _ in range(10):
            await asyncio.sleep(3)
            result_resp = await client.get(
                f"{BASE_URL}/s2s/v2.0/task/skin-analysis/{task_id}",
                headers=headers
            )
            result = result_resp.json()
            if result["data"]["task_status"] == "success":
                return result["data"]["results"]
            elif result["data"]["task_status"] == "error":
                error_detail = result["data"].get("error", "unknown")
                error_code = result["data"].get("error_code", "unknown")
                raise Exception(f"Skin analysis failed — error: {error_detail}, code: {error_code}")

        raise Exception("Timed out waiting for skin analysis result")