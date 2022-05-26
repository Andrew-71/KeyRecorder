from PyQt5.QtCore import QRunnable

import keyboard
import mouse
import time


class PlaybackThread(QRunnable):
    def __init__(self, events, typing_delay):
        super().__init__()
        self.events = events
        self.typing_delay = typing_delay

    def run(self):
        mouse_events = []
        for i in self.events:
            if i.__class__ != keyboard.KeyboardEvent:
                mouse_events.append(i)
            else:
                mouse.play(mouse_events)
                mouse_events = []
                keyboard.play([i])
                time.sleep(self.typing_delay)
        mouse.play(mouse_events)