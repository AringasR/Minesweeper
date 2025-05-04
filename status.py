import random

class GameStatus:
    def __init__(self, frames, messages):
        self.frames = frames
        self.messages = messages
        self.current_key = "neutral"
        self.frame_index = 0
        self.text = random.choice(messages["neutral"])

    def set(self, key):
        self.current_key = key
        self.frame_index = 0
        self.text = random.choice(self.messages.get(key, [""]))

    def update_frame(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames[self.current_key])

    def get_frame(self):
        return self.frames[self.current_key][self.frame_index]

    def get_text(self):
        return self.text