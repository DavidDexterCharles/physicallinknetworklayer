from serverphysicallayer import ServerPhysicallayer

spl=ServerPhysicallayer()
spl.start_server("localhost",1212)
# ackframe = '{"startFlag":["7e"],"Address": ["ff"],"SeqNo":["'+str(3)+'"],"FCS":["00"],endFlag":["7e"]}'
open('server.log', 'w').close()
open('server.out', 'w').close()
status=""
while status!="end":
    
    status=spl.receive_frame()
    
    # spl.send_Ackframes("fish")
    