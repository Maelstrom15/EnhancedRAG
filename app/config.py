"""Central configuration for paths and embedding setup."""
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = DATA_DIR / "vector_db"

# Ensure directories exist at import time
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
