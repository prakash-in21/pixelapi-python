"""PixelAPI Client - Main SDK interface"""

import requests
import base64
import time
from pathlib import Path
from typing import Optional, Union, List, Dict, Any
from .exceptions import PixelAPIError, AuthenticationError, RateLimitError, ValidationError, InsufficientCreditsError


class PixelAPI:
    """
    PixelAPI Python SDK
    
    Usage:
        from pixelapi import PixelAPI
        
        client = PixelAPI("your_api_key")
        
        # Remove background
        result = client.remove_background("photo.jpg")
        result.save("output.png")
        
        # Generate image
        result = client.generate("A sunset over mountains", model="flux-schnell")
        result.save("generated.png")
    """
    
    BASE_URL = "https://api.pixelapi.dev"
    
    def __init__(self, api_key: str, base_url: str = None, timeout: int = 120):
        """
        Initialize PixelAPI client.
        
        Args:
            api_key: Your PixelAPI API key
            base_url: Override API base URL (optional)
            timeout: Request timeout in seconds (default: 120)
        """
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "pixelapi-python/0.1.0"
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make API request with error handling"""
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        
        try:
            response = self.session.request(method, url, **kwargs)
        except requests.exceptions.Timeout:
            raise PixelAPIError("Request timed out", status_code=408)
        except requests.exceptions.ConnectionError:
            raise PixelAPIError("Connection failed", status_code=503)
        
        if response.status_code == 401:
            raise AuthenticationError("Invalid API key", status_code=401)
        elif response.status_code == 402:
            raise InsufficientCreditsError("Insufficient credits", status_code=402)
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded", status_code=429)
        elif response.status_code == 422:
            raise ValidationError(response.json().get("detail", "Validation error"), status_code=422)
        elif response.status_code >= 400:
            raise PixelAPIError(f"API error: {response.text}", status_code=response.status_code)
        
        return response.json()
    
    def _load_image(self, image: Union[str, Path, bytes]) -> str:
        """Load image and return base64 string"""
        if isinstance(image, bytes):
            return base64.b64encode(image).decode()
        
        path = Path(image)
        if path.exists():
            return base64.b64encode(path.read_bytes()).decode()
        
        # Assume it's already base64 or a URL
        if image.startswith(("http://", "https://")):
            return image  # API accepts URLs directly
        return image
    
    def _poll_result(self, job_id: str, max_wait: int = 120) -> dict:
        """Poll for async job result"""
        start = time.time()
        while time.time() - start < max_wait:
            result = self._request("GET", f"/v1/jobs/{job_id}")
            if result["status"] == "completed":
                return result
            elif result["status"] == "failed":
                raise PixelAPIError(result.get("error", "Job failed"))
            time.sleep(1)
        raise PixelAPIError("Job timed out")
    
    # ========== Image Generation ==========
    
    def generate(
        self,
        prompt: str,
        model: str = "flux-schnell",
        width: int = 1024,
        height: int = 1024,
        negative_prompt: str = None,
        seed: int = None,
        steps: int = None,
        guidance_scale: float = None
    ) -> "ImageResult":
        """
        Generate an image from text prompt.
        
        Args:
            prompt: Text description of the image
            model: Model to use (flux-schnell, sdxl)
            width: Output width (default: 1024)
            height: Output height (default: 1024)
            negative_prompt: What to avoid in generation
            seed: Random seed for reproducibility
            steps: Number of inference steps
            guidance_scale: How closely to follow prompt
            
        Returns:
            ImageResult with generated image
        """
        payload = {
            "prompt": prompt,
            "model": model,
            "width": width,
            "height": height
        }
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        if seed is not None:
            payload["seed"] = seed
        if steps:
            payload["steps"] = steps
        if guidance_scale:
            payload["guidance_scale"] = guidance_scale
        
        result = self._request("POST", "/v1/image/generate", json=payload)
        return ImageResult(result)
    
    # ========== Background Removal ==========
    
    def remove_background(self, image: Union[str, Path, bytes]) -> "ImageResult":
        """
        Remove background from image.
        
        Args:
            image: Image file path, URL, bytes, or base64 string
            
        Returns:
            ImageResult with transparent background
        """
        payload = {"image": self._load_image(image)}
        result = self._request("POST", "/v1/image/remove-bg", json=payload)
        return ImageResult(result)
    
    def replace_background(
        self,
        image: Union[str, Path, bytes],
        background: Union[str, Path, bytes] = None,
        prompt: str = None
    ) -> "ImageResult":
        """
        Replace image background.
        
        Args:
            image: Foreground image
            background: New background image (optional)
            prompt: Generate background from text (optional)
            
        Returns:
            ImageResult with new background
        """
        payload = {"image": self._load_image(image)}
        if background:
            payload["background"] = self._load_image(background)
        if prompt:
            payload["prompt"] = prompt
        
        result = self._request("POST", "/v1/image/replace-bg", json=payload)
        return ImageResult(result)
    
    # ========== Image Enhancement ==========
    
    def upscale(
        self,
        image: Union[str, Path, bytes],
        scale: int = 4
    ) -> "ImageResult":
        """
        Upscale image resolution.
        
        Args:
            image: Image to upscale
            scale: Scale factor (2 or 4, default: 4)
            
        Returns:
            ImageResult with upscaled image
        """
        payload = {"image": self._load_image(image), "scale": scale}
        result = self._request("POST", "/v1/image/upscale", json=payload)
        return ImageResult(result)
    
    def restore_face(self, image: Union[str, Path, bytes]) -> "ImageResult":
        """
        Restore and enhance faces in image.
        
        Args:
            image: Image with faces to restore
            
        Returns:
            ImageResult with enhanced faces
        """
        payload = {"image": self._load_image(image)}
        result = self._request("POST", "/v1/image/restore-face", json=payload)
        return ImageResult(result)
    
    # ========== Object Manipulation ==========
    
    def remove_object(
        self,
        image: Union[str, Path, bytes],
        mask: Union[str, Path, bytes]
    ) -> "ImageResult":
        """
        Remove object from image using mask.
        
        Args:
            image: Source image
            mask: Mask indicating object to remove (white = remove)
            
        Returns:
            ImageResult with object removed
        """
        payload = {
            "image": self._load_image(image),
            "mask": self._load_image(mask)
        }
        result = self._request("POST", "/v1/image/remove-object", json=payload)
        return ImageResult(result)
    
    def remove_text(self, image: Union[str, Path, bytes]) -> "ImageResult":
        """
        Remove text/watermarks from image.
        
        Args:
            image: Image with text to remove
            
        Returns:
            ImageResult with text removed
        """
        payload = {"image": self._load_image(image)}
        result = self._request("POST", "/v1/image/remove-text", json=payload)
        return ImageResult(result)
    
    # ========== New Features ==========
    
    def add_shadow(
        self,
        image: Union[str, Path, bytes],
        shadow_opacity: float = 0.5,
        shadow_blur: int = 20,
        shadow_offset_x: int = 10,
        shadow_offset_y: int = 10
    ) -> "ImageResult":
        """
        Add realistic shadow to product/object.
        
        Args:
            image: Image with transparent or solid background
            shadow_opacity: Shadow darkness (0-1, default: 0.5)
            shadow_blur: Shadow blur radius (default: 20)
            shadow_offset_x: Horizontal offset (default: 10)
            shadow_offset_y: Vertical offset (default: 10)
            
        Returns:
            ImageResult with shadow added
        """
        payload = {
            "image": self._load_image(image),
            "shadow_opacity": shadow_opacity,
            "shadow_blur": shadow_blur,
            "shadow_offset_x": shadow_offset_x,
            "shadow_offset_y": shadow_offset_y
        }
        result = self._request("POST", "/v1/image/add-shadow", json=payload)
        return ImageResult(result)
    
    def outpaint(
        self,
        image: Union[str, Path, bytes],
        direction: str = "all",
        pixels: int = 256,
        prompt: str = None
    ) -> "ImageResult":
        """
        Extend image beyond its borders.
        
        Args:
            image: Image to extend
            direction: Direction to extend (left, right, up, down, all)
            pixels: Pixels to extend (default: 256)
            prompt: Guide the extension with text
            
        Returns:
            ImageResult with extended image
        """
        payload = {
            "image": self._load_image(image),
            "direction": direction,
            "pixels": pixels
        }
        if prompt:
            payload["prompt"] = prompt
        
        result = self._request("POST", "/v1/image/outpaint", json=payload)
        return ImageResult(result)
    
    # ========== Batch Processing ==========
    
    def batch(
        self,
        operation: str,
        images: List[Union[str, Path, bytes]],
        **kwargs
    ) -> "BatchResult":
        """
        Process multiple images in batch.
        
        Args:
            operation: Operation to perform (remove-bg, upscale, etc.)
            images: List of images (max 100)
            **kwargs: Additional operation parameters
            
        Returns:
            BatchResult for tracking batch progress
        """
        payload = {
            "operation": operation,
            "images": [self._load_image(img) for img in images],
            **kwargs
        }
        result = self._request("POST", "/v1/image/batch", json=payload)
        return BatchResult(self, result["batch_id"])
    
    # ========== Account ==========
    
    def get_usage(self) -> dict:
        """Get current credit usage and balance"""
        return self._request("GET", "/v1/usage")
    
    def get_models(self) -> List[str]:
        """Get list of available models"""
        result = self._request("GET", "/v1/models")
        return result.get("models", [])


class ImageResult:
    """Result from image processing operations"""
    
    def __init__(self, data: dict):
        self.data = data
        self.url = data.get("url") or data.get("output_url")
        self.job_id = data.get("job_id") or data.get("id")
        self.credits_used = data.get("credits_used", 0)
        self.model = data.get("model")
        self._bytes = None
    
    def download(self) -> bytes:
        """Download image bytes"""
        if self._bytes is None:
            response = requests.get(self.url, timeout=30)
            response.raise_for_status()
            self._bytes = response.content
        return self._bytes
    
    def save(self, path: Union[str, Path]) -> Path:
        """Save image to file"""
        path = Path(path)
        path.write_bytes(self.download())
        return path
    
    def __repr__(self):
        return f"ImageResult(url={self.url}, credits={self.credits_used})"


class BatchResult:
    """Result from batch processing"""
    
    def __init__(self, client: PixelAPI, batch_id: str):
        self.client = client
        self.batch_id = batch_id
        self._status = None
        self._results = None
    
    def status(self) -> dict:
        """Get current batch status"""
        self._status = self.client._request("GET", f"/v1/image/batch/{self.batch_id}")
        return self._status
    
    def wait(self, poll_interval: int = 2, max_wait: int = 600) -> List[ImageResult]:
        """Wait for batch to complete and return results"""
        start = time.time()
        while time.time() - start < max_wait:
            status = self.status()
            if status["status"] == "completed":
                self._results = [ImageResult(r) for r in status.get("results", [])]
                return self._results
            elif status["status"] == "failed":
                raise PixelAPIError(f"Batch failed: {status.get('error')}")
            time.sleep(poll_interval)
        raise PixelAPIError("Batch timed out")
    
    def __repr__(self):
        return f"BatchResult(batch_id={self.batch_id})"
