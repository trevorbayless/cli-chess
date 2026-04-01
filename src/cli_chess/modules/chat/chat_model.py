class ChatModel:
    def __init__(self):
        self._messages: list[dict] = []
        self._event_listeners = []

    def add_message(self, username: str, text: str):
        msg = {"username": username, "text": text}
        self._messages.append(msg)
        self._notify_listeners()

    def get_messages(self) -> list[dict]:
        return self._messages.copy()

    def add_event_listener(self, callback):
        self._event_listeners.append(callback)

    def _notify_listeners(self):
        for cb in self._event_listeners:
            cb()