from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_db_engine(url):
    if url.startswith("sqlite"):
        return create_engine(url, connect_args={"check_same_thread": False})
    return create_engine(url)

engine = create_db_engine(DATABASE_URL)

# Verify connection; if it fails (e.g. PostgreSQL is not running), fall back to SQLite
if not DATABASE_URL.startswith("sqlite"):
    try:
        with engine.connect() as conn:
            pass
    except Exception as e:
        logger.warning(
            f"Failed to connect to database at {DATABASE_URL}. "
            "Falling back to local SQLite database (sqlite:///./codedna.db). "
            f"Error: {e}"
        )
        DATABASE_URL = "sqlite:///./codedna.db"
        engine = create_db_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)