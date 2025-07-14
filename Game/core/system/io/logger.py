import time ;   import socket ; import threading
from   random                   import randrange

from Assets.data.color   import cColors   as cc
from Game.utils.graphics import escapeAnsi

from Assets.data import (
    totalGameStatus as s,
    flags           as f
)


class Server:
    def __init__(self, host='localhost', port=-1):
        self.host = host
        self.port = randrange(1024, 49152) if port==-1 else port
        s.port    = self.port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.connected_clients = []

    def clientAccepter(self):
        while True:
            conn, addr = self.server_socket.accept()
            addLog(f"{cc['fg']['Y']}{':'.join(map(str, addr))}{cc['end']} 연결됨", colorKey='Y')
            self.connected_clients.append((conn, addr))

            threading.Thread(target=self.clientHandler, args=(conn, addr)).start()
            time.sleep(0.1)

    def clientHandler(self, conn, addr):
        try:
            while True:
                if not (data:=eval(self.receiveData(conn).decode())): break

                match data[0]:
                    # TODO: str(("RCC.REC", ...))에서 왜 여타 타입을 배제하는지 알아내기
                    # 일단은 str으로 메꿈
                    case "RCC":
                        try:
                            exec(data[1])
                            self.sendData(conn, addr, str(("RCC.REC", 'True')))

                        except: self.sendData(conn, addr, str(("RCC.REC", 'False')))

                        continue
                    
                    case "RGS":
                        self.sendData(conn, addr, str(("RGS.REC", (status:=eval(data[1]), str(type(status))[8:-2]))))
                        
                        continue
                    
                addLog(escapeAnsi(f"{data[0]} : {data[1]}"))
                
        except Exception as e: addLog(f"{cc['fg']['Y']}{':'.join(map(str, addr))}{cc['end']} 통신 오류 발생 : {e}", colorKey='Y')
        finally:
            conn.close()
            addLog(f"{cc['fg']['Y']}{':'.join(map(str, addr))}{cc['end']} 연결 종료됨", colorKey='Y')
            self.connected_clients.remove((conn, addr))

    def receiveData(self, conn):
        return conn.recv(1024)

    def sendData(self, conn, addr, data:str):
        if ':'.join(map(str, addr)) not in eval(data)[1]:
            conn.sendall(f"{data}&".encode())

    def close(self):
        self.server_socket.close()


def add(text, duration):
    s.onDisplay.append(text)
    s.onTime   .append(duration)

def addLog(text:str, duration:int=50, colorKey:str='E') -> None:
    """
    게임 내 최하단에 출력되는 로그를 작성하는 함수

        `text`(str)     : 로그의 내용.
        `duration`(int) : 로그가 표시될 시간, 1초는 10으로 계산함, 기본적으로 `50`으로 설정되어 있음.
        `colorKey`(str) : 채팅으로 보내질 색의 키. 기본적으로 `E(기본)`으로 설정되어 있음.
    """

    if   len(s.onDisplay) <  s.maxStack: add(text, duration)
    elif len(s.onDisplay) >= s.maxStack:
        s.onDisplay.pop(0)
        s.onTime   .pop(0)
        add(text, duration)
    
    for conn, addr in server.connected_clients:
        server.sendData(conn, addr, str(("", escapeAnsi(text), colorKey)))

def clear() -> None:
    s.onDisplay.clear()
    s.onTime   .clear()

server = Server()

threading.Thread(target=server.clientAccepter, daemon=True).start()

def logChecker() -> None:
    while s.main:
        if f.jpsf and not f.pause:
            time.sleep(0.1)
            if s.onTime: s.onTime = list(map(lambda t: t-1, s.onTime))

            s.infoWindow['time'] -= 1 if s.infoWindow['time'] else 0
            if not s.infoWindow['time']: s.infoWindow['text'] = ""
            
            while 0 in s.onTime:
                del s.onDisplay[s.onTime.index(0)]
                del s.onTime   [s.onTime.index(0)]
        else: time.sleep(0.5)

threading.Thread(target=logChecker, name="logger", daemon=True).start()
