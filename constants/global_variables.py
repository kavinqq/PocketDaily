from linebot import LineBotApi
from flask import current_app


class LazyLineBotApi:
    def __init__(self):
        self._api = None

    @property
    def api(self):
        if self._api is None:
            self._api = LineBotApi(current_app.config["LINE_CHANNEL_SECRET"])
            
        return self._api

line_bot_api = LazyLineBotApi()