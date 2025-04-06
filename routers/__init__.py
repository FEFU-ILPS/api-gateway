from .auth import router as auth_router
from .health import router as health_router
from .texts import router as texts_router

__all__ = ("health_router", "auth_router", "texts_router")
