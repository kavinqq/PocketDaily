from typing import Union


class UserStates:
    _instance = None
    _states = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserStates, cls).__new__(cls)
            cls._states = {}
        return cls._instance

    def get_state(
        self,
        user_id
    ) -> Union[dict, None]:
        return self._states.get(user_id, None)

    def set_state(
        self,
        user_id,
        action=None,        
        data=None,
        history_messages=None
    ) -> None:
        self._states[user_id] = {
            "action": action,            
            "data": data,
            "history_messages": history_messages
        }

        return None

    def delete_state(
        self,
        user_id
    ):
        return self._states.pop(user_id, None)

    def edit_state(
        self,
        user_id,
        action,
        data=None,
        history_messages=None
    ) -> None:
        self.set_state(
            user_id,
            action,
            data,
            history_messages
        )

        return None

    def init_state(
        self,
        user_id
    ):
        self.set_state(user_id)

        return None
