# Copyright (C) 2022 Horus View and Explore B.V.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
from concurrent.futures import (
    Future,
    TimeoutError as FutureTimeoutError,
)

import socketio

from .connection import (
    Connection,
    MissingFutureError,
    UnexpectedMessageError,
    UnexpectedResponseError,
)
from .utils import AttrDict


class SocketIOConnection(Connection):
    DEFAULT_TIMEOUT = 10

    ConnectionError = socketio.exceptions.ConnectionError

    def __init__(
        self,
        address,
        on_event_func=None,
    ):
        super().__init__(address, on_event_func)

        self._sio = socketio.Client()
        self._queue = {}  # Request id -> future mapping.
        self._is_connected = False

        self._on_connect_future: Future = Future()
        self._on_disconnect_future: Future = Future()

        self._sio.on("connect")(self._on_connect)
        self._sio.on("disconnect")(self._on_disconnect)
        self._sio.on("ctrl")(self._on_ctrl)

    def _on_connect(self):
        self._on_connect_future.set_result(True)
        self._is_connected = True

    def _on_disconnect(self):
        self._is_connected = False
        self._on_disconnect_future.set_result(True)

    def _on_ctrl(self, data):
        # NOTE: Sometimes data is not decoded and needs to be done manually.
        if isinstance(data, str):
            data = json.loads(data)
        if not isinstance(data, dict):
            raise TypeError(f"expected dict, but got {type(data)}")

        if "Events" in data:
            self._on_ctrl_event(data)
        elif "Response" in data:
            self._on_ctrl_response(data)
        else:
            raise UnexpectedMessageError(f"unexpected message: {data!r}")

    def _on_ctrl_response(self, data):
        req_id = data["Response"]["ResponseTo"]

        try:
            future = self._queue.pop(req_id)
        except KeyError:
            # TODO: Check if this works with the current way the
            # system works. Is a ping response send to everybody?
            raise UnexpectedResponseError
        if not future:
            raise MissingFutureError  # bug

        data = _unwrap_response(data)

        future.set_result(data)

    def _on_ctrl_event(self, data):
        if self._on_event_func:
            for event in data["Events"]:
                self._on_event_func(AttrDict(event), AttrDict(data.get("Request", {})))

    def _wait(self, future, timeout, err_msg):
        try:
            return future.result(timeout=timeout)
        except FutureTimeoutError:
            raise TimeoutError(err_msg) from None

    def connect(self):
        if self._is_connected:
            raise ConnectionError("already connected")
        self._sio.connect(self._address)
        self._wait(
            self._on_connect_future, self.DEFAULT_TIMEOUT, "timeout during connect"
        )
        self._on_connect_future = Future()

    def disconnect(self):
        if not self._is_connected:
            raise ConnectionError("is not connected")
        self._sio.disconnect()
        self._wait(
            self._on_disconnect_future,
            self.DEFAULT_TIMEOUT,
            "timeout during disconnect",
        )
        self._on_disconnect_future = Future()

    def send_ctrl(self, msg, timeout=None):
        if not self._is_connected:
            raise ConnectionError("is not connected")
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        req_id = self.next_id()

        try:
            msg["Request"]["Id"] = req_id
        except KeyError:
            raise ValueError(f"invalid request message: {msg!r}")

        future: Future = Future()
        self._queue[req_id] = future
        self._sio.emit("send-ctrl", json.dumps(msg))

        try:
            result = self._wait(future, timeout, "timeout while waiting on response")
        except TimeoutError:
            self._queue.pop(req_id)
            raise

        return result

    def send_rpc(self, msg, timeout=None):
        result = self.send_ctrl(msg, timeout)
        result = result.RPCResponse.response
        return result


def _unwrap_response(data):
    new_data = AttrDict({})

    for k, v in data["Response"].items():
        if not k.startswith("horus.pb.controlmessages.v1"):
            continue
        try:
            idx = k.rindex(".") + 1
        except ValueError:
            idx = 0
        name = k[idx:]
        new_data[name] = AttrDict(v)

    return new_data
