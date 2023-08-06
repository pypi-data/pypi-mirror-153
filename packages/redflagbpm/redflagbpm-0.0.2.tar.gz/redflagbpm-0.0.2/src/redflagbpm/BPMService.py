import sys
import time
import os
import atexit

from vertx import EventBus
from queue import Queue


class BPMService:
    eb_calls: EventBus
    eb_handlers: EventBus
    delay = 10
    call_timeout = 30.0
    handlers = []

    def __init__(self, host="localhost", port=7000, options=None, err_handler=None, ssl_context=None):
        if options is None:
            options = {}
        self.eb_calls = EventBus(host=host, port=port, options=options, err_handler=err_handler,
                                 ssl_context=ssl_context)
        self.eb_handlers = EventBus(host=host, port=port, options=options, err_handler=err_handler,
                                    ssl_context=ssl_context)
        self.setupServices()
        self.connect()
        atexit.register(self.close)

    def setupServices(self):
        pass

    def send(self, address, headers=None, body=None):
        ret = Queue()
        self.eb_calls.send(address=address, headers=headers, body=body, reply_handler=lambda msg: ret.put(msg))
        return ret.get(True, self.call_timeout)

    def reply(self, body=None, address=None, headers=None):
        if isinstance(address, dict):
            addr = address['replyAddress']
        elif isinstance(address, str):
            addr = address
        elif 'BPM_EVENT_BUS_REPLY' in os.environ:
            addr = os.environ['BPM_EVENT_BUS_REPLY']
        else:
            raise ValueError('No address supplied')
        if not isinstance(body,dict):
            body = {"reply": body}
        self.eb_calls.send(address=addr, headers=headers, body=body)

    def call(self, address, body=None, headers=None):
        ret=self.send(address, headers, body)
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

    def remote_exec(self, msg: dict, script: str, lang: str = 'javascript', context: dict = None):
        ret = Queue()
        self.eb_calls.send(address=msg['body']['address'], body={
            "lang": lang,
            "script": script,
            "context": context
        }, reply_handler=lambda x: ret.put(x))
        return ret.get(True, self.call_timeout)

    def start(self):
        # self.connect()
        try:
            while True:
                time.sleep(self.delay)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print("Stopping...")
        self.close()
        print("Stopped...")
        sys.exit(0)
