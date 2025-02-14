import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde .env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PASSWORD_MIN_LENGTH = int(os.getenv("PASSWORD_MIN_LENGTH", 8))  # Valor por defecto 8 si no está en .env
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")