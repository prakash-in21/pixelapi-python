#!/usr/bin/env python3
"""Example: Batch processing with PixelAPI"""

import os
from pathlib import Path
from pixelapi import PixelAPI

# Initialize client
api_key = os.getenv("PIXELAPI_KEY", "your_api_key_here")
client = PixelAPI(api_key)

# Get all images from a directory
input_dir = Path("products")
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

images = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png"))

if not images:
    print("No images found in 'products/' directory")
    exit(1)

print(f"Processing {len(images)} images...")

# Submit batch job
batch = client.batch(
    operation="remove-bg",
    images=[str(img) for img in images]
)

print(f"Batch submitted: {batch.batch_id}")
print("Waiting for completion...")

# Wait for results
results = batch.wait(poll_interval=2, max_wait=300)

# Save all results
for i, result in enumerate(results):
    output_path = output_dir / f"{images[i].stem}_nobg.png"
    result.save(output_path)
    print(f"✓ {output_path}")

print(f"\n✓ Processed {len(results)} images successfully")
