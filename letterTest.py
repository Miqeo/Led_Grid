import cv2
import time
from PIL import Image
import numpy as np
import socket
import sys

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

UDP_IP = sys.argv[1]
UDP_PORT = 4210
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

size = [6, 5]

back = (0, 0, 0)
front = (255, 255, 255)

pixelsBack = [[(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0)],
            [(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0)],
            [(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0)],
            [(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0)],
            [(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0)]]

pixels = pixelsBack

class Glyph:
    offset = 0
    width = 0
    letterType = ""
    
    def __init__(self, offset, width, letterType):
        self.offset = offset
        self.width = width
        self.letterType = letterType

        
def showBack():
    send(pixelsBack)

def send(arr):
    array = np.array(arr, dtype=np.uint8)
    image = np.array(array)
    
    cv2.imshow("preview", image)
    
    arrB = b""
    
    
    for y in range(0, size[1]):
        for x in range(0, size[0]):
            for i in range(0, 3):
                color = arr[y][x][i]
            
                print(hex(color))
                arrB += bytes(hex(color),"utf-8")
            
#            arr += bytes(hex(color[1]),"utf-8")
#            arr += bytes(hex(color[2]),"utf-8")
                   
    MESSAGE = arrB

    print("message: %s" % MESSAGE)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

t = True
f = False

glyps = {
    "A" : [[f,t,f],[t,f,t],[t,f,t],[t,t,t],[t,f,t]],
    "B" : [[t,t,f],[t,f,t],[t,t,f],[t,f,t],[t,t,t]],
    "C" : [[f,t,t],[t,f,f],[t,f,f],[t,f,f],[f,t,t]],
    "D" : [[t,t,f],[t,f,t],[t,f,t],[t,f,t],[t,t,f]],
    "E" : [[t,t,t],[t,f,f],[t,t,f],[t,f,f],[t,t,t]],
    "F" : [[t,t,t],[t,f,f],[t,t,f],[t,f,f],[t,f,f]],
    "G" : [[f,t,t],[t,f,f],[t,f,t],[t,f,t],[f,t,t]],
    "H" : [[t,f,t],[t,f,t],[t,t,t],[t,f,t],[t,f,t]],
    "I" : [[t],[t],[t],[t],[t]],
    "J" : [[f,t],[f,t],[f,t],[f,t],[t,f]],
    "K" : [[t,f,t],[t,f,t],[t,t,f],[t,f,t],[t,f,t]],
    "L" : [[t,f],[t,f],[t,f],[t,f],[t,t]],
    "M" : [[f,t,f,t,f],[f,t,f,t,f],[t,f,t,f,t],[t,f,t,f,t],[t,f,f,f,t],],
    "N" : [[t,f,f,t],[t,t,f,t],[t,f,t,t],[t,f,f,t],[t,f,f,t]],
    "O" : [[f,t,f],[t,f,t],[t,f,t],[t,f,t],[f,t,f]],
    "P" : [[t,t,f],[t,f,t],[t,t,f],[t,f,f],[t,f,f]],
    "R" : [[t,t,f],[t,f,t],[t,t,f],[t,f,t],[t,f,t]],
    "S" : [[f,t,t],[t,f,f],[f,t,f],[f,f,t],[t,t,f]],
    "T" : [[t,t,t],[f,t,f],[f,t,f],[f,t,f],[f,t,f]],
    "U" : [[t,f,t],[t,f,t],[t,f,t],[t,f,t],[f,t,f]],
    "V" : [[t,f,t],[t,f,t],[t,f,t],[f,t,f],[f,t,f]],
    "W" : [[t,f,f,f,t],[t,f,t,f,t],[t,f,t,f,t],[f,t,f,t,f],[f,t,f,t,f]],
    "X" : [[t,f,t],[t,f,t],[f,t,f],[t,f,t],[t,f,t]],
    "Y" : [[t,f,t],[t,f,t],[f,t,f],[f,t,f],[f,t,f]],
    "Z" : [[t,t,t],[f,f,t],[f,t,f],[t,f,f],[t,t,t]],

    "!" : [[t],[t],[t],[f],[t]],
    "?" : [[t,t],[f,t],[t,f],[f,f],[t,f]],
    "*" : [[f,f,f],[t,f,t],[f,t,f],[t,f,t],[f,f,f]],
    "-" : [[f,f],[f,f],[t,t],[f,f],[f,f]],
    "_" : [[f,f],[f,f],[f,f],[f,f],[t,t]],
    " " : [[f],[f],[f],[f],[f]]
}


def letterStr(sentence):
    letterData = [[],[],[],[],[]]
    for height in range(0, 5):
        for let in sentence:
            for count in range(0, len(glyps[let][0])):
                print(count)
                print(glyps[let][height][count])
                letterData[height].append(glyps[let][height][count])
            print("-----")
            letterData[height].append(False)
        for a in range(5):
            letterData[height].append(False)
        
        
    
    return letterData

def show(text):

    letterData = letterStr(text)
        
    i = 0
    last = len(letterData[0]) - 1
    
    while True:
        for a in range(0, size[1]):
            for b in range(0, 5):
                if (b > 4):
                    break
                pixels[a][b] = pixels[a][b + 1]
            if (i < last):
                pixels[a][5] = front if letterData[a][i] else back  
            else: 
                i = -1
            
        send(pixels)

        time.sleep(0.2)
        i += 1
        
        
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
        
showBack()
show("HELLO WORLD!")
#"ABCDEFGHIJKLMNOPRSTUVWXYZ !?*-_"

vc.release()
cv2.destroyWindow("preview")

