"""X-Input Watch Testing"""

from inputs import get_gamepad

types = ['Sync']
while True:
    events = get_gamepad()
    for event in events:
        if event.ev_type not in types:
            if event.state > 2:
                if event.state % 5 == 0:
                    print(event.ev_type, event.code, event.state)
            else:
                print(event.ev_type, event.code, event.state)
