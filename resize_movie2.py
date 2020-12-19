import moviepy.editor as mp
from PIL import Image
import socket
import cv2
import time
import random
import sys

movie = sys.argv

size = [6, 5]

clip = mp.VideoFileClip(movie[1])
clip_resized = clip.resize((size[0], size[1]))
clip_resized.write_videofile("movie_resized.mp4")

vidcap = cv2.VideoCapture('movie_resized.mp4')


UDP_IP = movie[2]
UDP_PORT = 4210
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)


while(True):

#    time.sleep(0.01)
    time.sleep(0.02)
    arr = b""
    
    pixCount = size[0] * size[1]
    
    success,image = vidcap.read()
    print('Read a new frame: ', success)
    if (not success):
        vidcap = cv2.VideoCapture('movie_resized.mp4')
        success,image = vidcap.read()
    
    for y in range(0, size[1]):

        for x in range(0, size[0]):
            b,g,r = image[y, x]
            
            arr += bytes(hex(r),"utf-8")
            arr += bytes(hex(g),"utf-8")
            arr += bytes(hex(b),"utf-8")
#            arr += bytes(hex(random.randint(0, 255)),"utf-8")
#            arr += bytes(hex(random.randint(0, 255)),"utf-8")
#            arr += bytes(hex(random.randint(0, 255)),"utf-8")

#    arr += bytes(hex(255),"utf-8")                    
    MESSAGE = arr

    print("message: %s" % MESSAGE)


    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))