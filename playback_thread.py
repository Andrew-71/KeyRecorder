from PyQt5.QtCore import QRunnable

import keyboard
import mouse
import time


class PlaybackThread(QRunnable):
    def __init__(self, parent, events, typing_delay):
        super().__init__()
        self.events = [i['event'] for i in events]
        self.typing_delay = typing_delay
        self.parent = parent

    def run(self):
        self.parent.toggle_buttons(enabled=False, include_stop=True)
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
        self.parent.toggle_buttons(enabled=True, include_stop=True)


