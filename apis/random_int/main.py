import random
from constants.global_variables import line_bot_api
from linebot.models import (
    MessageEvent,
    TextSendMessage,
)
from utils.user_states import UserStates


class RandomInt:
    def __init__(self) -> None:
        self.user_states = UserStates()        
        
    def main(self, event: MessageEvent, user_state=None) -> None:
        user_id = event.source.user_id
        
        if user_state:
            stage = user_state["stage"]
            
            match stage:
                case 0:
                    reply_message = self.stage_0_to_1(
                        user_id=user_id, 
                        message=event.message.text
                    )                
                case 1:
                    reply_message =self.stage_1_to_2(
                        user_id=user_id,
                        message=event.message.text
                    )
                case _:
                    reply_message = "發生錯誤，請重新輸入。"
        else:    
            reply_message = self.stage_0(user_id)
            
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )        
    
    def stage_0(self, user_id) -> str:
        self.user_states.edit_state(user_id, "random_int", 0)
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
                stage=1,
                data={
                    "start": number
                }
            )
            reply_message = f"請輸入結束數字, 我將回傳一個介於{number}這個數字之間的亂數。"
            
        return reply_message

    def stage_1_to_2(self, user_id, message) -> str:
        try:
            number = int(message)
        except ValueError:
            reply_message = "請輸入結束的數字(要是一個數字呦！)"
        else:
            start = self.user_states.get_state(user_id)["data"]["start"]
            
            if number <= start:
                reply_message = "結束數字必須大於開始數字。\n請輸入結束的數字"
            else:
                random_number = random.randint(start, number)
                reply_message = f"亂數結果為: {random_number}"
                
                self.user_states.delete_state(user_id)
                
        return reply_message
