import os

from dotenv import load_dotenv


base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(
    dotenv_path=os.path.join(base_dir, ".env"),
    override=True,
)


class Config:
    OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
    CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
    LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'
