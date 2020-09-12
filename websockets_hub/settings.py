import types
import json
import sys


def encoding_byte_utf8(data):
    return json.dumps(data, ensure_ascii=False).encode("utf8")


def json_check_strict_false(data):
    return json.loads(data, strict=False)


__SET_DEFAULT = {
    "request_processing_def": None,
    "answer_processing_def": None,
    "ping": None,
    "timeout_handshake": None,
    "timeout_wait_answer": None,
    "timeout_max_interval_connect": None,  # default=1
    "urls": "ws://echo.websocket.org/"
    }


SET_1 = {
    "request_processing_def": encoding_byte_utf8,  # or None
    "answer_processing_def": json_check_strict_false,  # or None
    "ping": {
             "time_interval": 45, "request": {'id': 9, 'method': 'call',
                                              'params': [0, 'get_objects', [["2.8.0"]]]}
             },  # or None
    "timeout_handshake": 3,  # or None, default
    "timeout_wait_answer": 10 * 2,  # or None
    "timeout_max_interval_connect": 60,  # or None, default=1
    "urls": [                       # or None, str
            "wss://b.mrx.im/ws",
            "wss://bitshares.openledger.info/ws",
            "wss://bitshares.dacplay.org:8089/ws",
            "wss://dele-puppy.com/ws",
            "wss://eu.openledger.info/ws",
            "wss://bit.btsabc.org/ws",
            "wss://eu.openledger.info/ws",
            "wss://dexnode.net/ws",
            "wss://ws.gdex.top",   # work
            "wss://kc-us-dex.xeldal.com/ws",
            "wss://bts.ai.la/ws",
            "wss://btsza.co.za:8091/ws",
            "wss://japan.bitshares.apasia.tech/ws",
            "wss://api.bts.blckchnd.com",
            "wss://bitshares-api.wancloud.io/ws",
            "wss://eu.nodes.bitshares.ws",  # work
            "wss://bitshares.crypto.fans/ws",
            "wss://dex.rnglab.org",
            "wss://ws.winex.pro",
            "wss://sg.nodes.bitshares.ws",
            "wss://us.nodes.bitshares.ws",
            "wss://bitshares.apasia.tech/ws",
            "wss://openledger.hk/ws",
            "wss://bitshares.dacplay.org/ws"
            ]
    }


def get_set(set_name):
    if not hasattr(sys.modules[__name__], set_name):
        raise NameError(f"Переменная '{set_name}' не найдена.")
    temp_set = getattr(sys.modules[__name__], set_name)
    if not isinstance(temp_set, dict):
        raise TypeError(f"Тип переменной '{set_name}' не <dict>.")
    for key in temp_set:
        if key not in __SET_DEFAULT:
            raise KeyError(f"Нepaзpeшённый ключ '{key}' в переменной '{set_name}'.")
    for key in __SET_DEFAULT:
        if key not in temp_set:
            temp_set[key] = __SET_DEFAULT[key]
    temp_set = dict(temp_set)
    # --
    if not isinstance(temp_set["request_processing_def"], (types.FunctionType, type(None))):
        raise TypeError(f"Тип аттрибута 'request_processing_def' должен быть <function> или <None>.")
    # --
    if not isinstance(temp_set["answer_processing_def"], (types.FunctionType, type(None))):
        raise TypeError(f"Тип аттрибута 'answer_processing_def' должен быть <function> или <None>.")
    # --
    if not isinstance(temp_set["ping"], (dict, type(None))):
        raise TypeError(f"Тип аттрибута 'ping' должен быть <dict> или <None>.")
    if isinstance(temp_set["ping"], dict):
        if "time_interval" in temp_set["ping"]:
            if not isinstance(temp_set["ping"]['time_interval'], (int, float)):
                raise TypeError(f"Тип аттрибута в переменной '{set_name}['ping']['time_interval']' должен быть <int> или <float>.")
            if temp_set["ping"]['time_interval'] < 1:
                raise ValueError(f"Аттрибут в переменной '{set_name}['ping']['time_interval']' должен быть >= 1.")
        else:
            raise KeyError(f"Нe найден ключ 'time_interval' в переменной '{set_name}['ping']'.")
        if "request" in temp_set["ping"]:
            pass
        else:
            raise KeyError(f"Нe найден ключ 'request' в переменной '{set_name}['ping']'.")
    # --