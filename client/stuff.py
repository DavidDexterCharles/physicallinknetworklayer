# bits=[0,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,1,0]

def stuff1(bits):
                counter=0
                for i in range(0,len(bits)):
                    print bits[i]
                    if bits[i]==1:
                        counter+=1
                        if counter==6:
                            print "insert zero:" + str(i+1)+" "
                            counter=0
                            if bits[i+1] ==0:
                                print " deleted bit/stuffed"+ str(i+1)
                            if bits[i+1]==1 and bits[i+2]==0:
                              print "Is Flag"+ str()
               

# bits=[1,0,0,1,1,1,1,1,0,1,1,0]
def stuff(bits):
    
            stuffed=[]
            count=0
            for i in range(len(bits)):
                if bits[i]==1:
                    stuffed.append(bits[i])
                    count=count+1
                    
                elif bits[i]!=1:
                    count=0
                    stuffed.append(bits[i])
                if count==5:
                        stuffed.append(0)
                        count=0
                        
            stuffed=''.join(stuffed)
                    
            return str(stuffed)

            
def unstuff(bits):
    
            unstuffed=[]
            count=0
            a=0
            i=0
            while i<(len(bits)):
                
                
                unstuffed.append(bits[i])
                if bits[i]==0:
           
                    count=0
                if bits[i]==1:
                    count=count+1
                    
                if count==5:
                    if bits[i+1]==0:
                        unstuffed.append(bits[i+2])
                        count =0
                        i=i+2
                        
                i=i+1        
            unstuffed=''.join(unstuffed)      
            return str(unstuffed) 

# c=stuff(bits)
# print bits
# print c

# d= unstuff(c)
# print d
