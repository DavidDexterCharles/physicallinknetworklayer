
from socket import *
from clientnetworklayer import network_layer
from clientphysicallayer import ClientPhysicalLayer
import time

open('client.log', 'w').close()
def client_process(cpl):
    cpl.establish_connection('localhost',1212)
   

cpl=ClientPhysicalLayer()
client_process(cpl)
network_layer(cpl)