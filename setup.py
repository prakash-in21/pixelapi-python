from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pixelapi",
    version="0.2.0",
    author="PixelAPI",
    author_email="support@pixelapi.dev",
    description="AI image processing API: background removal, product photography, FLUX/SDXL generation, upscaling, virtual try-on, object removal, image captioning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pixelapi.dev",
    project_urls={
        "Documentation": "https://pixelapi.dev/docs.html",
        "Tutorials": "https://pixelapi.dev/tutorials/",
        "Dashboard": "https://pixelapi.dev/app/",
        "Source": "https://github.com/prakash-in21/pixelapi-python",
        "Bug Tracker": "https://github.com/prakash-in21/pixelapi-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    keywords=[
        "background removal", "remove background", "image processing",
        "AI image API", "product photography", "image generation",
        "FLUX", "SDXL", "stable diffusion", "upscaling", "virtual try-on",
        "object removal", "face restoration", "image captioning",
        "ecommerce automation", "product photo", "BiRefNet", "Real-ESRGAN"
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "Pillow>=9.0.0",
    ],
    extras_require={
        "async": ["aiohttp>=3.8.0", "aiofiles>=22.1.0"],
    },
)
