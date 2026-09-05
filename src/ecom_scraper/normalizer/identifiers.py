"""Identifier normalization helpers."""


def normalize_platform_id(value: object) -> str:
    """Normalize a platform id into a stripped string."""
    if value is None:
        return ""
    return str(value).strip()
