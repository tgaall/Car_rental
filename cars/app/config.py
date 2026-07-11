
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://timurgallamov:454657@localhost:5432/car_rental")
SECRET_KEY = os.getenv("SECRET_KEY", "454657")