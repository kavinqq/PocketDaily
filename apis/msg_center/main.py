from apis.random_int import main as random_int_main


class EventCenter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventCenter, cls).__new__(cls)
        return cls._instance

    def handle_event(self, event):
        message = event.message.text

        if "亂數" in message:
            return random_int_main(event)
