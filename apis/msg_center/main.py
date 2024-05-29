from linebot.models import (
    MessageEvent,
    TextSendMessage
)

from apis.random_int.main import RandomInt
from constants.global_variables import line_bot_api

from utils.user_states import UserStates


class EventCenter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventCenter, cls).__new__(cls)
        return cls._instance

    def handle_event(self, event: MessageEvent):
        message = event.message.text
        
        user_states = UserStates()
        user_id = event.source.user_id
        user_state = user_states.get_state(user_id)

        if "亂數" in message or (user_state and user_state["action"] == "random_int"):
            random_int = RandomInt()
            random_int.main(event, user_state)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )            
