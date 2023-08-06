import logging

from uuid import uuid4

from abc import ABC

from copy import deepcopy

from dataclasses import dataclass

from typing import Any, Dict, Optional, Callable, List, Union

from dnastack.common.logger import get_logger


@dataclass(frozen=True)
class Event:
    details: Dict[str, Any]

    @classmethod
    def make(cls, details: Optional[Dict[str, Any]] = None):
        return Event(details=deepcopy(details) if details else dict())


class EventHandler:
    def __call__(self, event: Event) -> None:
        raise NotImplementedError()


class EventTypeNotRegistered(RuntimeError):
    """ Raised when the given event type is not registered """


class AbstractEventSource:
    def get_id(self) -> str:
        raise NotImplementedError()

    def get_fixed_types(self) -> List[str]:
        raise NotImplementedError()

    def dispatch(self, event_type: str, event: Union[Event, Dict[str, Any]]):
        raise NotImplementedError()

    def on(self, event_type: str, handler: Union[EventHandler, Callable[[Event], None]]):
        raise NotImplementedError()

    def off(self, event_type: str, handler: Union[EventHandler, Callable[[Event], None]]):
        raise NotImplementedError()

    def clear(self, event_type: Optional[str] = None):
        raise NotImplementedError()


class EventSource(AbstractEventSource):
    """
    Event Source

    This is not thread-safe.
    """
    def __init__(self, fixed_types: Optional[List[str]] = None, origin: Optional[Any] = None):
        self._origin = origin
        self._id = str(uuid4())
        self._event_logger = get_logger(f'{type(self).__name__}/{self._id}', logging.WARNING)
        self._event_handlers: Dict[str, List[Union[EventHandler, Callable[[Event], None]]]] = dict()
        self._fixed_types = fixed_types or list()

        self._event_logger.debug(f'REF: {self}')

        if self._origin:
            self._event_logger.debug(f'ORIGIN: {self._origin}')

    def get_id(self) -> str:
        return self._id

    def get_fixed_types(self) -> List[str]:
        return self._fixed_types

    def dispatch(self, event_type: str, event: Union[Event, Dict[str, Any]]):
        self._raise_error_for_non_registered_event_type(event_type)

        self._event_logger.debug(f'E/{event_type}: DISPATCH {event}')

        if event_type in self._event_handlers:
            for handler in self._event_handlers[event_type]:
                self._event_logger.debug(f'E/{event_type}: INVOKE {handler}')
                handler(event if isinstance(event, Event) else Event.make(details=event))
        else:
            pass

    def on(self, event_type: str, handler: Union[EventHandler, Callable[[Event], None]]):
        self._raise_error_for_non_registered_event_type(event_type)

        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = list()

        self._event_handlers[event_type].append(handler)
        self._event_logger.debug(f'E/{event_type}: USE {handler}')

        return self

    def off(self, event_type: str, handler: Union[EventHandler, Callable[[Event], None]]):
        self._raise_error_for_non_registered_event_type(event_type)

        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = list()

        new_handlers = [
            existing_handler
            for existing_handler in self._event_handlers[event_type]
            if hash(handler) != hash(existing_handler)
        ]

        self._event_handlers[event_type] = new_handlers
        self._event_logger.debug(f'E/{event_type}: NOT USE {handler}')

        return self

    def clear(self, event_type: Optional[str] = None):
        if event_type:
            if event_type in self._event_handlers:
                self._event_handlers[event_type].clear()
            else:
                pass
        else:
            self._event_handlers.clear()

    def _raise_error_for_non_registered_event_type(self, event_type: str):
        if self._fixed_types and event_type not in self._fixed_types:
            raise EventTypeNotRegistered(f'Given {event_type}, but expected {", ".join(self._fixed_types)}')

    def set_passthrough(self, origin: AbstractEventSource):
        self._event_logger.debug(f'SET PASSTHROUGH {origin} => {self}')

        for event_type in origin.get_fixed_types():
            origin.on(event_type, EventRelay(self, event_type))


class EventRelay(EventHandler):
    def __init__(self, relay_source: AbstractEventSource, event_type: str):
        self.__relay_source = relay_source
        self.__event_type = event_type
        self.__logger = get_logger(f'{type(self).__name__}/{self.__relay_source.get_id()}/{self.__event_type}',
                                   logging.WARNING)

    def __call__(self, event: Event) -> None:
        self.__logger.debug('Relaying...')
        self.__relay_source.dispatch(self.__event_type, event)
        self.__logger.debug('Relayed')
