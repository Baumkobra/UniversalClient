
from math import ceil
from uuid import uuid4
import json

class Chunk:
    CHUNK = 4096
    
  
    def __init__(self) -> None:
        pass
    
    def format(self, message) -> list[bytes]:
        """
        returns a list of bytes objects in chunks
        1: Chunk the message
        2: convert to bytes
        Return: list containing formatted messages in bytes format
        """
        
        # calculating the amount of whitespaces that will be used 
        length_of_id = 40
        length_of_len = 5
        length_of_seq = 5
        length_of_number_of_chunks = 5
        
        length_of_dictionary_keys = 28
        # 2 is constant for {}, 6 bytes per entry for "" and whitespaces + 2 bytes for every entry-  1: ' ,' 
        length_of_delimiters = 2 + 5 * 6 + 4 * 2 
        
        length_of_delimiters_and_keys = length_of_id + length_of_len + length_of_seq + length_of_number_of_chunks + length_of_dictionary_keys + length_of_delimiters
        
        # calculating how much data can be packed into one message
        self.chunksize = self.CHUNK - length_of_delimiters_and_keys
        
        # calculating the numbers of chunks required:
        # Example: len = 2000 ==> 1+1 ==> 2 chunks
        number_of_chunks = ceil(len(message) / self.chunksize)
       
        # splits the message into chunksized strings and removes empty strings which can occur
        chunked_message_list = [message[x*self.chunksize:(x +1)*self.chunksize] for x in range(number_of_chunks)]
        if "" in chunked_message_list: chunked_message_list.remove("")
        
        # checking that everything works fine
        assert number_of_chunks == len(chunked_message_list)
        
        # creating a unique id for every message
        message_id = uuid4().__int__() 
        
        # creating a dictionary containing the data and metadata
        messagelist = [json.dumps({"data":item, 
                        "len":len(item).__str__()                    .ljust(length_of_len), 
                        "id":message_id.__str__()                    .ljust(length_of_id), 
                        "seq":(x + 1)        .__str__()                    .ljust(length_of_seq),
                        "number_of_chunks":number_of_chunks.__str__().ljust(length_of_number_of_chunks)
                        }) for x,item in enumerate(chunked_message_list)]
        # adding padding and converting to bytes
      
        return [li.ljust(self.CHUNK).encode("utf-8") for li in messagelist]

        
    class Message:
        def __init__(self, data_dict) -> None:
            self.data = data_dict["data"]
            self.len = int(data_dict["len"])
            self.id = data_dict["id"]
            # seq: 1. Element hat die seq 1, 
            self.seq = int(data_dict["seq"])
            self.number_of_chunks = int(data_dict["number_of_chunks"])
        
            
    class CombinedMessage:
        message_dict_by_id = {}
        seq_range_by_id = {}
        def __init__(self) -> None:
            pass
        
        def add(self,message):
            id = message.id
            seq = message.seq
            number_of_chunks = message.number_of_chunks
            
            # checking if there has already been a message with the same id, if not create a dict for the msg
            if not id in self.message_dict_by_id.keys(): self.message_dict_by_id.update({id:{}}); print(f"> Creating new message_by_id_dict for {id}")
            # checking if there has already been a message with the same id, if not save the number of chunks which will be expected
            if not id in self.seq_range_by_id: self.seq_range_by_id.update({id:list(range(1, int(number_of_chunks) + 1))}); print(f"> Calculating range of sequences which will be expected for {id}")

            # adding the new data to the dictionary
            self.message_dict_by_id[id].update({seq:message})
            
            # checking whether the message has been received entirelly
            if self.check_for_finished(id):
                # putting all the data back together
                final_msg = "".join(m.data for m in self.message_dict_by_id[id].values())
                print(f"> Completed message {id}")
                return final_msg
            return False
                   
        def check_for_finished(self,id):
            # all possible sequences
            seq_range = self.seq_range_by_id.get(id)
            # all sequences which have already been received
            received_seqs = list(self.message_dict_by_id.get(id).keys())

            # checking whether both lists have same length, if not, return False
            if len(seq_range) != len(received_seqs): return False
            # if all sequences have been received, return True
            if seq_range == received_seqs: return True
            


    def deformat_single_message(self,message_in_bytes) -> dict:
        """
        deformatting a single message and returning Message object
        """
        # decoding the data, then parsing it in json, then converting to a Message object for ease of use
        return self.Message(json.loads(message_in_bytes.decode("utf-8")))
    

    
        
if __name__ == "__main__":      
    # sending
    c = Chunk()
    x = c.format(open("testmsg.txt","r").read())



    # reading

    # Object for combining messages
    comb = Chunk().CombinedMessage()
    for m in x:
        # reading the bytes and converting it to a Chunk.Message object
        d = c.deformat_single_message(m)
        # adding all the messages up
        msg = comb.add(d)
        # CombinedMessage.add() returns False when the message is incomplete, and the data if the message is complete
        if msg:
            print(msg)
        