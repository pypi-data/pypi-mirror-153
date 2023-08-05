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

from functools import partialmethod

from .connection import Connection
from .types import MessageType, SimpleMessageType


class Client:
    def __init__(self, connection):
        if not isinstance(connection, Connection):
            raise TypeError("connection must be an instance of Connection")
        self._conn = connection

    def connect(self):
        self._conn.connect()

    def disconnect(self):
        self._conn.disconnect()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def _simple_ctrl(self, message_type, timeout=None):
        if not isinstance(message_type, SimpleMessageType):
            raise ValueError("message_type must be in SimpleMessageType")
        return self._conn.send_ctrl({"Request": {"Type": message_type.value}}, timeout)

    def rpc_get_cababilties(self, recipient=None, timeout=None):
        return self.rpc_request(recipient, [{"method": "get_capabilities"}], timeout)

    def rpc_set(self, recipient, args=None, timeout=None):
        return self.rpc_request(
            recipient, [{"method": "set", "args": args or []}], timeout
        )

    def rpc_get(self, recipient, args=None, timeout=None):
        return self.rpc_request(
            recipient, [{"method": "get", "args": args or []}], timeout
        )

    def rpc_request(self, recipient=None, requests=None, timeout=None):
        request = {"requests": requests or []}
        if recipient is not None:
            request["recipient"] = recipient

        return self._conn.send_rpc(
            {
                "Request": {
                    "Type": MessageType.REMOTE_PROCEDURE_CALL,
                    "horus.pb.controlmessages.v1.RPCRequestMessage.RPCRequest": request,
                }
            },
            timeout,
        )


# Generate client methods for control messages that have no arguments.
for message_type in SimpleMessageType:
    method_name = message_type.name.lower()
    if hasattr(Client, method_name):
        raise AttributeError(f"Client already has method {method_name}")
    setattr(
        Client,
        method_name,
        partialmethod(Client._simple_ctrl, message_type=message_type),
    )
