#!/usr/bin/env python3
"""Example: Background removal with PixelAPI"""

import os
from pixelapi import PixelAPI

# Initialize client
api_key = os.getenv("PIXELAPI_KEY", "your_api_key_here")
client = PixelAPI(api_key)

# Remove background from single image
print("Removing background...")
result = client.remove_background("input.jpg")

# Save result
result.save("output.png")
print(f"✓ Saved to output.png")
print(f"  URL: {result.url}")
print(f"  Credits used: {result.credits_used}")

# Process from URL
print("\nProcessing from URL...")
result = client.remove_background("https://example.com/photo.jpg")
result.save("output_from_url.png")
print(f"✓ Saved to output_from_url.png")
