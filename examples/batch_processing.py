#!/usr/bin/env python3
"""
Batch process product images with PixelAPI
Full pipeline: background removal + shadow = $0.015/image

500 images = $7.50 total (vs remove.bg $35–100+)

Get your free API key: https://pixelapi.dev/app/
Tutorial: https://pixelapi.dev/tutorials/batch-processing.html
"""
import requests
import concurrent.futures
import time
from pathlib import Path

API_KEY = "YOUR_API_KEY"
BASE_URL = "https://api.pixelapi.dev"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def wait_for_job(gen_id: str, timeout: int = 120) -> dict:
    for _ in range(timeout):
        r = requests.get(f"{BASE_URL}/v1/generation/{gen_id}", headers=HEADERS)
        data = r.json()
        if data["status"] in ("completed", "failed"):
            return data
        time.sleep(1)
    raise TimeoutError(f"Job timed out")


def remove_background(img_path) -> str:
    with open(img_path, "rb") as f:
        r = requests.post(
            f"{BASE_URL}/v1/image/remove-background",
            headers=HEADERS,
            files={"image": f},
            data={"output_format": "png"}
        )
    result = wait_for_job(r.json()["generation_id"])
    return result["output_url"]


def add_shadow(image_url: str, shadow_type: str = "soft") -> str:
    r = requests.post(
        f"{BASE_URL}/v1/image/add-shadow",
        headers=HEADERS,
        json={
            "image_url": image_url,
            "shadow_type": shadow_type,   # soft | hard | natural | floating
            "shadow_opacity": 0.45,
            "shadow_blur": 18,
        }
    )
    result = wait_for_job(r.json()["generation_id"])
    return result["output_url"]


def product_pipeline(img_path) -> str:
    """Remove BG → Add shadow → Download. Cost: $0.015/image"""
    img_path = Path(img_path)
    nobg_url = remove_background(img_path)
    final_url = add_shadow(nobg_url)
    out_path = Path("output") / f"{img_path.stem}_final.png"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_bytes(requests.get(final_url).content)
    print(f"  done: {img_path.name}")
    return str(out_path)


if __name__ == "__main__":
    images = list(Path("products/").glob("*.jpg"))
    print(f"Processing {len(images)} images... (${len(images) * 0.015:.2f} total)")
    
    Path("output").mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        list(pool.map(product_pipeline, images))
    
    print(f"Done. Results in output/")
