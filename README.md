# PixelAPI - AI Image Processing API | Background Removal, Upscaling, Generation

Official Python SDK for [PixelAPI](https://pixelapi.dev) — **2x cheaper than alternatives. Powered by bare-metal GPUs.**

[![PyPI version](https://badge.fury.io/py/pixelapi.svg)](https://pypi.org/project/pixelapi/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why PixelAPI?

- **50% cheaper** than Remove.bg, Cloudinary AI, Replicate
- **Bare-metal GPUs** — no cold starts, consistent speed
- **One API** for background removal, upscaling, generation, object removal, face restoration
- **No usage limits** — process 10,000+ images/day with no throttling
- **Simple pricing** — $0.001–$0.05 per operation, no monthly fees

## Alternatives to Remove.bg & Cloudinary

| Service | Background Removal | 4x Upscale | Image Generation |
|---------|-------------------|------------|------------------|
| PixelAPI | $0.005 | $0.005 | $0.001 |
| Remove.bg | $0.09 | N/A | N/A |
| Cloudinary AI | $0.10 | $0.15 | N/A |
| Replicate | $0.012 | $0.012 | $0.003 |

## Installation

```bash
pip install pixelapi
```

## Quick Start

```python
from pixelapi import PixelAPI

client = PixelAPI("your_api_key")

# Remove background
result = client.remove_background("product.jpg")
result.save("output.png")

# Generate image
result = client.generate("A sunset over mountains", model="flux-schnell")
result.save("generated.png")

# Upscale 4x
result = client.upscale("photo.jpg", scale=4)
result.save("upscaled.png")
```

## Features

### Background Removal
```python
# Remove background → transparent PNG
result = client.remove_background("product.jpg")

# Replace with new background
result = client.replace_background(
    image="person.jpg",
    background="beach.jpg"
)

# Or generate background from text
result = client.replace_background(
    image="person.jpg",
    prompt="professional office background"
)
```

### Image Generation
```python
result = client.generate(
    prompt="minimalist product photo of a watch",
    model="flux-schnell",  # or "sdxl"
    width=1024,
    height=1024,
    negative_prompt="blurry, low quality"
)
result.save("generated.png")
```

### Image Enhancement
```python
# 4x upscaling
result = client.upscale("photo.jpg", scale=4)

# Face restoration
result = client.restore_face("old_photo.jpg")
```

### Object Manipulation
```python
# Remove unwanted objects
result = client.remove_object(
    image="photo.jpg",
    mask="mask.png"  # white = remove
)

# Remove text/watermarks
result = client.remove_text("watermarked.jpg")
```

### Advanced Features
```python
# Add realistic shadow
result = client.add_shadow(
    image="product.png",
    shadow_opacity=0.5,
    shadow_blur=20
)

# Extend image borders (outpainting)
result = client.outpaint(
    image="photo.jpg",
    direction="all",
    pixels=256,
    prompt="continue the landscape"
)
```

### Batch Processing
```python
# Process multiple images efficiently
batch = client.batch(
    operation="remove-bg",
    images=["photo1.jpg", "photo2.jpg", "photo3.jpg"]
)

# Wait for completion
results = batch.wait()
for i, result in enumerate(results):
    result.save(f"output_{i}.png")
```

### Account Management
```python
# Check usage and credits
usage = client.get_usage()
print(f"Credits remaining: {usage['credits_remaining']}")
print(f"Credits used this month: {usage['credits_used']}")

# List available models
models = client.get_models()
print(models)
```

## Examples

See the [examples/](examples/) directory for complete working examples:

- `remove_background.py` - Basic background removal
- `generate_images.py` - Text-to-image generation
- `batch_processing.py` - Process multiple images
- `product_photo.py` - E-commerce product photography workflow

## API Reference

### Methods

- `remove_background(image)` - Remove image background
- `replace_background(image, background=None, prompt=None)` - Replace background
- `generate(prompt, model, width, height, ...)` - Generate image from text
- `upscale(image, scale)` - Upscale image 2x or 4x
- `restore_face(image)` - Restore and enhance faces
- `remove_object(image, mask)` - Remove objects using mask
- `remove_text(image)` - Remove text/watermarks
- `add_shadow(image, shadow_opacity, ...)` - Add realistic shadow
- `outpaint(image, direction, pixels, prompt)` - Extend image borders
- `batch(operation, images, **kwargs)` - Batch processing
- `get_usage()` - Get credit usage
- `get_models()` - List available models

### Image Input

All methods accept images as:
- File path: `"photo.jpg"`
- URL: `"https://example.com/image.jpg"`
- Bytes: `open("photo.jpg", "rb").read()`
- Base64 string

### Error Handling

```python
from pixelapi import PixelAPI, PixelAPIError, AuthenticationError, RateLimitError

try:
    result = client.remove_background("photo.jpg")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded")
except PixelAPIError as e:
    print(f"API error: {e.message}")
```

## Pricing

| Operation | Cost | Remove.bg | Cloudinary |
|-----------|------|-----------|------------|
| Background removal | $0.005 | $0.09 | $0.10 |
| Image generation | $0.001 | N/A | N/A |
| 4x upscale | $0.005 | N/A | $0.15 |
| Face restoration | $0.005 | N/A | $0.12 |
| Object removal | $0.020 | N/A | $0.10 |

No monthly fees. No usage limits. Pay only for what you use.

## Get API Key

1. Visit [https://pixelapi.dev/app/](https://pixelapi.dev/app/)
2. Sign up (free tier includes 100 credits)
3. Copy your API key from dashboard

## Links

- 🌐 [Website](https://pixelapi.dev)
- 📚 [Documentation](https://pixelapi.dev/docs)
- 🔑 [Get API Key](https://pixelapi.dev/app/)
- 💬 [Discord Community](https://discord.gg/pixelapi)

## License

MIT

---

**Keywords**: background removal, image upscaling, AI image generation, object removal, face restoration, image processing API, remove.bg alternative, cloudinary alternative, replicate alternative, AI image API
