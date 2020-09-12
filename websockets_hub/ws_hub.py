from threading import Thread
from queue import Queue, Empty
from global_settings import STOPPED_ALL
from websockets_hub import settings
import sys

__qu_clients_to_hub = Queue()
__num_ws = 0


def create_new_ws():
    global __num_ws
    if __num_ws + 1 > 99:
        return False
    __num_ws += 1
    ws_id = "wsId-{:02}".format(__num_ws)
    qu_ws_to_client = Queue()
    Wss(ws_id, qu_ws_to_client)
    return {"ws_id": ws_id, "qu_get": qu_ws_to_client, "qu_put": __qu_clients_to_hub}


class Wss:
    ws_list = {}

    def __init__(self, ws_id, qu):
        self.ws_id = ws_id
        self.qu = qu
        self.cur_set = None
        self.status = 'waiting launch'
        self.method = None
        Wss.ws_list[self.ws_id] = self

    def start(self, set_name):
        self.method = 'start'
        try:
            self.cur_set = settings.get_set(set_name)
        except (NameError, ValueError, AttributeError) as e:
            pass


def loop(qu_get):
    while True:
        try:
            ws_id, method, request, request_num = qu_get.get(block = False)
        except Empty:
            pass
        else:
            qu_get.task_done()
            if method == "start":
                Wss.ws_list[ws_id].start(request)


__th_ws_hub = Thread(target=loop, name = "ws_hub", daemon = True,
                     kwargs = {"qu_get": __qu_clients_to_hub})
__th_ws_hub.start()

# r = dict(vars())
# # print(vars())
# for s in r.items():
#     print(s )
# for name in dir(sys.modules[__name__]):
#     print(name, getattr(sys.modules[__name__], name))
# print(dir(sys.modules[__name__]))
print(hasattr(settings, 'SET_1'))













