from __future__ import annotations
import enum
import logging
from typing import Callable

LOGGER = logging.getLogger("EventManager")


class EventManager:
    def __init__(self):
        self._handlers = {}

    def register(self, event_type: str, callback: Callable):
        if not callable(callback):
            raise ValueError('callback parameter must be a callable')
        if event_type not in self._handlers:
            raise KeyError(f'Unknown event type {event_type}, supported types:'
                           f'{list(self._handlers.keys())}')
        self._handlers[event_type].append(callback)

    def unregister(self, event_type: str, callback: Callable):
        try:
            self._handlers[event_type].remove(callback)
        except (KeyError, ValueError):
            LOGGER.warning(f'event callback not found')
            pass

    def notify(self, event_type: str, *args, **kwargs):
        if event_type in self._handlers.keys():
            for callback in self._handlers[event_type]:
                callback(*args, **kwargs)

    def append_event_type(self, event_type: str):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
