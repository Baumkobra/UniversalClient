from Universalclient import *

"""
Computer Side Client
"""

class Client(UniversalClient): 
    
    def __init__(self) -> None:
        self.connection = socket(AF_INET,SOCK_STREAM)
        self.connection.setblocking(True)
        self.connect()
        
    
    def connect(self): 
        print("connecting")
        self.connection.connect((HOST,PORT))
        print("connected")
       
        super().__init__(self.connection)
        
        
        
if __name__ == "__main__":
    client = Client()
    while True:
        client.send(input("input: "))
