
from Message import *
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from multiprocessing import Process
from timeit import timeit
HOST, PORT = "127.0.0.1",50000


class UniversalClient:
    chunker = Chunk()
    combinator = chunker.CombinedMessage()
    
    def __init__(self, connection:socket) -> None:
        print("initializing UniversalClient")
        # the socket of the PEER
        self.connection = connection
        self.connection.setblocking(True)
        
        # starting 
        self.receive_process = Thread(target=self.receive)
        self.receive_process.start()
        
        self.send("asdlfköasdf")
        
        
    def send(self,data):
        chunked_messages = self.chunker.format(data)
        chunked_messages:list[bytes]
        for message in chunked_messages:
            message:bytes
            self.connection.send(message)
            
  
            
    def receive(self):
        while True:
            # receiving data from the connection
            data = self.connection.recv(Chunk.CHUNK)
            print(data)
            # giving the data to a Childprocess, as to not halt the receive Process
        
            self.read_message(data)
        
            
    def read_message(self, data):
        """
        Interpreting Data, used as a Process
        """
        # formatting the data to a dict
        deformatted_mes = self.chunker.deformat_single_message(data)
        # adding the data to the combinator, returns False if still waiting for packets
        msg = self.combinator.add(deformatted_mes)
        
        if msg:
            # full message was received, ...
            print(msg)
                 

if __name__ == "__main__":
    UniversalClient()