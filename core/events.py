_subscribers = {}

def subscribe(event, fn):
    print(f"[EVENTS] subscribe → {event}")
    _subscribers.setdefault(event, []).append(fn)

def emit(event, data=None):
    print(f"[EVENTS] emit → {event}: {data}")
    for fn in _subscribers.get(event, []):
        fn(data)
