from socket import *
from random import randint
from serverlinklayer import ServerLinkLayer
from tools import *
from servererrorsimulator import ServerErrorSimulator
from servereventhandler import ServerEventHandler
class ServerPhysicallayer:

    def __init__(self):
        self.serverName=""
        self.serverPort = ""
        self.serverSocket ="" 
        self.connectionSocket, self.addr = "",""
        self.frame=""
        self.ses=ServerErrorSimulator()
        self.seh=ServerEventHandler()
        self.sll=ServerLinkLayer()
        # self.connectionSocket, self.addr = self.serverSocket.accept()
    
    def start_server(self,host,port):
        a=randint(10, 13)
        self.serverPort=port#int(str(12) + str(a))
        self.serverSocket = socket(AF_INET,SOCK_STREAM)
        self.serverSocket.bind((host, self.serverPort))
        self.serverSocket.listen(1)
        print  self.serverPort
        print 'The server is ready to receive'
        
        
    def send_Ackframes(self,no_error):
       
        ACK=""
        # print "SEQ numb ",self.sll.frame_seqnumber
        
        if(self.sll.frame_seqnumber==""):
            ACK=""
        else:
            self.ses.update_frame_counter()
            if no_error:
                ACK=htb(self.sll.frame_seqnumber)#+htb(self.sll.frame_seqnumber)
                # self.ses.update_frame_counter()
                
                print "Ack Before= ",ACK
                if(self.ses.is_eightth_frame()):
                    ACK=self.ses.flip_bit(ACK)
                    # ACK+=" simError"
                    print "Ack After= ",ACK
                    print "simulated error"
                else:
                     print "Ack After= ",ACK
                # print self.ses.framecount
                print "=================================================="
                self.seh.ack_sent(ACK)
                self.connectionSocket.send(ACK)
        print self.ses.framecount
        self.connectionSocket.close()

    def receive_frame(self):# GET FROM CLIENT
        self.connectionSocket, self.addr = self.serverSocket.accept()
        self.frame=self.connectionSocket.recv(1024)
        # if self.frame==0:
        #     return "end"
        NoChecksumError=self.send_frame_to_linklayer()
        if NoChecksumError:
            self.send_Ackframes(1)
        else:
            self.send_Ackframes(0)
        
    def send_frame_to_linklayer(self):
        return self.sll.receive_frame_from_physical(self.frame)
    