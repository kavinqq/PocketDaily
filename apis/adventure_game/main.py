import logging

from linebot.models import (
    MessageEvent,
    TextSendMessage,
    ImageSendMessage,
)

from utils.user_state_helper import UserStatesHelper
from utils.opanai_helper import OpenAIHelper
from constants.global_variables import line_bot_api
from models import UserState, UserStateEnum


logger = logging.getLogger(__name__)


class AdventureGame:
    def __init__(self) -> None:
        self.user_states = UserStatesHelper()
        self.open_ai_helper = OpenAIHelper()
        self.default_prompt = """
            請模擬一個文字冒險遊戲。
            由你來描述遊戲場景，由玩家來決定要採取的動作，每次你描述完場景之後，
            請根據你的描述產生一張圖。
            請詳細描述場景中所有的物品、生物，如果場景中的人物在對話或跟主角對話，
            請把對話內容完整說出來，如果主角和場景中的任何生物互動，
            請把互動過程詳細描述出來，不要出現重複的場景或對話，
            故事要曲折離奇、高潮迭起、引人入勝。
        """
        self.user_state = None

    def main(
        self,
        event: MessageEvent,
        user_state: UserState
    ) -> None:
        self.user_id = event.source.user_id
        user_input = event.message.text

        self.user_state = user_state
        # Init user state
        if self.user_state.action is None:
            self.init_game(event)
            return None

        # Start game
        if self.user_state.data is None:            
            self.start_game(event)

        # Check user input
        if str(user_input) not in ("1", "2", "3", "4", "5"):
            line_bot_api.api.reply_message(
                event.reply_token,
                TextSendMessage(text="請輸入1-5的數字")
            )
            return None

        # Quit
        if user_input == "5":
            self.user_states.update(
                user_id=self.user_id
            )
            
            line_bot_api.api.reply_message(
                event.reply_token,
                TextSendMessage(text="遊戲結束!! 謝謝您的遊玩 :D")
            )
            return None

        # Continue game
        user_input = f"我選擇選項{user_input}"
        response, history_messages = self.open_ai_helper.chat_gpt(
            input_text=user_input,
            history_messages=self.user_state.history_messages,
        )

        self.user_states.update(
            user_id=self.user_id,
            action=UserStateEnum.ADVENTURE_GAME.value,
            data=self.user_state.data,
            history_messages=history_messages
        )

        self.gen_reply(event, response)

        return None

    def init_game(
        self,
        event: MessageEvent
    ) -> None:
        line_bot_api.api.reply_message(
            event.reply_token,
            TextSendMessage(text="圖文冒險遊戲即將開始!!"),
            TextSendMessage(text="回應速度較慢，請耐心等候 :D"),
            TextSendMessage(text="請輸入冒險主角的名字:"),            
        )

        self.user_states.update(
            user_id=self.user_id,
            action=UserStateEnum.ADVENTURE_GAME.value,
        )

        return None

    def start_game(
        self,
        event: MessageEvent
    ) -> None:
        main_character_name = event.message.text
        
        response, history_messages = self.open_ai_helper.chat_gpt(
            system_setting_str=f"""
                {self.default_prompt}。
                主角的名字是: {main_character_name}。
                
                請在每一段劇情結束時,空一行並且附上五個數字接續選項，選項五固定是離開遊戲。

                範例:
                這是一個森林，你看到一隻狼在吼叫。
                = = = = =
                1. 接近狼
                2. xxx
                3. yy
                4. zzz
                5. 結束遊戲
            """,
            input_text="遊戲開始！"
        )

        self.user_states.update(
            user_id=self.user_id,
            action=UserStateEnum.ADVENTURE_GAME.value,
            data={"name": main_character_name},
            history_messages=history_messages
        )

        self.gen_reply(event, response)

        return None

    def gen_reply(
        self,
        event: MessageEvent,
        response: str,
        
    ) -> None:
        pic_url = self.open_ai_helper.dall_e(
            input_text=f"{response}. 。",
            size="1024x1024"
        )

        line_bot_api.api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=f"{response}"),
                ImageSendMessage(
                    original_content_url=pic_url,
                    preview_image_url=pic_url
                )
            ],
            timeout=60
        )

        return None
