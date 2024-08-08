from sqlmodel import create_engine, SQLModel
from .config import settings

DATABASE_URL = settings.get_database_url()
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True)
