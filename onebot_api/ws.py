from typing import Union, Optional
import time
import json

from mcdreforged.api.types import ServerInterface, PluginEvent
from mcdreforged.api.decorator.new_thread import new_thread
import websocket

from onebot_api.constants import ERROR_CODES, ID, PATHS


class OneBotAPI:
    def __init__(self, server: ServerInterface, ws_url: str):
        self.server = server
        self.url = ws_url
        self.should_stop = False
        self.event_listener = EventListener(self)
        self.running = False
        self.ws = websocket.WebSocket()
        self.started = False
        self.will_stop = False

    def wait_till_all_finish(self) -> None:
        while self.running:
            continue

    def call_api(self, api: str, **params) -> Optional[dict]:
        if self.server.is_on_executor_thread():
            raise RuntimeError("Cannot invoke {} on the task executor thread".format(api))
        self.wait_till_all_finish()
        if self.will_stop:
            return
        self.ws.send(json.dumps({
            "action": api,
            "params": params,
        }))
        response = json.loads(self.ws.recv())
        if response['status'] == "failed":
            raise ERROR_CODES[response['retcode']]
        return response

    def __getattr__(self, item: str):
        return lambda **params: self.call_api(item, **params)
    
    @new_thread("OneBot API")
    def start(self) -> None:
        self.event_listener.start()
        self.ws.connect(self.url+PATHS.API)

    def stop(self) -> bool:
        if not self.started:
            return False
        self.event_listener.stop()
        self.ws.close()
        return True


class EventListener:
    def __init__(self, api: OneBotAPI):
        self.api = api
        self.server = api.server
        self.should_stop = False
        self.ws = websocket.WebSocket()

    def tick(self) -> None:
        try:
            content = self.ws.recv()
        except ConnectionRefusedError:
            self.server.logger.error("Cannot connect to {}".format(self.api.url))
            time.sleep(0.5)
            return
        content = _to_json(content)
        if not content:
            return
        self.server.dispatch_event(PluginEvent(".".join((ID, "qq", content['post_type']))), (content,))

    @new_thread("OneBot API Event Listener")
    def start(self) -> None:
        self.ws.connect(self.api.url+PATHS.EVENT)
        while not self.should_stop:
            try:
                self.tick()
            except Exception as e:
                self.server.logger.error("Error: {}, stopping OneBot API".format(e))
                self.api.stop()

    def stop(self) -> None:
        self.should_stop = True


def _to_json(content: Union[str, bytes]):
    if not isinstance(content, str):
        try:
            content = str.encode("UTF-8")
        except UnicodeError:
            return
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return
