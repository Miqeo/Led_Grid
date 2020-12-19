import cv2
import time
from PIL import Image
import socket
import sys

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
    
size = [6, 5]
UDP_IP = sys.argv[1]
UDP_PORT = 4210
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)


while rval:
    resized = cv2.resize(frame, (size[0], size[1]))
    
    resized = cv2.flip(resized, 1)
    
    cv2.imshow("preview", resized)
    rval, frame = vc.read()
#    time.sleep(0.01)
    
    
    ##----------------------
    
    arr = b""
    
    pixCount = size[0] * size[1]
    
    
    for y in range(0, size[1]):

        for x in range(0, size[0]):
            b,g,r = resized[y, x]
            
            arr += bytes(hex(r),"utf-8")
            arr += bytes(hex(g),"utf-8")
            arr += bytes(hex(b),"utf-8")
                   
    MESSAGE = arr

    print("message: %s" % MESSAGE)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    
    ##----------------------
    
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")
