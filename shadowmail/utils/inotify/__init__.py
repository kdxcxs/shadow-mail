"""For watching maildir changes"""

import inotify.adapters
from threading import Thread

__all__ = [
    'watch',
]

class InotifyThread(Thread):
    daemon = True
    def __init__(self, watch_path, handler):
        Thread.__init__(self)
        self.watch_path = watch_path
        self.handler = handler

    def run(self):
        for event in inotify.adapters.InotifyTree(self.watch_path).event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            self.handler(type_names, path, filename)

def watch(path, handler):
    t = InotifyThread(path, handler)
    t.start()
    return t
