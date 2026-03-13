import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """アプリケーション設定"""

    DB_HOST = os.getenv("DB_HOST","127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER","root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME","sort_portfolio")

    @staticmethod
    def validate():
        required = [
            Config.DB_HOST,
            Config.DB_PORT,
            Config.DB_USER,
            Config.DB_PASSWORD,
            Config.DB_NAME,
        ]

        if any(v is None for v in required):
            raise RuntimeError("Database environment variables are not set")