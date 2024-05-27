import os
from linebot import LineBotApi


line_bot_api = LineBotApi(os.getenv("LineToken"))