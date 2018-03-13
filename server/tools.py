import binascii
import json


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
    
def checksum(line):
    b=[line[i:i+8] for i in range(0, len(line), 8)]
    y='{0:b}'.format(int(b[0],2) ^ int(b[1],2)).zfill(8)
    
    for i in range(2,len(b)):
        y='{0:b}'.format(int(y,2) ^ int(b[i],2)).zfill(8)
    return y