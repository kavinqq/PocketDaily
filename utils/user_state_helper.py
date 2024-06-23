from typing import Union

from models import UserState


class UserStatesHelper:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserStatesHelper, cls).__new__(cls)
                        
        return cls._instance
    
    def init(
        self,
        user_id: str
    ) -> None:
        if UserState.query.get(
            {"line_id": user_id}
        ):
            pass
        else:        
            user_state = UserState(line_id=user_id)       
            user_state.save()

        return None

    def get(
        self,
        user_id: str
    ) -> Union[UserState, None]:        
        return UserState.query.get(
            {
                "line_id": user_id
            }
        ) 

    def update(
        self,
        user_id: str,
        action=None,        
        data=None,
        history_messages=None
    ) -> None:
        user_state: UserState = UserState.query.get({"line_id": user_id})
        user_state.update(
            action=action,
            data=data,
            history_messages=history_messages
        )

        return None
