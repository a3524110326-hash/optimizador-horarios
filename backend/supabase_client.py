import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client


# Buscar el archivo .env que está dentro de backend/
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Faltan SUPABASE_URL o SUPABASE_KEY en backend/.env"
    )


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)