"""PixelAPI Exceptions"""

class PixelAPIError(Exception):
    """Base exception for PixelAPI errors"""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

class AuthenticationError(PixelAPIError):
    """Invalid or missing API key"""
    pass

class RateLimitError(PixelAPIError):
    """Rate limit exceeded"""
    pass

class ValidationError(PixelAPIError):
    """Invalid request parameters"""
    pass

class InsufficientCreditsError(PixelAPIError):
    """Not enough credits for operation"""
    pass
