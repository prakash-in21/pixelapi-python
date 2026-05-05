# PixelAPI — Official Python SDK

Official Python SDK for [PixelAPI](https://pixelapi.dev) — *AI image, video, audio, and 3D API for builders.*

[![PyPI version](https://badge.fury.io/py/pixelapi.svg)](https://pypi.org/project/pixelapi/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why PixelAPI

- **From $0.001 per image** — image gen $0.001, BG removal $0.010, upscale $0.060, face restore $0.005, object removal $0.025
- **15 AI tools, one API key** — image gen, BG removal, upscale, face restore, object removal, image edit, audio (music), TTS (23 languages), 3D model gen, content moderation, smart-generate, ad creative, image search, portrait studio, interior design, photo relighting
- **No cold starts** — always-warm infrastructure, sub-3-second response on most endpoints
- **100 free credits on signup** — no credit card required
- **GST invoice (India)** — registered Indian business, GST-compliant

## Installation

```bash
pip install pixelapi
```

## Quickstart

```python
from pixelapi import PixelAPI

client = PixelAPI("YOUR_API_KEY")  # get free at https://pixelapi.dev/app

# 1. Generate AI image — $0.001
result = client.generate("product photo of red sneakers, white background, studio lighting")
result.save("sneakers.png")

# 2. Remove background — $0.010
result = client.remove_background("photo.jpg")
result.save("transparent.png")

# 3. Upscale 4× — $0.060
result = client.upscale("photo.jpg", scale=4)
result.save("upscaled.png")

# 4. Restore faces — $0.005
result = client.face_restore("old_family_photo.jpg")
result.save("restored.jpg")
```

## Endpoints

| Method | Description | Price |
|---|---|---|
| `client.generate(prompt)` | AI image gen | $0.001 |
| `client.remove_background(image)` | BG removal → transparent PNG | $0.010 |
| `client.replace_background(image, scene)` | BG replacement (AI scene) | $0.075 |
| `client.upscale(image, scale=4)` | 4× upscaling | $0.060 |
| `client.face_restore(image)` | Face restoration | $0.005 |
| `client.remove_object(image, prompt)` | Object/person removal | $0.025 |
| `client.edit(image, prompt)` | Prompt-driven edit | $0.020 |
| `client.relight(image, preset)` | Photo relighting | $0.018 |
| `client.moderate(image)` | NSFW / content moderation | $0.0005 |
| `client.audio(prompt)` | AI music generation | $0.007 |
| `client.tts(text, voice)` | Text-to-speech (23 langs) | $0.015/30s |
| `client.three_d(prompt)` | 3D model generation (GLB) | $0.50 |

## Pricing

| Plan | Monthly | Credits | Per-image |
|---|---|---|---|
| Free | $0 | 100 | — |
| Starter | $10 | 10,000 | $0.001 avg |
| Pro | $50 | 60,000 | $0.00083 avg |
| Scale | $200 | 300,000 | $0.00067 avg |

## Authentication

```python
client = PixelAPI("YOUR_API_KEY")
# or set PIXELAPI_KEY env var:
# import os; client = PixelAPI(os.environ["PIXELAPI_KEY"])
```

Get your API key at [pixelapi.dev/app](https://pixelapi.dev/app) — 100 free credits, no credit card.

## Errors

```python
from pixelapi import PixelAPI, AuthenticationError, RateLimitError, InsufficientCreditsError

try:
    result = client.remove_background("photo.jpg")
except AuthenticationError:
    print("Invalid API key")
except InsufficientCreditsError:
    print("Out of credits — top up at /app")
except RateLimitError:
    print("Rate limited — slow down or upgrade plan")
```

## Rate limits

- Free: 10 requests / minute
- Starter: 60 / minute
- Pro: 300 / minute
- Scale: unlimited (fair-use)

## Migration from remove.bg / Cloudinary / Replicate

PixelAPI's BG removal is API-compatible with most workflows that take an image input and return a transparent PNG output URL. The migration is typically a 30-minute swap:

```python
# Before (remove.bg)
import requests
r = requests.post("https://api.remove.bg/v1.0/removebg",
    files={"image_file": open("photo.jpg", "rb")},
    headers={"X-API-Key": REMOVEBG_KEY})
open("output.png", "wb").write(r.content)

# After (PixelAPI — 11× cheaper, same output)
from pixelapi import PixelAPI
client = PixelAPI(PIXELAPI_KEY)
client.remove_background("photo.jpg").save("output.png")
```

## Examples

See [`examples/`](examples/) for full code samples:
- Bulk product-photo BG removal (Shopify catalog)
- LinkedIn-headshot generation pipeline
- E-commerce upscale + relight workflow
- Audio-on-demand for video apps

## Support

- Docs: [pixelapi.dev/docs](https://pixelapi.dev/docs)
- API ref: [pixelapi.dev/developers.html](https://pixelapi.dev/developers.html)
- Issues: [GitHub issues](https://github.com/prakash-in21/pixelapi-python/issues)
- Email: support@pixelapi.dev

## License

MIT — see [LICENSE](LICENSE).

---

Built by [PixelAPI](https://pixelapi.dev). Indian business, GST registered.
