import keyboard
import mouse
from win32api import GetSystemMetrics


# full == all resolutions are same as monitor's
# partial == resolutions can be auto-edited
# none == manual resizing required
def check_compatibility(events):
    w, h = GetSystemMetrics(0), GetSystemMetrics(1)

    full = True
    partial = True
    for i in events:
        res = i['resolution']
        if res['w'] != w or res['h'] != h:
            full = False
            if round(w / h, 2) != round(res['w'] / res['h'], 2):
                partial = False
    if not full:
        return 'partial' if partial else 'none'
    return 'full'


# Auto resize all events in the list to be same resolution as monitor's
def resize(events, target_res=(GetSystemMetrics(0), GetSystemMetrics(1))):
    new_events = []

    w, h = target_res
    for i in events:
        if i['event'].__class__ != keyboard.KeyboardEvent:
            res = i['resolution']

            # TODO: Is this the correct way to divide, or we need the opposite?
            ratio_w = w / res['w']
            ratio_h = h / res['h']

            new_events.append({'event': mouse.MoveEvent(x=int(i['event'].x * ratio_w), y=int(i['event'].y * ratio_h), time=i['event'].time),
                               'resolution': {'w': w, 'h': h},
                               'window': i['window']})

        else:
            new_events.append(i)

    return new_events
