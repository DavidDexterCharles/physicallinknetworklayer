from socket import *
import json
from tools import *
from stuff import*
from clienterrorsimulator import ClientErrorSimulator
from clienteventhandler import ClientEventHandler

class ClientPhysicalLayer:
    framecount=0
    def __init__(self):
        self.serverName=""
        self.serverPort=0
        self.clientSocket=""
        self.ceh=ClientEventHandler()
        self.prevframe=""
        self.toresend=0
        
    def is_fith_frame(self): 
        if  ClientPhysicalLayer.framecount%5==0:
            return 1
        else:
            return 0
    
    def update_frame_counter(self):
        ClientPhysicalLayer.framecount+=1
        # print  ClientPhysicalLayer.framecount,"Counter"
    def get_frameCounter(self):
        return  ClientPhysicalLayer.framecount
    
    def establish_connection(self,host,port):
        self.serverName = gethostbyname(host)
        self.serverPort = port
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName,self.serverPort))
        # return clientSocket
        
        
    def send_frames(self,frames):
        ces=ClientErrorSimulator()
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName,self.serverPort))
        frames= stuff(list(frames))
        self.clientSocket.send(frames)
        # ces.update_frame_counter()
        # self.receive_frame()
        
        
    def receive_frame(self):
        ceh= ClientEventHandler()
        ack = self.clientSocket.recv(1024)
        print self.prevframe
        if ack==self.prevframe:#"00000001":
            ceh.ack_received_successfully(str(ack))
            self.toresend=0
            return ack
        elif len(ack)!=0:
            ceh.ack_received_with_error(str(ack))
            print  "Ack from server: ",ack
            print "frame resent"
            self.toresend=2
            return ack
        else:
            self.toresend=0
           
            print "sent bad checksum"
            print "No ack received, start-timer"
            # return 0
        # print 'Ack From Server:', ack , len(ack)
       
        return ack
    
    def sendStop(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName,self.serverPort))
        action= "0"
        self.clientSocket.send(action)
        self.clientSocket.close()