from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pixelapi",
    version="0.1.0",
    author="PixelAPI",
    author_email="support@pixelapi.dev",
    description="Official Python SDK for PixelAPI - AI Image Processing API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pixelapi/pixelapi-python",
    project_urls={
        "Documentation": "https://pixelapi.dev/docs",
        "Bug Tracker": "https://github.com/pixelapi/pixelapi-python/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": ["pytest", "pytest-cov", "black", "mypy"],
    },
)
