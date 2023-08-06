from __future__ import annotations

import logging
import typing

from abc import ABC
from abc import abstractmethod

from starlette.websockets import WebSocket

class WebSocketMessageEndpoint(ABC):
    """
    An abstract base class for a class which accepts routed websocket messages.

    All routes used by WebSocketRouterEndpoint must be based on this class.
    """
    def __init__(self, route: str, websocket: WebSocket):
        self._route = route
        self._websocket = websocket

    @property
    def route(self):
        """The WebSocket route for this endpoint"""
        return self._route

    @property
    def websocket(self):
        """The WebSocket this endpoint instance is attached to"""
        return self._websocket

    @property
    def app(self):
        """The Starlette app object"""
        return self._websocket.app

    @abstractmethod
    async def on_receive(self, route: str, data: typing.Any) -> None:
        """Override to handle an incoming websocket message"""

    async def on_disconnect(self, close_code: int) -> None:
        """Override to handle a disconnecting websocket"""

