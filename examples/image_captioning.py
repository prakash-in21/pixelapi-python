#!/usr/bin/env python3
"""
Auto-generate product descriptions, SEO tags, and alt text from images
$0.005/image — batch your entire catalog for $2.50 per 500 products

Tutorial: https://pixelapi.dev/tutorials/image-captioning.html
"""
import requests, time

API_KEY = "YOUR_API_KEY"
BASE = "https://api.pixelapi.dev"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def caption_product(image_path: str) -> dict:
    """
    Returns:
    - caption: natural language description
    - alt_text: accessibility + SEO alt attribute
    - tags: list of SEO keywords
    - structured.seo_title: SEO title
    - structured.meta_description: meta tag content
    """
    with open(image_path, "rb") as f:
        r = requests.post(
            f"{BASE}/v1/image/caption",
            headers=HEADERS,
            files={"image": f},
            data={"mode": "full", "style": "product", "max_tags": 15}
        )
    r.raise_for_status()
    gen_id = r.json()["generation_id"]

    for _ in range(30):
        status = requests.get(f"{BASE}/v1/generation/{gen_id}", headers=HEADERS).json()
        if status["status"] == "completed":
            return requests.get(status["output_url"]).json()
        time.sleep(1)

    raise TimeoutError("Caption timed out")


if __name__ == "__main__":
    result = caption_product("product.jpg")
    print("Description:", result["caption"])
    print("Alt text:", result["alt_text"])
    print("Tags:", ", ".join(result["tags"]))
    print("SEO title:", result["structured"]["seo_title"])
    # Cost: $0.005
