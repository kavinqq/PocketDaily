import os
from linebot import LineBotApi


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_SECRET"))