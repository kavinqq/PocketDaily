from linebot import LineBotApi
from flask import current_app


line_bot_api = LineBotApi(current_app.config["LINE_CHANNEL_SECRET"])
