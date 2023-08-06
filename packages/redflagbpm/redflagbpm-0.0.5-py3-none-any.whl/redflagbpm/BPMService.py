import sys
import time
import os
import atexit
import threading
from typing import Any

from vertx import EventBus
from queue import Queue


class BPMService:
    eb_calls: EventBus
    eb_handlers: EventBus
    delay = 10
    call_timeout = 30.0
    handlers = []
    address_dict : dict

    def __init__(self, host="localhost", port=7000, options=None, err_handler=None, ssl_context=None):
        if options is None:
            options = {}
        self.eb_calls = EventBus(host=host, port=port, options=options, err_handler=err_handler,
                                 ssl_context=ssl_context)
        self.eb_handlers = EventBus(host=host, port=port, options=options, err_handler=err_handler,
                                    ssl_context=ssl_context)
        self.setupServices()
        self.connect()
        self.address_dict = {}
        atexit.register(self.close)

    def setupServices(self):
        pass

    def setAddress(self, address: Any = None):
        if isinstance(address, dict):
            addr = address['replyAddress']
        elif isinstance(address, str):
            addr = address
        elif 'BPM_EVENT_BUS_REPLY' in os.environ:
            addr = os.environ['BPM_EVENT_BUS_REPLY']
        else:
            raise ValueError('No address supplied')
        tid = threading.get_ident()
        self.address_dict[tid]=addr

    def getAddress(self, address: Any = None) -> str:
        if isinstance(address, dict):
            return address['replyAddress']
        elif isinstance(address, str):
            return address
        elif threading.get_ident() in self.address_dict:
            return self.address_dict[threading.get_ident()]
        elif 'BPM_EVENT_BUS_REPLY' in os.environ:
            return os.environ['BPM_EVENT_BUS_REPLY']
        else:
            raise ValueError('No address supplied')

    def send(self, address, headers=None, body=None):
        ret = Queue()
        self.eb_calls.send(address=address, headers=headers, body=body, reply_handler=lambda msg: ret.put(msg))
        return ret.get(True, self.call_timeout)

    def reply(self, body=None, address=None, headers=None):
        addr = self.getAddress(address)
        if not isinstance(body, dict):
            body = {"reply": body}
        self.eb_calls.send(address=addr, headers=headers, body=body)

    def call(self, address, body=None, headers=None):
        ret = self.send(address, headers, body)
        if 'body' in ret:
            if 'reply' in ret['body']:
                return ret['body']['reply']
        return None

    def connect(self):
        if not self.eb_calls.is_connected():
            self.eb_calls.connect()
        if not self.eb_handlers.is_connected():
            self.eb_handlers.connect()

    def close(self):
        for address in self.handlers:
            self.unregister_handler(address)
        if self.eb_calls.is_connected():
            self.eb_calls.close()
        if self.eb_handlers.is_connected():
            self.eb_handlers.close()

    def runtime_setVariable(self, processId: str, variables: dict):
        ret = self.call("bpmHelper.runtime_setVariable", body={
            "processId": processId,
            "variables": variables})
        return ret

    def register_handler(self, address, handler):
        self.eb_handlers.register_handler(address, handler)
        self.handlers.append(address)

    def unregister_handler(self, address, handler=None):
        self.eb_handlers.unregister_handler(address, handler)
        self.handlers.remove(address)

    def run(self, address, handler):
        self.register_handler(address, handler)
        self.start()

    def exec(self, script: str, lang: str = 'javascript', context: dict = None, address: object = None) -> object:
        addr = self.getAddress(address)
        ret = Queue()
        self.eb_calls.send(address=addr, body={
            "lang": lang,
            "script": script,
            "context": context
        }, reply_handler=lambda x: ret.put(x))
        result = ret.get(True, self.call_timeout)
        if result['body']['succeeded']:
            return result['body']['body']
        else:
            raise ValueError(result['body']['trace'])

    def request(self, request: str, address=None):
        addr = self.getAddress(address)
        ret = Queue()
        self.eb_calls.send(address=addr, body={"request": request}, reply_handler=lambda x: ret.put(x))
        return ret.get(True, self.call_timeout)

    def start(self):
        # self.connect()
        try:
            while True:
                time.sleep(self.delay)
        except KeyboardInterrupt:
            self.stop()

    def isConnected(self):
        return self.eb_calls.is_connected()

    def stop(self):
        print("Stopping...")
        self.close()
        print("Stopped...")
        sys.exit(0)
