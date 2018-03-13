import binascii
from clienteventhandler import ClientEventHandler
from clienterrorsimulator import ClientErrorSimulator
from checksum import checksum
import json
import time


def dopad(binary_string):
    bsize=len(binary_string)
    while bsize%8!=0:
        binary_string="0"+binary_string
        bsize=len(binary_string)
    return binary_string

def htb(h):   #hext to binary
    h=h.replace(' ', '')
    binary_string=bin(int(h, 16))[2:]
    binary_string=dopad(binary_string)
    return binary_string

def bth(binary_string):
    hstr = '%0*X' % ((len(binary_string) + 3) // 4, int(binary_string, 2))
    return hstr

def buildframe(numframes,packet):
    binary_string=htb(packet)
    firstpart='{"startFlag":["7e"],"Address": ["ff"],"Information": ["'
    middlepart='"],"FCS": ["'
    frames=[]
    if numframes==1:
        frames.insert(1,firstpart+packet.replace(' ', '')+middlepart+str(bth(checksum(binary_string)))+'"],"endFlag": ["7e"],"SeqNo":["'+str(1)+'"],"EndOfPacket":["'+str(1)+'"],"FrameId":["0"]}')              
    else:
        # print "grapes"
        splitpoint=0
        for i in range(0,numframes):
            partofpacket=binary_string[splitpoint:splitpoint+480]
            hexstring=bth(partofpacket)
            # print len(partofpacket),"\n"
           
            frames.insert(i+1,firstpart+hexstring+middlepart+str(bth(checksum(partofpacket)))+'"],"endFlag": ["7e"],"SeqNo":["'+str(i+1)+'"],"EndOfPacket":["00"],"FrameId":["0"]}')
            splitpoint+=480
        if len(binary_string)%(60*8)>0:
            partofpacket = binary_string[splitpoint:len(binary_string)]
            hexstring=bth(partofpacket)
            frames.insert(numframes+1,firstpart+hexstring+middlepart+str(bth(checksum(partofpacket)))+'"],"endFlag": ["7e"],"SeqNo":["'+str(numframes+1)+'"],"EndOfPacket":["01"],"FrameId":["0"]}')
    return frames

def frame_to_bits(frame):
    finalbstring=""
    finalbstring+=htb(frame["startFlag"][0])#7e
    finalbstring+=htb(frame["Address"][0])#ff
    finalbstring+=htb(frame["SeqNo"][0])#
    finalbstring+=htb(frame["Information"][0])
    finalbstring+=htb(frame["FCS"][0])
    finalbstring+=htb(frame["EndOfPacket"][0])
    finalbstring+=htb(frame["endFlag"][0])
    finalbstring+=htb(frame["FrameId"][0])
    return finalbstring
 
    
def linklayer(cpl,packet):
    binary_string=htb(packet)
    frames=[]
    ceh=ClientEventHandler()
    ces=ClientErrorSimulator()   
    # print len(binary_string)/8
    if len(binary_string)/8<=60:
        # print binary_string
        numframes=1
        frames= buildframe(numframes,packet)
    else:
        # print "apples"
        numframes=len(binary_string)/(60*8)
        frames= buildframe(numframes,packet)
    
    for i in range(0,len(frames)):
                    frame  = json.loads(frames[i])
                    # print frame["Information"][0],frame["SeqNo"],frame["FCS"]
                    ceh.frame_sent_from_linklayer_to_physicallayer(str(frame["FCS"][0]))
                    cpl.update_frame_counter()
                    frame["FrameId"][0]=str(cpl.get_frameCounter())
                    originalframeFCS=frame["FCS"][0]
                    flippedbit=""
                    if cpl.is_fith_frame():
                        flippedbit=ces.flip_bit(htb(frame["FCS"][0]))
                        print "BeforeFlip2", htb(frame["FCS"][0])
                        frame["FCS"][0]=bth(flippedbit)
                        print "AfterFlip2", flippedbit
                  
                    
                    print "FrameId:",frame["FrameId"]
                    cpl.send_frames(frame_to_bits(frame))
                    cpl.prevframe=htb(frame["SeqNo"][0])
                    ack=cpl.receive_frame()
                    # print "BeforeFlip2", frame["FCS"][0]
                    # print "AfterFlip2", flippedbit
                    if len(ack)==0:
                        secs=0
                        
                        while secs != 6:
                            print ">>>>>>>>>>>>>>>>>>>>>", secs
                            # Sleep for a 10 seconds
                            time.sleep(1)
                            # Increment the secon total
                            secs += 1
                        
                        flippedbit=ces.flip_bit(htb(frame["FCS"][0]))
                        print "BeforeFlip2", htb(frame["FCS"][0])
                        frame["FCS"][0]=bth(flippedbit)
                        print "AfterFlip2", flippedbit
                        cpl.send_frames(frame_to_bits(frame))
                        ack=cpl.receive_frame()
                        ceh.timer_expired(frame)
                        print "New Ack from server: ",ack
                    print "================================================="    
                    while  cpl.toresend==2:
                        print "Sent frame Result"
                        cpl.send_frames(frame_to_bits(frame))
                        cpl.receive_frame()
              
                    
    # cpl.sendStop()
   
    return frames
    
    
    
    # import time
    # run = raw_input("Start? > ")
    # mins = 0
    # # Only run if the user types in "start"
    # if run == "start":
    #     # Loop until we reach 20 minutes running
    #     while mins != 20:
    #         print ">>>>>>>>>>>>>>>>>>>>>", mins
    #         # Sleep for a minute
    #         time.sleep(60)
    #         # Increment the minute total
    #         mins += 1