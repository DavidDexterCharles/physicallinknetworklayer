
class ServerNetworkLayer(object):
    
    def __init__(self):
        self.packet=""
    
    
    def write_packet_to_serveroutputfile(self):
        with open("server.out", "a") as myfile:
            myfile.write(self.packet)
    
    def receive_from_link_layer(self,packet):
        self.packet=packet+"\n"
        self.write_packet_to_serveroutputfile()