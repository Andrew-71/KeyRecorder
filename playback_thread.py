from PyQt5.QtCore import QRunnable

import keyboard
import mouse
import time

from win32gui import GetWindowText, GetForegroundWindow


# QRunnable to play current events
class PlaybackThread(QRunnable):
    def __init__(self, parent, events, typing_delay):
        super().__init__()

        self.events = list(filter(lambda x: x['enabled'], events))  # Only play enabled events
        self.typing_delay = typing_delay
        self.parent = parent

        self.last_pos = False  # Used to compare mouse position to see if the user wants to stop playback

    def run(self):
        self.parent.toggle_buttons(enabled=False, include_stop=True)
        mouse_events = []
        for i in self.events:

            if mouse.get_position() != self.last_pos and self.last_pos is not False and self.parent.config['move_stop']:
                self.parent.toggle_buttons(enabled=True, include_stop=True)
                return

            if i['event'].__class__ not in (keyboard.KeyboardEvent, mouse.ButtonEvent) and not \
                    (self.parent.config['move_stop'] and
                     len(mouse_events) > self.parent.config['move_stop_frequency']):
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
                    self.parent.toggle_buttons(enabled=True, include_stop=True)
                    return

            self.last_pos = mouse.get_position()

        mouse.play(mouse_events)
        self.parent.toggle_buttons(enabled=True, include_stop=True)


