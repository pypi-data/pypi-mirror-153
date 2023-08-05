"""PyTandem Module

This module handles the attachment, collection, and triggering of
functions in a multithreaded fasion.
"""


import threading
import time


class EventManager:
    """housing class for events and threads"""

    events = []
    threads = []


def attach(event_name):
    """decorator function that attaches functions to the housing class's
    events list property"""

    def decorator(f):
        def wrapper(*args, **kwargs):
            EventManager.events.append({
                'event_name': event_name,
                'callback': f,
                'args': args,
                'kwargs': kwargs
            })
        return wrapper
    return decorator


def trigger(event_name, threaded=True, max_threads=None):
    """trigger function to fire functions in the housing class's events
    list. these are fired in tandem `max_threads` at a time"""

    for event in EventManager.events:
        if event['event_name'] == event_name:
            try:
                if threaded:
                    t = threading.Thread(target=event['callback'], args=(event['args']), kwargs=(event['kwargs']))
                    EventManager.threads.append(t)
                else:
                    event['callback'](*event['args'], **event['kwargs'])
            except Exception as err:
                print(err.args)

    for thread in EventManager.threads:
        _start_thread(thread, max_threads)

    EventManager.threads = []


def _start_thread(thread, max_threads=None):
    """starts a given thread using thread.start()"""

    active_threads = threading.active_count()
    max_threads = max_threads if max_threads else 4

    if active_threads >= max_threads:
        time.sleep(1)
        _start_thread(thread, max_threads)

    else:
        thread.start()