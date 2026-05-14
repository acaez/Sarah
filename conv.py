from config import HISTORY_MAX_TURNS


class Conversation:
    def __init__(self):
        self._history = []

    def add(self, role, content):
        self._history.append({"role": role, "content": content})

    def pop_last(self):
        if self._history:
            self._history.pop()

    def get(self):
        max_messages = HISTORY_MAX_TURNS * 2
        return self._history[-max_messages:]
