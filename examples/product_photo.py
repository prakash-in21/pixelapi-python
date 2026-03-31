#!/usr/bin/env python3
"""Example: E-commerce product photography workflow"""

import os
from pixelapi import PixelAPI

# Initialize client
api_key = os.getenv("PIXELAPI_KEY", "your_api_key_here")
client = PixelAPI(api_key)

# Step 1: Remove background
print("Step 1: Removing background...")
result = client.remove_background("product.jpg")
nobg_path = "product_nobg.png"
result.save(nobg_path)
print(f"✓ Saved to {nobg_path}")

# Step 2: Replace with professional background
print("\nStep 2: Adding professional background...")
result = client.replace_background(
    image=nobg_path,
    prompt="modern minimalist studio background with soft gradient"
)
result.save("product_studio.png")
print("✓ Saved to product_studio.png")

# Step 3: Add realistic shadow
print("\nStep 3: Adding shadow...")
result = client.add_shadow(
    image="product_studio.png",
    shadow_opacity=0.4,
    shadow_blur=25,
    shadow_offset_x=10,
    shadow_offset_y=15
)
result.save("product_final.png")
print("✓ Saved to product_final.png")

print("\n✓ Product photo ready for e-commerce!")
