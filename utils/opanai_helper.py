import os
from typing import Tuple
from enum import Enum

from openai import OpenAI
from flask import current_app


class ChatGPTModelChoice(Enum):
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"


class OpenAIHelper:
    _instance = None            
    
    def __new__(cls):        
        if cls._instance is None:
            cls._instance = super(OpenAIHelper, cls).__new__(cls)
        return cls._instance    
    
    def __init__(self) -> None:        
        self.client = OpenAI(api_key=current_app.config["OPEN_AI_KEY"])
    
    def dall_e(
        self,
        input_text: str,
        size:str
    ) -> str:
        """回傳

        Args:
            input_text (str): 用戶輸入的文字

        Returns:
            str: 產生的圖片網址
        """        
        
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=input_text,
            size=size,
            n=1
        )
        
        image_url = response.data[0].url.strip()
        
        return image_url
    
    def chat_gpt(
        self,
        input_text: str,
        model=ChatGPTModelChoice.GPT_3_TURBO,
        system_setting_str=None,
        history_messages: list = None
    ) -> Tuple[str, list]:
        """ chat with ChatGPT
        
        Args:
            input_text (str): 用戶輸入的文字
            system_setting_str (str): AI系統設定
            model (ChatGPTModelChoice): ChatGPT model Choice
            
        Returns:
            str: ChatGPT的回應
        """
    
        model = (
            model.value
            if model in ChatGPTModelChoice
            else ChatGPTModelChoice.GPT_3_TURBO.value
        )
            
        
        """GPT API Role
        發送消息的角色
            - system: 用來設置對話的上下文或規則。這些訊息不會被直接顯示給用戶，但會影響AI的行為。
            - user: 角色代表用戶發送的訊息。這些訊息是用戶直接輸入的，並且是 AI 回應的依據。
            - assistant: 代表AI發送的訊息。這些訊息是 AI 直接回應用戶的。
        """
        if history_messages:
            history_messages.append(
                {
                    "role": "user",
                    "content": input_text
                }
            )
            messages = history_messages
        else:
            messages = [
                {
                    "role": "system",
                    "content": system_setting_str
                },
                {
                    "role": "user",
                    "content": input_text
                }
            ]        
        
        # Response Process
        gpt_response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        response_content = gpt_response.choices[0].message.content        
        messages.append(
            {
                "role": "assistant",
                "content": response_content
            }
        )        
        
        return gpt_response.choices[0].message.content, messages
        