
from linebot.models import (
    MessageEvent,
    TextSendMessage
)

from apis.random_int.main import RandomInt
from apis.adventure_game.main import AdventureGame
from constants.global_variables import line_bot_api

from utils.user_states import UserStates
from logging_config import logger


LIKES = ["亭妤", "Betty"]


class EventCenter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventCenter, cls).__new__(cls)
        return cls._instance

    def handle_event(self, event: MessageEvent):
        message = event.message.text
        user_id = event.source.user_id

        user_states = UserStates()
        user_state = user_states.get_state(user_id)
        action = user_state.get("action") if user_state else ""

        logger.info(f"User_id:{user_id}\tMessage:{message}\tReply:{event.reply_token}")

        if any(like in message for like in LIKES):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="希望能更瞭解她")
            )
        elif "亂數" in message or action == "random_int":            
            random_int = RandomInt()
            random_int.main(event, user_state)
        elif "圖片遊戲" in message or action == "adventure_game":
            adventure_game = AdventureGame()
            adventure_game.main(event, user_state)
        elif "測試push" in message:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="這是測試reply")
            )
            
            line_bot_api.push_message(
                user_id,
                TextSendMessage(text="這是測試push")
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=message)
            )
