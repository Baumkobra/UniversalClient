from Universalclient import *

"""
Ev3 Side Server
"""



class Server(UniversalClient):
    
    def __init__(self) -> None:
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.setblocking(True)
        self.socket.bind((HOST,PORT))
        self.socket.listen()
        self.accept()
        
        
    def accept(self):
        print("accepting")
        connection, addr = self.socket.accept()
        print("accepted")
        # starting UniversalClient
        super().__init__(connection=connection)
        print(addr)
        

        
        
if __name__ == "__main__":
    Server()
    print("True")