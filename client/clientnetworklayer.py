# import json
from clientdatalinklayer import linklayer
from clienteventhandler import ClientEventHandler
import time

def network_layer(cpl):
    with open("input.raw") as f:
        i=0
     
        for line in f:
            # content = [x.strip() for x in content]
            ceh=ClientEventHandler()
            ceh.packet_sent_from_networklayer_to_linklayer(i)
            result= line.strip().split('  ')
           
            if i==0:
                i+=1
            else:
                # print result[0],result[1]
                # frames= linklayer(result[1])
                # frame  = json.loads(frames[0])
             
                linefromfile= linklayer(cpl,result[1])
            
                # time.sleep(5)
                # for i in range(0,len(frames)):
                #     frame  = json.loads(frames[i])
                #     print frame["Information"],frame["SeqNo"],frame["FCS"]
                # print htb(frame["Information"][0])
                # print bth(htb((frame["Information"][0])))
                # print htb(bth(htb((frame["Information"][0]))))
               
        # print content