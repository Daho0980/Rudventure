import re
import time

from . import (
    status as s,
    rules  as r
)


_ansiCompile = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
escapeAnsi   = lambda l: _ansiCompile.sub('',l)

systemCommand = ("RCC", "RGS")

def addChat(data:list|None):
    if data:
        s.history['chat'].append(data)
        if len(s.history['chat']) > s.history['max']:
            s.history['chat'].pop(0)

def sendChat(data:list):
    if s.serverConnection and s.client.isConnect: s.client.sendData(data)
    if data[0] not in systemCommand: addChat(data)

def receiveChat():
    data = s.client.receiveData()
    if data == "excepted":
        return "excepted"
    else: addChat(data)


def error(text:str, exception:Exception|bool=False, speaker:bool=False):
    sender = sendChat if speaker else addChat
    sender(["Error", text, 'R'])
    if exception and r.command['showErrorOutput']:
        sender([exception.__class__.__name__, str(exception), 'R'])

def explanation(text:str, speaker:bool=False):
    sender = sendChat if speaker else addChat
    sender(["Explanation", text, 'G1'])

def warning(text:str, speaker:bool=False):
    sender = sendChat if speaker else addChat
    sender(["Warning", text, 'Y'])

def info(text:str, speaker:bool=False):
    sender = sendChat if speaker else addChat
    sender(["Info", text, 'B1'])

def output(text:str, speaker:bool=False):
    sender = sendChat if speaker else addChat
    sender(["Output", text, 'F'])

def direct(sendType:str, data) -> tuple:
    sendChat([sendType, data])
    time.sleep(0.1)

    return s.client.statusData.pop()