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

import inspect
from random import randint


class UnexpectedResponseError(Exception):
    pass


class MissingFutureError(Exception):
    pass


class UnexpectedMessageError(Exception):
    pass


class Connection:
    def __init__(
        self,
        address,
        on_event_func=None,
    ):
        self._address = address
        self._on_event_func = on_event_func

        # Callback can accept 1 or 2 arguments. First argument is the
        # event data and the second argument is the request data.
        if on_event_func:
            pc = _get_param_count(on_event_func)
            if pc == 1:
                self._on_event_func = self._wrap_on_event_func(on_event_func)
            elif pc == 2:
                self._on_event_func = on_event_func
            else:
                raise TypeError("on_event_func must have 1..=2 parameters")

    def _wrap_on_event_func(self, f):
        def wrapper(event, request):
            return f(event)
        return wrapper

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def send_ctrl(self, msg, timout=None):
        raise NotImplementedError

    def send_rpc(self, msg, timout=None):
        raise NotImplementedError

    def next_id(self):
        return randint(0x1, 0xFFFF)


def _get_param_count(f):
    return len(inspect.signature(f).parameters)
