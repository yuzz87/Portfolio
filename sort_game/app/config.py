import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "app_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME", "sort_portfolio")

    @staticmethod
    def validate():
        required = {
            "DB_HOST": Config.DB_HOST,
            "DB_PORT": Config.DB_PORT,
            "DB_USER": Config.DB_USER,
            "DB_PASSWORD": Config.DB_PASSWORD,
            "DB_NAME": Config.DB_NAME,
        }

        missing = [key for key, value in required.items() if value in (None, "")]
        if missing:
            raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")