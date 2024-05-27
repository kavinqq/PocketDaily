from enum import Enum


class MessageKeywordEnum(Enum):
    RANDOM_NUMBER = "亂數"

    @classmethod
    def list_all_keywords(cls):
        return [keyword.value for keyword in cls]
