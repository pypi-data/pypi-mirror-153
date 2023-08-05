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

from enum import IntEnum


class SimpleMessageType(IntEnum):
    START_PIPELINE = 50
    LIST_GRABBER_PLUGINS = 52
    STOP_PIPELINE = 53
    DISCOVER_DEVICES = 54
    LIST_PIPELINE_COMPONENTS = 55
    GET_OUTPUT_CATALOG = 56
    GET_RUNNING_STATE = 57
    PING = 58
    START_RECORDING = 63
    STOP_RECORDING = 64
    PAUSE_RECORDING = 65
    GET_RECORDING_NAME = 69
    AUTO_CALIBRATE = 70
    GET_PIPELINE = 76
    GET_CONNECTION_STATISTICS = 77
    GET_LICENSE_STATE = 82
    GENERATE_KEYPAIR = 86
    GET_SYSTEM_GUID = 89
    GET_SERVICES = 90


class MessageType(IntEnum):
    # SET_PIPELINE = 51
    # LIST_COMPONENT_INSTANCES = 59
    # LIST_GRABBER_INSTANCES = 60
    # GET_COMPONENT_PROPERTY_VALUES = 61
    # SET_COMPONENT_PROPERTY_VALUE = 62
    # LIST_DIRECTORY_CONTENTS = 66
    # CREATE_DIRECTORY = 67
    # SET_RECORDING_NAME = 68
    # DELETE_PATH = 71
    # RENAME_PATH = 72
    # GET_GRABBER_PROPERTY_VALUES = 73
    # SET_GRABBER_PROPERTY_VALUE = 74
    # GET_PROPERTY_VALUE_SUGGESTIONS = 75
    # TOGGLE_DAY_NIGHT = 78
    # DISCOVER_SYSTEMS = 79
    # SET_LICENSE = 80
    # LOAD_COMPONENTS = 81
    # GET_DATA_CONTENT = 83
    # SET_DATA_CONTENT = 84
    # GET_SYSTEM_CATALOG = 85
    # PERSIST_PIPELINE = 87
    REMOTE_PROCEDURE_CALL = 88


class Event(IntEnum):
    NEW_PIPELINE_STATE = 50


class PipelineState(IntEnum):
    NO_PIPELINE = 0
    INITIALIZED = 2
    RUNNING = 1
    STOPPED = 3


class RecordingState(IntEnum):
    NO_PIPELINE = 0
    RUNNING = 1
    PAUSED = 2
    STOPPED = 3
