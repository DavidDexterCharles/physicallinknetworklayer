
class ClientErrorSimulator(object):
    
    '''
    Force a client transmission error in every 5th frame 
    sent by flipping any single bit in the error-
    detection byte prior to transmission of the frame.
    frames 5, 10, 15, ... sent by the
    client will be perceived as in error by the server
    '''
    
    def __init__(self):
        self.clientlogfile="client.log"
        self.framecount=0
        
    
    
    def flip_bit(self,checksum): #flip the 3rd bit
        list1 = list(checksum)
        # print list1
        if list1[2]=='1':
          list1[2]='0'
        #   print list1[2],"inside"
        else:
            list1[2]='1'
        checksum = str(''.join(list1))
        return checksum
        
    '''
    Error-Detection Use a byte-by-byte XOR of all 
    the internal bytes for creating your error-
    detection CRC byte. For the ACK frame, the error 
    detection byte becomes simply a copy of the
    sequence number byte.
    '''