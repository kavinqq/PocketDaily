import random
from typing import Optional

from linebot.models import (
    MessageEvent,
    TextSendMessage,
)

from utils.user_state_helper import UserStatesHelper
from constants.global_variables import line_bot_api
from models import UserState, UserStateEnum


class RandomInt:
    def __init__(self) -> None:
        self.user_states = UserStatesHelper()
        self.user_state = None
    
    def main(
        self,
        event: MessageEvent,
        user_state: Optional[UserState]
    ) -> None:        
        user_id: str = event.source.user_id
        self.user_state = user_state
        
        if self.user_state.action is None:
            self.stage_0(
                event=event,
                user_id=user_id
            )
            
            return None
              
        data = data if isinstance(user_state.data, dict) else {}
        
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
            
        line_bot_api.api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )        
        
        return None
    
    def stage_0(
        self,
        event: MessageEvent,
        user_id: str
    ) -> None:
        self.user_states.update(
            user_id=user_id,
            action=UserStateEnum.RANDOM_INT.value,
        )
        
        line_bot_api.api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )   
        
        reply_message = "請輸入亂數開始的數字"
        
        return reply_message
        
    def stage_0_to_1(
        self,
        user_id: str,
        message: str
    ) -> str:
        try:
            number = int(message)
        except ValueError:
            reply_message = "請輸入開始數字~"
        else:
            self.user_states.update(
                user_id=user_id,
                action=UserStateEnum.RANDOM_INT.value,
                data={
                    "start": number
                }
            )
            reply_message = f"請輸入結束數字, 我將回傳一個介於{number}這個數字之間的亂數。"
            
        return reply_message

    def stage_1_to_2(
        self,
        user_id: str,
        message: str,
        start: int
    ) -> str:
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
                
                self.user_state.update(
                    user_id=user_id,
                )
                
        return reply_message
