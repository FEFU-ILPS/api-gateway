from .auth import router as auth_router
from .health import router as health_router
from .texts import router as text_router
from .audio import router as audio_router

__all__ = ("health_router", "auth_router", "text_router", "audio_router")
