import random
from typing import Union

from linebot.models import (
    MessageEvent,
    TextSendMessage,
)

from utils.user_states import UserStates
from constants.global_variables import line_bot_api


class RandomInt:
    def __init__(self) -> None:
        self.user_states = UserStates()
        self.action = "random_int"
    
    def main(
        self,
        event: MessageEvent,
        user_state: Union[dict, None]
    ) -> None:
        
        user_id = event.source.user_id
        
        if user_state:
            data = user_state.get("data")
            data = data if isinstance(data, dict) else {}
            
            if "start" in data:
                reply_message =self.stage_1_to_2(
                    user_id=user_id,
                    message=event.message.text,
                    start=data["start"]
                )           
            else:
                reply_message = self.stage_0_to_1(
                    user_id=user_id, 
                    message=event.message.text,
                )
        else:
            reply_message = self.stage_0(user_id)
            
        line_bot_api.api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )        
        
        return None
    
    def stage_0(self, user_id) -> str:
        self.user_states.edit_state(
            user_id=user_id,
            action=self.action,
        )
        reply_message = "請輸入亂數開始的數字"
        
        return reply_message
        
    def stage_0_to_1(self, user_id, message) -> str:
        try:
            number = int(message)
        except ValueError:
            reply_message = "請輸入開始的數字(要是一個數字呦！)"
        else:
            self.user_states.edit_state(
                user_id=user_id,
                action="random_int",
                data={
                    "start": number
                }
            )
            reply_message = f"請輸入結束數字, 我將回傳一個介於{number}這個數字之間的亂數。"
            
        return reply_message

    def stage_1_to_2(self, user_id, message, start) -> str:
        try:
            number = int(message)
        except ValueError:
            reply_message = "請輸入結束的數字(要是一個數字呦！)"
        else:
            if number <= start:
                reply_message = "結束數字必須大於開始數字。\n請輸入結束的數字"
            else:
                random_number = random.randint(start, number)
                reply_message = f"亂數結果為: {random_number}"
                
                self.user_states.delete_state(user_id)
                
        return reply_message
