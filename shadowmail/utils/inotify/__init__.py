"""For watching maildir changes"""

import inotify.adapters
from threading import Thread

__all__ = [
    'watch',
]

def watch(path, handler):
    def _watch(_path):
        for event in inotify.adapters.InotifyTree(_path).event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            handler(type_names, path, filename)
    Thread(target=_watch, args=(path,)).start()
