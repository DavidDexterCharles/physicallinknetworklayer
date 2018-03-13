import json
import datetime
class ServerEventHandler(object):
    eventcount=1
    def __init__(self):
        self.serverlogfile="server.log"
        self.theevent=""
       
     
    
    def received_data_frame_in_error(self):
        # print "David Received Frame in Error"
        self.theevent=str(ServerEventHandler.eventcount)+":\nTime:"+datetime.datetime.now().isoformat()
        self.theevent+="\nReceived frame in error from client\n\n"
        self.write_event()
        ServerEventHandler.eventcount+=1
        return
    
    def received_data_frame(self,frame):
        self.theevent=str(ServerEventHandler.eventcount)+":\nTime:"+datetime.datetime.now().isoformat()
        
        self.theevent+="\nFrame Received"+str(json.dumps(frame, sort_keys=True, indent=4))+"\n\n"
        self.write_event()
        ServerEventHandler.eventcount+=1
        return
    
    def received_duplicate_frame(self,frame):
        '''
        the server needs to send an ACK when a duplicate frame
        is received due to possibly damaged ACKs.
        '''
        self.theevent=str(ServerEventHandler.eventcount)+":\nTime:"+datetime.datetime.now().isoformat()
        self.theevent+="\nDuplicate Frames Received due to bad ACK"+str(json.dumps(frame, sort_keys=True, indent=4))+"\n\n"
        self.write_event()
        ServerEventHandler.eventcount+=1
        return
    
    def ack_sent(self,ack):
        self.theevent=str(ServerEventHandler.eventcount)+":\nTime:"+datetime.datetime.now().isoformat()
        self.theevent+="\nACK sent to client\n"+str(ack)+"\n\n"
        self.write_event()
        ServerEventHandler.eventcount+=1
        return
    
    def packet_sent_to_network_layer(self):
        self.theevent=str(ServerEventHandler.eventcount)+":\nTime:"+datetime.datetime.now().isoformat()
        self.theevent+="\nPacket sent to Network Layer\n\n"
        self.write_event()
        ServerEventHandler.eventcount+=1
        return
    
    def write_event(self):
       # The server records significant events including frame
       #received, frame received in error, duplicate frame received,
       #ACK sent, and packet sent to the
       #network layer in server.log.
        with open(self.serverlogfile, "a") as logfile:
            logfile.write(self.theevent)