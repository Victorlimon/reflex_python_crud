from sqlmodel import create_engine
from dotenv import load_dotenv
import os

# Cargar variables desde .env
load_dotenv()

def connect():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    dbname = os.getenv("DB_NAME")

    database_url = f"postgresql+pg8000://{user}:{password}@{host}/{dbname}"
    engine = create_engine(database_url)
    return engine
