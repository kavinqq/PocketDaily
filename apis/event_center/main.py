
from linebot.models import (
    MessageEvent,
    TextSendMessage,
)

from apis.random_int.main import RandomInt
from apis.adventure_game.main import AdventureGame
from constants.global_variables import line_bot_api

from utils.user_state_helper import UserStatesHelper
from models import UserInputHistory, UserStateEnum
from constants.special import LIKES


class EventCenter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventCenter, cls).__new__(cls)
        return cls._instance

    def handle_event(self, event: MessageEvent):
        message = event.message.text
        user_id = event.source.user_id

        state_helper = UserStatesHelper()
        state_helper.init(user_id=user_id)
        user_state = state_helper.get(user_id=user_id)
        
        UserInputHistory(
            user_state_line_id=user_state.line_id,
            input_text=message
        ).save()        

        if user_state.action is None and any(like in message for like in LIKES):
            line_bot_api.api.reply_message(
                event.reply_token,
                TextSendMessage(text="""
                    不要讓她太孤零零做需求, 但她也需要自己的空間。
                    不要給她太多壓力，但要能幫助她更好。
                    專案要為他留一個位置，要耐心等她。
                    """
                )
            )
        elif "亂數" in message or user_state.action == UserStateEnum.RANDOM_INT.value:            
            random_int = RandomInt()
            random_int.main(event, user_state)
        elif "AdventureTime" in message or user_state.action == UserStateEnum.ADVENTURE_GAME.value:
            adventure_game = AdventureGame()
            adventure_game.main(event, user_state)     
        else:
            line_bot_api.api.reply_message(
                event.reply_token,
                TextSendMessage(text=message)
            )
