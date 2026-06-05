_listeners: dict[str, list] = {}

def listener(event: str):
    def decorator(func):
        _listeners.setdefault(event, []).append(func)
        return func
    return decorator

def emit(event: str, **kwargs):
    for handler in _listeners.get(event, []):
        handler(**kwargs)