#!/usr/bin/env python3
"""Example: AI Image Generation with PixelAPI"""

import os
from pixelapi import PixelAPI

# Initialize client
api_key = os.getenv("PIXELAPI_KEY", "your_api_key_here")
client = PixelAPI(api_key)

# Generate image with FLUX
print("Generating image with FLUX Schnell...")
result = client.generate(
    prompt="A minimalist product photo of a smartwatch on marble surface, studio lighting",
    model="flux-schnell",
    width=1024,
    height=1024
)
result.save("generated_flux.png")
print(f"✓ Saved to generated_flux.png")
print(f"  Credits used: {result.credits_used}")

# Generate with SDXL
print("\nGenerating image with SDXL...")
result = client.generate(
    prompt="Professional headshot of a business person, neutral background",
    model="sdxl",
    width=1024,
    height=1024,
    negative_prompt="blurry, low quality, distorted"
)
result.save("generated_sdxl.png")
print(f"✓ Saved to generated_sdxl.png")
