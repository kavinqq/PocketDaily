from constants.global_variables import line_bot_api
from linebot.models import (
    MessageEvent,
    TextSendMessage,
)

def random_int(event: MessageEvent):
    if 
    
    
    
    
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )