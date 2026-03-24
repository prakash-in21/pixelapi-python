# PixelAPI Python SDK

Official Python SDK for [PixelAPI](https://pixelapi.dev) — AI image processing that doesn't cost a fortune.

[![PyPI version](https://badge.fury.io/py/pixelapi.svg)](https://pypi.org/project/pixelapi/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What it does

Background removal, AI product photography, image generation, upscaling, virtual try-on, object removal, face restoration, outpainting, image captioning — all through one API. Runs on privately owned GPUs, so no cold starts and no "serverless" unpredictability.

Pricing: $0.001–$0.075 per image depending on operation. Typically 5–10x cheaper than Replicate or fal.ai for the same models.

## Install

```bash
pip install pixelapi
```

## Quickstart

```python
import pixelapi

client = pixelapi.Client(api_key="YOUR_API_KEY")

# Remove background
result = client.remove_background("product.jpg")
print(result.output_url)  # direct link to PNG with transparent background

# Generate image
result = client.generate_image(
    prompt="a minimalist leather wallet on marble surface, product photography",
    model="flux-schnell"
)

# AI product photography (BG removal + new background in one call)
result = client.product_photo(
    image="shoe.jpg",
    preset="white-studio"  # or gradient-light, marble, outdoor
)

# Add realistic shadow
result = client.add_shadow(
    image_url=result.output_url,
    shadow_type="soft",  # soft, hard, natural, floating
    shadow_opacity=0.5
)

# Auto-caption a product image
result = client.caption_image(
    image="product.jpg",
    mode="full"  # returns description + tags + alt text + SEO title
)
print(result.tags)   # ["sneaker", "leather", "black", "casual"]
print(result.caption)  # "Black leather sneaker with white rubber sole..."
```

## Batch processing

No batch API needed — just use threads or async:

```python
import concurrent.futures
from pathlib import Path

images = list(Path("products/").glob("*.jpg"))

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
    results = list(pool.map(client.remove_background, images))

# 500 images × $0.005 = $2.50 total
# remove.bg charges $35–100 for the same
```

## Full API coverage

| Operation | Method | Cost |
|-----------|--------|------|
| Background removal | `remove_background()` | $0.005 |
| Image generation (FLUX/SDXL) | `generate_image()` | $0.001 |
| 4x upscale | `upscale()` | $0.005 |
| AI product photography | `product_photo()` | $0.075 |
| Add shadow | `add_shadow()` | $0.020 |
| Image captioning + tags | `caption_image()` | $0.005 |
| Virtual try-on | `virtual_tryon()` | $0.050 |
| Object removal | `remove_object()` | $0.020 |
| Text removal | `remove_text()` | $0.020 |
| Face restoration | `restore_face()` | $0.005 |
| Outpainting | `outpaint()` | $0.030 |
| Text-to-video (Wan 2.1) | `generate_video()` | TBD |

## Links

- [Full docs](https://pixelapi.dev/docs.html)
- [Tutorials](https://pixelapi.dev/tutorials/)
- [Dashboard + API key](https://pixelapi.dev/app/)
- [Pricing](https://pixelapi.dev/#pricing)

## License

MIT
