def checksum(line):
    b=[line[i:i+8] for i in range(0, len(line), 8)]
    y='{0:b}'.format(int(b[0],2) ^ int(b[1],2)).zfill(8)
    
    for i in range(2,len(b)):
        y='{0:b}'.format(int(y,2) ^ int(b[i],2)).zfill(8)
    return y