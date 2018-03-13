
class ServerErrorSimulator(object):
    
    '''
    Force a server transmission error every 8th
    ACK frame sent by flipping any single bit in the error-
    detection byte prior to transmission of the frame.
    ACK frames 8, 16, 24, ... sent by the server
    will be perceived as error by the client.)
    '''
    
    def __init__(self):
        self.clientlogfile="server.log"
        self.framecount=0
        
    def is_eightth_frame(self): 
        if  self.framecount%8==0:
            return 1
        else:
            return 0
    
    def update_frame_counter(self):
        self.framecount+=1
    
    def flip_bit(self,ACK): #flip the 3rd bit
        list1 = list(ACK)
        if list1[2]=='1':
          list1[2]='0'
        #   print list1[2],"inside"
        else:
            list1[2]='1'
        ACK = str(''.join(list1))
        return ACK
        
    '''
    Error-Detection Use a byte-by-byte XOR of all 
    the internal bytes for creating your error-
    detection CRC byte. For the ACK frame, the error 
    detection byte becomes simply a copy of the
    sequence number byte.
    '''