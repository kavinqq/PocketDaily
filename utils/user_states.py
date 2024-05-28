class UserStates:
    _instance = None
    _states = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserStates, cls).__new__(cls)
        return cls._instance

    def get_state(self, user_id):
        return self._states.get(user_id, None)

    def set_state(self, user_id, action, stage, data) -> None:
        self._states[user_id] = {
            "action": action,
            "stage": stage,
            "data": data
        }

        return None

    def delete_state(self, user_id):
        return self._states.pop(user_id, None)

    def edit_state(self, user_id, action, stage, data) -> None:
        self.delete_state(user_id)
        self.set_state(user_id, action, stage, data)

        return None
