import struct

class Message:
    def __init__(self, chuck, checksum : int, counter : int):
        self.chuck = chuck
        self.checksum = checksum
        self.counter = counter
    def get_struct(self):
        #covert chuck to bytes
        if type(self.chuck) == str:
            #convert to ascii
            self.chuck = self.chuck.encode('ascii')
        return struct.pack('4sHH', self.chuck, self.checksum, self.counter)
    
    @staticmethod
    def fromBytesToMessage(raw_message):
        return Message(*struct.unpack('4sHH', bytes(raw_message)))
        
    
    def __str__(self):
        return f'Chuck: {self.chuck}, Checksum: {self.checksum}, Counter: {self.counter}'
 
class MessageConstructor:
    def __init__(self):
        self.counter = 0

    def checksum(self, message):
        return sum(ord(c) for c in message) % 2**16 # 16 bit checksum

    def create_message(self, message):
        chunks = [message[i:i+4] for i in range(0, len(message), 4)]# every 4 letters
        m_array = []
        for chunk in chunks:
            self.counter = (self.counter + 1) % 2**16 # 16 bit counter
            cs = self.checksum(chunk)
            #print(f'Sending chunk: {chunk}, Checksum: {cs}, Counter: {self.counter}')
            m = Message(chunk, cs, self.counter).get_struct()
            m_array.append(m)
        return m_array