"""Platform listing route."""

from fastapi import APIRouter

router = APIRouter(prefix="/platforms", tags=["platforms"])

_SUPPORTED_PLATFORMS = ["jd", "taobao", "amazon"]


@router.get("")
async def list_platforms() -> list[str]:
    """Return the supported platform names."""
    return _SUPPORTED_PLATFORMS
