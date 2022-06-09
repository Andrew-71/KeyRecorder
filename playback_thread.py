from PyQt5.QtCore import QRunnable

import keyboard
import mouse
import time

from PyQt5.QtWidgets import QMessageBox
from win32gui import GetWindowText, GetForegroundWindow


class PlaybackThread(QRunnable):
    def __init__(self, parent, events, typing_delay):
        super().__init__()
        self.events = events
        self.typing_delay = typing_delay
        self.parent = parent

    def run(self):
        self.parent.toggle_buttons(enabled=False, include_stop=True)
        mouse_events = []
        for i in self.events:
            if i['event'].__class__ not in (keyboard.KeyboardEvent, mouse.ButtonEvent):
                mouse_events.append(i['event'])
            else:
                mouse.play(mouse_events)
                mouse_events = []
                if i['event'].__class__ == keyboard.KeyboardEvent:
                    keyboard.play([i['event']])
                else:
                    mouse.play([i['event']])
                time.sleep(self.typing_delay)

                # TODO: Some apps love to change name of window dynamically. Which might break our app sometimes
                if i['window'] != GetWindowText(GetForegroundWindow()) and self.parent.config['stop_unexpected_playback']:

                    # TODO: figure out how to make error. Currently attempts failed.
                    print("Playback Aborted due to unexpected behaviour")
                    print(f'Window titles do not match:\nExcepted \'{i["window"]}\'\nRecieved \'{GetWindowText(GetForegroundWindow())}\'')
                    self.parent.toggle_buttons(enabled=True, include_stop=True)
                    return
        mouse.play(mouse_events)
        self.parent.toggle_buttons(enabled=True, include_stop=True)


