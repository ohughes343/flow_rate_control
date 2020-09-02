#extrudes cold filament while recording both diameter and M221 command
#IMPORTANT: remove printer nozzle before running this test


import numpy as np
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import sys
import numpy as np
import argparse
import io
import os
from time import sleep
import getopt
import sys
import getopt
import threading


from printrun.printcore import printcore
from printrun.utils import setup_logging
from printrun import gcoder

DELAY=106240 #E-step delay
BASE_DIAMETER = 1.75 #baseline diameter of filament in mm (usually 1.75 or 2.85)
PIXELS_PER_MM = 294.74

#remove files if they exist
if os.path.exists('filament_diameter.txt'):
    os.remove('filament_diameter.txt')
if os.path.exists('command.txt'):
    os.remove('command.txt')


#files to write to
f=open('filament_diameter.txt','w')
o=open('command.txt','w')


#initialize camera
camera=PiCamera()
camera.resolution=(640,480)
camera.framerate=10
rawCapture=PiRGBArray(camera,size=(640,480))

#connect to printer
port='/dev/ttyACM1'
baud=250000
p = printcore(port, baud) 
p.loud = False
time.sleep(2)

#turn on cold extrusion
p.send_now("M302 S0")


    
#array of previous values for data smoothing
expected_width=504
previous_width=[]
for k in range(0,10):
    previous_width.append(expected_width)
    
#array of commands to delay flow rate change
default_command=100
command_array=[]
for c in range(0,1280):
    command_array.append(default_command)



def change_flow_rate(command):
    #p.send_now("M221 S%d"%(command)) #then send command to adjust flow rate
    with open('command.txt','a') as f: #and update file
        print(str(command), file=f)
    

    
### Main loop ###
for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    
    image=frame.array
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    boundary=[(0,0,0),(255,255,255)]
    lower=boundary[0]
    upper=boundary[1]

    mask=cv2.inRange(hsv,lower,upper)
    result=cv2.bitwise_and(image,image,mask=mask)
    rows,cols,_ = result.shape
    
    array=[]
    num=0
    
    #points defining the rectangle to be scanned
    pt1=(int((cols/5)),int(240*(rows/480)))
    pt2=(int(4*(cols/5)),int(241*(rows/480)))
    
    

    for i in range(pt1[1],pt2[1],1):
        for j in range(0,cols,1):
            if result[i,j][1] < 200: num+=1
            
    
    print("num: " + str(num))
    #filament_width_px = int(100*round((sum(array) / len(array)),2))
    
    previous_width[9]=num
    
    #shift values in array left and add newest value
    for k in range(0,len(previous_width)-1):
        previous_width[k] = previous_width[k+1]
    
    
    
    
    #get the average of the last 10 measurements
    width_px = sum(previous_width) / len(previous_width)
        
    #width_px = round(num,2)
    width_mm = round(width_px / PIXELS_PER_MM,4)
    
    #M221 command to send
    try:
        command = int(100*((BASE_DIAMETER ** 2) / (width_mm ** 2)))
    except ZeroDivisionError:
        command = 0
    
    command_array[-1] = command
    for d in range(0,len(command_array)-1):
        command_array[d] = command_array[d+1]
   
    change_flow_rate(command_array[0])
        
        
    
    #output diameter to file
    with open('filament_diameter.txt','a') as f:
        print(str(width_mm), file=f)
    
    
    
    print("Width(px): " + str(width_px))
    print("Width(mm): " + str(round(width_mm,4)))
    print("Command: " + str(command_array[0]))
    #p.send_now("M117 Width=%d"%(width))
    #p.send_now("M221 S%d"%(width))
    
   
    
    cv2.imshow("frame", image)
    
    key = cv2.waitKey(1)
    rawCapture.truncate(0)
    if key==27:
        break
    
    
    
cv2.destroyAllWindows()

