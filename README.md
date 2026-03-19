# PixelAPI Python SDK

Official Python SDK for [PixelAPI](https://pixelapi.dev) - AI-powered image processing API.

[![PyPI version](https://badge.fury.io/py/pixelapi.svg)](https://pypi.org/project/pixelapi/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🎨 **Image Generation** - FLUX, SDXL text-to-image
- ✂️ **Background Removal** - Instant, accurate cutouts
- 🔍 **4x Upscaling** - AI-powered resolution enhancement  
- 👤 **Face Restoration** - Fix blurry/damaged faces
- 🧹 **Object Removal** - Erase unwanted elements
- 📝 **Text Removal** - Remove watermarks/text
- 🌅 **Outpainting** - Extend images beyond borders
- 🎭 **AI Shadows** - Add realistic product shadows
- 📦 **Batch Processing** - Process up to 100 images

## Installation

```bash
pip install pixelapi
```

## Quick Start

```python
from pixelapi import PixelAPI

# Initialize client
client = PixelAPI("your_api_key")

# Remove background
result = client.remove_background("photo.jpg")
result.save("cutout.png")

# Generate image
result = client.generate("A golden retriever on a beach, sunset")
result.save("generated.png")

# Upscale image
result = client.upscale("low_res.jpg", scale=4)
result.save("high_res.png")
```

## Usage Examples

### Background Removal

```python
# From file
result = client.remove_background("product.jpg")

# From URL
result = client.remove_background("https://example.com/image.jpg")

# From bytes
with open("image.png", "rb") as f:
    result = client.remove_background(f.read())

# Save result
result.save("output.png")
print(f"Credits used: {result.credits_used}")
```

### Image Generation

```python
# Basic generation
result = client.generate("A futuristic cityscape at night")

# With parameters
result = client.generate(
    prompt="A serene Japanese garden",
    model="flux-schnell",  # or "sdxl"
    width=1024,
    height=1024,
    negative_prompt="blurry, low quality",
    seed=42
)
```

### Replace Background

```python
# With another image
result = client.replace_background(
    image="portrait.jpg",
    background="beach.jpg"
)

# With AI-generated background
result = client.replace_background(
    image="portrait.jpg",
    prompt="professional office environment"
)
```

### Face Restoration

```python
result = client.restore_face("old_photo.jpg")
result.save("restored.png")
```

### Object Removal

```python
# Remove object using mask
result = client.remove_object(
    image="photo.jpg",
    mask="mask.png"  # White = remove
)
```

### Outpainting (Extend Image)

```python
result = client.outpaint(
    image="landscape.jpg",
    direction="all",  # left, right, up, down, all
    pixels=256,
    prompt="continue the mountain scenery"
)
```

### AI Shadow

```python
result = client.add_shadow(
    image="product.png",
    shadow_opacity=0.5,
    shadow_blur=20,
    shadow_offset_x=10,
    shadow_offset_y=15
)
```

### Batch Processing

```python
# Process multiple images
images = ["img1.jpg", "img2.jpg", "img3.jpg"]
batch = client.batch("remove-bg", images)

# Wait for completion
results = batch.wait()
for i, result in enumerate(results):
    result.save(f"output_{i}.png")
```

### Check Usage

```python
usage = client.get_usage()
print(f"Credits remaining: {usage['credits_remaining']}")
print(f"Credits used: {usage['credits_used']}")
```

## Pricing

| Operation | Credits | ~USD |
|-----------|---------|------|
| Background Removal | 10 | $0.01 |
| Image Generation | 12 | $0.012 |
| Premium Generation | 25 | $0.025 |
| 4x Upscale | 50 | $0.05 |
| Face Restoration | 25 | $0.025 |
| Object Removal | 20 | $0.02 |
| Text Removal | 20 | $0.02 |
| Add Shadow | 10 | $0.01 |
| Outpaint | 25 | $0.025 |

## Error Handling

```python
from pixelapi import PixelAPI, AuthenticationError, InsufficientCreditsError

try:
    result = client.remove_background("image.jpg")
except AuthenticationError:
    print("Invalid API key")
except InsufficientCreditsError:
    print("Not enough credits - top up at pixelapi.dev")
except PixelAPIError as e:
    print(f"API error: {e.message}")
```

## Get API Key

Sign up at [pixelapi.dev](https://pixelapi.dev) to get your free API key with 100 credits.

## Links

- [Documentation](https://pixelapi.dev/docs)
- [API Reference](https://api.pixelapi.dev/docs)
- [Pricing](https://pixelapi.dev/#pricing)
- [GitHub](https://github.com/pixelapi/pixelapi-python)

## License

MIT License - see [LICENSE](LICENSE) for details.
