#!/usr/bin/env python3
"""
Add AI product shadows via PixelAPI
Soft, hard, natural, and floating shadow styles
$0.010/image (5x cheaper than Photoroom)

Tutorial: https://pixelapi.dev/tutorials/product-shadows.html
"""
import requests, time

API_KEY = "YOUR_API_KEY"
BASE = "https://api.pixelapi.dev"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def add_shadow(image_url: str, shadow_type: str = "soft",
               opacity: float = 0.5, blur: int = 20) -> str:
    """Add shadow and return output URL. Cost: $0.010"""
    r = requests.post(
        f"{BASE}/v1/image/add-shadow",
        headers=HEADERS,
        json={
            "image_url": image_url,
            "shadow_type": shadow_type,   # soft | hard | natural | floating
            "shadow_opacity": opacity,    # 0.0 to 1.0
            "shadow_blur": blur,          # 0 (sharp) to 80 (very soft)
            "shadow_offset_x": 8,
            "shadow_offset_y": 12,
        }
    )
    r.raise_for_status()
    gen_id = r.json()["generation_id"]

    for _ in range(60):
        status = requests.get(f"{BASE}/v1/generation/{gen_id}", headers=HEADERS).json()
        if status["status"] == "completed":
            return status["output_url"]
        elif status["status"] == "failed":
            raise Exception(status.get("error", "Shadow generation failed"))
        time.sleep(1)

    raise TimeoutError("Shadow timed out")


if __name__ == "__main__":
    product_url = "https://example.com/sneaker_nobg.png"  # transparent PNG works best

    for style in ["soft", "floating", "hard", "natural"]:
        url = add_shadow(product_url, shadow_type=style, opacity=0.45)
        print(f"  {style:10s}: {url}")

    # Total cost: $0.040 for 4 variants ($0.010 each)
