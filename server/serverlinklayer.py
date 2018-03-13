import binascii
import json
from stuff import stuff,unstuff
from tools import*
from servereventhandler import ServerEventHandler
from servernetworklayer import ServerNetworkLayer

class ServerLinkLayer(object):
    
    def __init__(self):
        self.frames=""
        self.tempframe = ""
        self.packetData=""
        self.frame_seqnumber=""
        self.prevFrameId=""
        self.endoftempframe=""
        self.seh=ServerEventHandler()
        self.snl=ServerNetworkLayer()
        self.prevSeq=""
        
    def receive_frame_from_physical(self,frame):
        
        self.tempframe= self.unstuff_packet(list(frame))
        return self.reassemble_packet(frame)
        
    #  def receive_frame_from_physical(self,frame):
    #     if self.check_received_frames_for_duplicates!=1:
    #         self.tempframe=frame
    #             self.tempframe=""
    #         else:
    #             self.tempframe=frame
    #             self.prevSeq=frame[16:24]
            
    #         return self.reassemble_packet(frame)
        
    def reassemble_packet(self,aframe):
        frame={}
        bsize=len(self.tempframe)
        if bsize>0:
            # print self.tempframe
            # print bsize
            # print bth(str(self.tempframe))
            
            # print "Before:","SeqNo:",self.frame_seqnumber,"EndOfPacket:",self.EOP
            self.endoftempframe=self.tempframe[-32:]
            NoError=self.chek_errordetectionbyte_of_frame()
            print "value of NoError before:",NoError
            if NoError:
                
                # print endoftempframe[0:8]
                # print bth(str(endoftempframe[0:8]))
                frame["startFlag"]=bth(self.tempframe[0:8])
                frame["Address"]=bth(self.tempframe[8:16])
                frame["SeqNo"]=bth(self.tempframe[16:24])
                
                frame["Information"]=bth(self.tempframe[24:bsize-len( self.endoftempframe)])
                
                
                frame["FCS"]= bth(str( self.endoftempframe[0:8]))
                frame["EndOfPacket"]=bth( self.endoftempframe[8:16])
                frame["endFlag"]=bth( self.endoftempframe[16:24])
                frame["FrameId"]=bth( self.endoftempframe[24:32])
                # print "The EndOfPacket is ",frame["EndOfPacket"]
                print "Previous frame ID",self.prevFrameId
                print "FrameId:", frame["FrameId"]
                
                if self.prevFrameId!=frame["FrameId"]:
                    if frame["EndOfPacket"]=="01":
                        self.frames+=frame["Information"]
                        self.send_packet_to_networklayer(self.frames)
                        self.frames=""
                        self.prevFrameId=frame["FrameId"]
                  
                    else:
                        self.frames+=frame["Information"]
                        self.prevFrameId=frame["FrameId"]
                    # self.send_packet_to_networklayer(frame["Information"])
                    
                    # if self.EOP==frame["EndOfPacket"] and self.frame_seqnumber==frame["SeqNo"]:
                    #     self.seh.received_data_frame(frame)
                    # else:
                    self.seh.received_data_frame(frame)
                        
                    self.frame_seqnumber= frame["SeqNo"]
                    # self.EOP=frame["EndOfPacket"]
                    # print "After:","SeqNo:",self.frame_seqnumber,"EndOfPacket:",self.EOP
                    print "value of NoError after:",NoError
                else:
                    print "Duplicate frame received"
                    self.seh.received_duplicate_frame(frame)
                return NoError
            else:
                print "There was erro here, due to client so we ignore the frame and wait for resent frame"
                print "value of NoError after:",NoError
                self.prevFrameId=-1
                print "=================================================="
                return NoError
        
    def unstuff_packet(self,frame):
        #do unstuffing
        return unstuff(frame)
        # return self.chek_errordetectionbyte_of_frame()
        
    
    def send_packet_to_networklayer(self,packet):
        self.snl.receive_from_link_layer(packet)
        self.seh.packet_sent_to_network_layer()
        
    
    
    
    def chek_errordetectionbyte_of_frame(self):
        #check for an error in error-detection byte of frame
        bsize=len(self.tempframe)
        cfromclient=self.endoftempframe[0:8]
        cfromserver=checksum(self.tempframe[24:bsize-len(self.endoftempframe)])
        if cfromclient==cfromserver:
            print "No Error in Checksum",cfromclient,cfromserver
            # self.seh.received_data_frame(frame)
            # print "=================================================="
            return 1
        else:
            self.seh.received_data_frame_in_error()
            print "Error detected in Checksum",cfromclient,cfromserver
            
            return 0
        
    
    # def check_received_frames_for_duplicates(self, frame):
        
    #      if frame[16:24]==self.prevSeq:
    #          return 1
    #     # #If duplicate frame received due to possibly damaged ACK let server send ACK
    #     #return ack[seqnooftheduplicatedframe]
    #     return
    
  