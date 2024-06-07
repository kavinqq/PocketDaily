from typing import Union

from linebot.models import (
    MessageEvent,
    TextSendMessage,
    ImageSendMessage,
)

from utils.user_states import UserStates
from utils.opanai_helper import OpenAIHelper
from constants.global_variables import line_bot_api


class AdventureGame:
    def __init__(self) -> None:
        self.action = "adventure_game"
        self.user_states = UserStates()       
        self.open_ai_helper = OpenAIHelper() 
        self.default_prompt = """
            請開始一個文字冒險遊戲。
            由你來描述遊戲場景，由玩家來決定要採取的動作，每次你描述完場景之後，
            請根據你的描述產生一張圖。
            請詳細描述場景中所有的物品、生物，如果場景中的人物在對話或跟主角對話，
            請把對話內容完整說出來，如果主角和場景中的任何生物互動，
            請把互動過程詳細描述出來，不要出現重複的場景或對話，
            故事要曲折離奇、高潮迭起、引人入勝。
        """
        self.user_id = None
        
    def main(self, event: MessageEvent, user_state:Union[dict, None]) -> None:
        self.user_id = event.source.user_id
        
        if user_state is None:
            self.init_game(event)
        else:
            user_input = event.message.text
            
            if str(user_input) not in ("1", "2", "3", "4", "5"):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="請輸入1-5的數字")
                )
                return None
            
            if user_input == "5":
                self.user_states.delete_state(self.user_id)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="遊戲結束!!")
                )
                return None            
            
            user_input = f"我選擇選項{user_input}"
            response, history_messages = self.open_ai_helper.chat_gpt(
                input_text=user_input,
                history_messages=history_messages,
            )
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"{response}\n產生圖片需要一點時間，請稍等")
            )
            
            self.gen_reply(event, response)
            
            return None
            
        
    def init_game(self, event: MessageEvent) -> None:
        response, history_messages = self.open_ai_helper.chat_gpt(
            system_setting_str=self.default_prompt,
            input_text="請在每一段故事結束時附上五個接續選項，選項五固定是離開遊戲。遊戲開始!"
        )
        
        self.user_states.edit_state(
            user_id=self.user_id,
            action=self.action,
            data=None,
            history_messages=history_messages            
        )        
        
        self.gen_reply(event, response)
        
        return None
    
    def gen_reply(self, event: MessageEvent, response: str) -> None:
        picture_url = self.open_ai_helper.dall_e(
            input_text=response,
            size="256x256"
        )
        
        image_message = ImageSendMessage(
            original_content_url=picture_url,
            preview_image_url=picture_url,
        )
        
        line_bot_api.push_message(
            self.user_id,
            image_message
        )        
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"{response}\n\n產生圖片需要一點時間，請稍等")
        )
        line_bot_api.push_message(
            self.user_id,
            image_message,
            timeout=60
        )            
        
        return None