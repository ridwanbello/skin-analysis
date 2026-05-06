from PIL import Image
import io
import httpx
import os
import asyncio

API_KEY = os.getenv("PERFECTCORP_API_KEY")
BASE_URL = "https://yce-api-01.makeupar.com"

async def analyze_skin(image_bytes: bytes, content_type: str = "image/jpeg") -> dict:
    # Resize image if needed
    image = Image.open(io.BytesIO(image_bytes))
    width, height = image.size
    short_side = min(width, height)

    if short_side < 480:
        scale = 480 / short_side
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = image.resize((new_width, new_height), Image.LANCZOS)

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()
    content_type = "image/jpeg"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60) as client:

        # Step 1: Register file
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
        print("Step 1 status:", register_resp.status_code)
        print("Step 1 response:", register_resp.json())
        register_resp.raise_for_status()

        register_data = register_resp.json()
        file_info = register_data["data"]["files"][0]
        file_id = file_info["file_id"]
        upload_url = file_info["requests"][0]["url"]
        upload_headers = file_info["requests"][0]["headers"]

        # Step 2: Upload image
        upload_resp = await client.put(
            upload_url,
            content=image_bytes,
            headers=upload_headers
        )
        print("Step 2 status:", upload_resp.status_code)
        upload_resp.raise_for_status()

        # Step 3: Create task — FIXED: removed duplicate code
        task_resp = await client.post(
            f"{BASE_URL}/s2s/v2.0/task/skin-analysis",
            headers=headers,
            json={
                "src_file_id": file_id,
                "dst_actions": [
                    "acne",
                    "moisture",
                    "oiliness",
                    "pore",
                ],
                "format": "json"
            }
        )
        print("Step 3 status:", task_resp.status_code)
        print("Step 3 response:", task_resp.json())

        if task_resp.status_code != 200:
            raise Exception(f"Task creation failed: {task_resp.json()}")

        task_id = task_resp.json()["data"]["task_id"]

        # Step 4: Poll for results
        for _ in range(10):
            await asyncio.sleep(3)
            result_resp = await client.get(
                f"{BASE_URL}/s2s/v2.0/task/skin-analysis/{task_id}",
                headers=headers
            )
            result = result_resp.json()
            print("Poll status:", result["data"]["task_status"])

            if result["data"]["task_status"] == "success":
                return result["data"]["results"]
            elif result["data"]["task_status"] == "error":
                error_detail = result["data"].get("error", "unknown")
                error_code = result["data"].get("error_code", "unknown")
                raise Exception(f"Skin analysis failed — error: {error_detail}, code: {error_code}")

        raise Exception("Timed out waiting for skin analysis result")