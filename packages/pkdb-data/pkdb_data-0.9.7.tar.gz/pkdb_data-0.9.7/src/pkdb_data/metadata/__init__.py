"""Working with metadata and annotations."""
from pathlib import Path

from pkdb_data import RESOURCES_DIR

CACHE_USE: bool = True
CACHE_PATH: Path = RESOURCES_DIR / "cache"
