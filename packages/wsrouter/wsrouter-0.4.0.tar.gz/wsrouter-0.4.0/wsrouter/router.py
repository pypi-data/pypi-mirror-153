from __future__ import annotations

import logging
import orjson
import typing

from pathlib import Path
from starlette.websockets import WebSocket
from starlette.endpoints import WebSocketEndpoint

class WebSocketRouterEndpoint(WebSocketEndpoint):
    """
    This is a Starlette WebSocket Endpoint which acts as a router for WebSocket
    messages by resuing a single WebSocket for all routes.
    """

    def __init__(self, *arg, routes: dict[str,WebSocketMessageEndpoint] = None, **kw):
        super().__init__(*arg, **kw)

        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__qualname__}")
        self._websocket = None

        self._routes = routes or {}

    @property
    def routes(self) -> list[WebSocketMessageEndpoint]:
        """
        The list of Starlette WebSocket routes
        """
        return self._routes

    @property
    def websocket(self) -> WebSocket|None:
        """The websocket associated with this class instance"""
        return self._websocket

    def add_route(self, route: str, endpoint: WebSocketMessageEndpoint):
        """
        Add a Starlette route to the Router object.

        Equivalent to:

            >>> self.routes[route] = endpoint
        """
        self._routes[route] = endpoint

    async def on_connect(self, websocket):
        await websocket.accept()
        self._logger.debug(f"WebSocket Opened: {websocket.url.path}")
        self._websocket = websocket

        # Initialize the active routes table for this connection
        websocket.state.routes = {}

    async def on_disconnect(self, websocket, close_code):
        # NOTE: The on_disconnect event does not occur with Starlette TestClient
        for route in websocket.state.routes:
            await websocket.state.routes[route].on_disconnect(close_code)
        websocket.state.routes.clear()

    async def on_receive(self, websocket, data):
        try:
            msg = orjson.loads(data)

            if type(msg) != dict:
                self._logger.error(F"Unknown Message Format: {msg}")
            elif not 'route' in msg:
                self._logger.error(F"Message received with no route: {msg}")
            elif not msg['route'] in self._routes:
                self._logger.warning(F"WebSocket message route has no endpoint: {msg['route']}")
            else:
                wsroutes = websocket.state.routes

                endpoint = wsroutes.setdefault(
                    msg['route'],
                    self._routes[msg['route']](msg['route'], websocket)
                )

                await endpoint.on_receive(**msg)

        except Exception as ex: # pragma: no cover
            self._logger.exception(f"Exception in Websocket Receive [{ex}]: [{data}]")

class WebSocketRouter:
    """
    This is a factory class whose entire purpose is to create a WebSocketRouterEndpoint object.

    WebSocketRouterEndpoint uses a single websocket to route messages
    between multiple endpoints on both client (JavaScript) and server (Python)
    sides of the websocket connection.

    This separation into two classes is necessary because Starlete Endpoint
    objects are created only on connect, but routes should be configured before
    the application is running.

    Example usage:

        >>> from starlette.routing import WebSocketRoute
        >>> from starlette.applications import Starlette

        >>> class MyWebSocketEndpoint(WebSocketCommandEndpont):
        >>>     ...

        >>> # Create the WebSocket routes
        >>> wsroutes = {
                "/comp1": MyWebSocketEndpoint),
            }

        >>> # Create the application routes
        >>> routes   = [WebSocketRoute("/ws", endpoint=WebSocketRouter(routes=wsroutes))]

        >>> # Create the Starlette application
        >>> app      = Starlette(routes=routes, ...)
    """

    # NOTE: A few alternate implementations were considered.
    # ... In the end, this solution was chosen as aligning best with:
    #     ... Starlette paradigms
    #     ... Ease of understanding looking at the code (years later)
    #     ... It follows general good coding practices
    #
    # Below are notes on why alternate solutions were discarded.
    #
    # Class level default routes directly in WebSocketRouterEndpoint
    # ... Discarded as a Bad Idea™
    # ... Becuase it is a hacky type solution
    #
    # Automatic registration of endpoints by the final destination
    # ... Discarded as a Very Bad Idea™
    # ... Because there is no control in the app over what endpoints appear
    # ... Because it could too easily lead to repated routes
    # ... Because it would limit code reuse
    #
    # Registration of endpoints by command from the GUI
    # ... Discarded as a Horrible Idea™
    # ... Because it violates separation of GUI and Backend code desired in this module
    # ... Because it creates potential maintenance nightmares checking JavaScript code for Python code name changes
    #
    # Ruse the Starlette Route framework
    # ... Discarded as having too much irrelevant code that would confuse functionality

    # The default endpoint class created by this class
    # ... This can be easily overridden via a subclass to change the default behavior.
    DEFAULT_ENDPOINT = WebSocketRouterEndpoint

    # The JavaScript static files path for use in Starlette Mount commands
    JS_PATH = Path(__file__).parent/'static'


    def __init__(self, routes: list[WebSocketRoute], epClass: typing.Any = None):
        self._routes = routes
        self._epClass = epClass or self.DEFAULT_ENDPOINT

    @property
    def routes(self) -> list[WebSocketRoute]:
        """
        The list of WebSocket routes
        """
        return self._routes

    @property
    def endpoint_class(self):
        """
        The actual endpoint class which will be created
        """
        return self._epClass

    def __call__(self, *arg, **kw):
        """
        Return an instance of WebSocketRouterEndpoint with the configured routes
        """
        return self._epClass(*arg, routes=self.routes, **kw)

