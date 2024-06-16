import os

from dotenv import load_dotenv


base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, ".env"))


class Config:
    OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
    CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
    LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    