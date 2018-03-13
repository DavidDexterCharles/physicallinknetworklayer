import datetime
import json
class ClientEventHandler(object):
    eventcount=1
    def __init__(self):
        self.clientlogfile="client.log"
        self.theevent=""
        #For logging purposes identify the packet and the frame
        #within a packet by number for each event.
        #Begin counting packets and frames at 1.
        self.packetcount=0
        self.framecount=0
        
    
    def packet_sent_from_networklayer_to_linklayer(self,packetNumber):
        self.theevent="\n\n"+"Event Count:"+str(ClientEventHandler.eventcount)+"\n"+"\n"+datetime.datetime.now().isoformat()+"\n"+"Sent Packets to link layer:"+"Packet seq#: "+str(packetNumber)+"\n"
        ClientEventHandler.eventcount+=1
        self.write_event()
        return
    
    def frame_sent_from_linklayer_to_physicallayer(self,frameSeq):
        self.theevent="\n\n"+"Event Count:"+str(ClientEventHandler.eventcount)+"\n"+"\n"+datetime.datetime.now().isoformat()+"\n"+"Sent Frames to physical layer"+"Frame seq#:"+frameSeq+"\n"
        ClientEventHandler.eventcount+=1
        self.write_event()
        return
    
    def frame_resent_from_linklayer_to_physicallayer(self,frameSeq):
        self.theevent="\n\n"+"Event Count:"+str(ClientEventHandler.eventcount)+"\n"+"\n"+datetime.datetime.now().isoformat()+"\n"+"Resent Frames to physical layer: \n "+"Frame seq#:"+frameSeq+"\n"
        ClientEventHandler.eventcount+=1
        self.write_event()
        return
    
    def ack_received_successfully(self,seqNumber):
        #If the ACK frame is received successfully before 
        #the timer expires, the client sends the next frame of
        #the packet or gets the next packet from the network layer.
        self.theevent="\n\n"+"Event Count:"+str(ClientEventHandler.eventcount)+"\n"+"\n"+datetime.datetime.now().isoformat()+"\n"+"Ack recieved Succesfully: \n "+"Frame seq#:"+seqNumber+"\n"
        ClientEventHandler.eventcount+=1
        self.write_event()
        return
    
    def ack_received_with_error(self,seqNumber):
        #layer. If the ACK frame is received in error,
        #record the event in the log and continue the data link layer
        #as if the ACK was never received.
        self.theevent="\n\n"+"Event Count:"+str(ClientEventHandler.eventcount)+"\n"+"\n"+datetime.datetime.now().isoformat()+"\n"+"Ack recieved in error: \n "+"Frame seq#:"+seqNumber+"\n"
        ClientEventHandler.eventcount+=1
        self.write_event()
        return
    
    def timer_expired(self,frame):
        '''
        When the client times out due to either type of
        transmission error, it resends the same frame 
        with the correct error-detection byte.
        '''
        self.theevent="\n\n"+"Event Count:"+str(ClientEventHandler.eventcount)+"\n"+"\n"+datetime.datetime.now().isoformat()#+"\n"+"Ack recieved in error: \n "+"Frame seq#:"+seqNumber+"\n"
        self.theevent+="\nServer timed out Resending frame\n"+str(json.dumps(frame, sort_keys=True, indent=4))+"\n\n"
        ClientEventHandler.eventcount+=1
        self.write_event()
        return
    
    def write_event(self):
        #The client records significant events in a log
        #file client.log.
        with open(self.clientlogfile, "a") as logfile:
            logfile.write(self.theevent)