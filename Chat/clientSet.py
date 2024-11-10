import socket

from . import mainFunctions as mf


class FakeClient:
    host       = None
    port       = None
    isConnect  = False
    statusData = []

    def sendData(self, _): ...
    def receiveData(self): ...
    def close(self):       ...

class Client:
    def __init__(self, host='localhost', port=None):
        self.host = host
        self.port = port

        self.sendedData = ("server", "")

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.chatData   = []
        self.statusData = []

        self.isConnect = True

        try: self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print(f"'{self.host}:{self.port}'에서 요청을 수락하지 않았습니다 : {e}")
            exit(0)

    def sendData(self, data):
        self.sendedData = ("server", data)
        self.client_socket.sendall(str(data).encode())

    def receiveData(self) -> list|None|str:
        try:
            self.client_socket.settimeout(0.01)
            socketMessages = self.client_socket.recv(1024).decode().split('&')
            data           = eval(socketMessages.pop(0))

            # self.chatData.extend(socketMessages)
            if data[0] in ("RGS.REC", "RCC.REC"):
                self.statusData.append(data)
                return

        except socket.timeout:
            return None
        
        except Exception as e:
            mf.addChat(["system", f"서버와 연결이 끊어졌습니다. : {e}", 'Y'])
            self.isConnect = False
            self.client_socket.close()
            mf.addChat(["system", "소켓이 닫혔습니다.", 'Y'])
            return "excepted"
        
        return None if("server",data[1].split(" : "))==self.sendedData else data

    def close(self):
        self.client_socket.close()