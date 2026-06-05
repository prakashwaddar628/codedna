import os
from dotenv import load_dotenv

# Find .env relative to the current file (app/core/config.py)
# Up two levels is app/, up three levels is backend/
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
dotenv_path = os.path.join(base_dir, ".env")

# Load environment variables from .env
load_dotenv(dotenv_path)

# Configuration settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./codedna.db")
SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecretkeyfordevonly")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
