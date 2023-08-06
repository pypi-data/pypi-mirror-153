from __future__ import annotations

import inspect
import logging
import orjson
import typing

from copy import copy

from boltons.dictutils import MultiDict

from .message import WebSocketMessageEndpoint

class command:
    """
    Decorator for use with the WebSocketCommandEndpont class.

    Use of the decorator designates the method as a command callback method

    Example Usage:

        >>> class Foo(WebSocketCommandEndpont):
        >>>     @command("test")
        >>>     def on_test(self, arg1, optarg = None):
        >>>         pass

    Multiple commands can target the same method:

        >>> class Foo(WebSocketCommandEndpont):
        >>>     @command("test_1")
        >>>     @command("test_2")
        >>>     def on_test(self, arg1, optarg = None):
        >>>         pass
    """
    varname = '_cmds'

    def __init__(self, cmd):
        self.cmd = cmd

    def __call__(self, func):
        # Use a list to store registered command names
        # ... This permits multiple commands to target a single method
        if not hasattr(func, self.varname):
            setattr(func, self.varname, [])
        cmds = getattr(func, self.varname)
        cmds.append(self.cmd)
        return func


class WebSocketCommandEndpont(WebSocketMessageEndpoint):
    """
    An endpoint for websocket messages routed to multiple locations.

    This class assumes JSON mesages of the following format are received:

    >>> msg = {'route': 'my_route', 'cmd': 'my_cmd', 'data': {...}}

    my_route is a route identifier unique to this class and is configured with the application.
    my_cmd is linked to a callback method using the `command` decorator
    data will be converted to the callback command function keywords (using: `**data`)

    The client side code must send the `setRoute` command before any other action.
    This will configure the return route for messages sent by this class.

    To send commands back to the server, use the `send_cmd` method.

    """
    def __init__(self, *arg, **kw):
        super().__init__(*arg, **kw)
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__qualname__}")
        self._routeResponse = None

        # Get a list of command callbacks registered via decorator
        callbacks = inspect.getmembers(
            self,
            lambda func: inspect.ismethod(func) and hasattr(func, command.varname)
        )

        # Save the list of command callback methods in a format easy to use later
        # ... A MultiDict (OrderedMultiDict) is used to permit multiple callbacks to the same method
        # ... Callbacks will be called in the order they are registered!
        self._commands = MultiDict([
            (cmd, func)
            for fname,func in callbacks
            for cmd in getattr(func, command.varname)
        ])

    @property
    def commands(self):
        """The dict of registered command callbacks"""
        return self._commands

    @property
    def routeResponse(self):
        """The response route identifier for outgoing commands"""
        return self._routeResponse

    async def on_receive(self, route: str, cmd: str, data: typing.Any) -> None:
        """Override to handle an incoming websocket message"""
        if cmd not in self._commands:
            self._logger.warning(f"Unknown Command: {cmd}")
        elif type(data) != dict:
            self._logger.error(f"Route [{route}] Command [{cmd}] data is not a dict type: {data}")
        else:
            self._logger.debug(f"Route [{route}] Command [{cmd}] received: {data}")
            for func in self._commands.getlist(cmd):
                try:
                    await func(**data)
                except TypeError as ex:
                    self._logger.exception(ex)

    async def send_cmd(self, cmd: str, route: str = None, **data) -> None:
        """
        Send a command back to the server.

        In ordinary usage, the `route` parameter should not be used.
        Its value will be set automatically by the `setRoute` command from the client.

        A command will be structured the same as commands received from the client.

        >>> msg = {'route': 'my_route', 'cmd': 'my_cmd', 'data': {...}}

        :param cmd: The command name to send
        :param route: The routing for this command (optional)
        :param data: Any additional keywords will be sent along in the `data` portion of the command
        """
        await self.websocket.send_bytes(orjson.dumps({
            'route': route or self._routeResponse,
            'cmd':   cmd,
            'data':  data
        }).decode("utf-8"))

    @command("connect")
    async def on_setRoute(self, route: str):
        """
        Set the route string for messages retuirning to the JavaScript front end
        """
        self._routeResponse = route


