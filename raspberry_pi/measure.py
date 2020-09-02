import numpy as np
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

import getopt
import sys
import getopt


from printrun.printcore import printcore
from printrun.utils import setup_logging
from printrun import gcoder

DELAY=106240 #E-step delay

#initialize camera
camera=PiCamera()
camera.resolution=(640,480)
camera.framerate=10
rawCapture=PiRGBArray(camera,size=(640,480))

time.sleep(1)

port='/dev/ttyACM1'
baud=250000
p = printcore(port, baud) #connect to the printer
p.loud = False
time.sleep(2)
filename="petg_neck_test_noprobe.gcode"
gcode = [i.strip() for i in open(filename)]
gcode = gcoder.LightGCode(gcode)
p.startprint(gcode)
time.sleep(1)
    
#array of previous values for data smoothing
expected_width=500
previous_width=[]
for k in range(0,10):
    previous_width.append(expected_width)


time.sleep(1)
### maybe main code here??? ###
for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    #time.sleep(1)
    
    
    image=frame.array
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    boundary=[(0,0,0),(255,255,255)]
    lower=boundary[0]
    upper=boundary[1]

    mask=cv2.inRange(hsv,lower,upper)
    result=cv2.bitwise_and(image,image,mask=mask)
    rows,cols,_ = result.shape
    
    array=[]
    
    #points defining the rectangle to be scanned
    pt1=(int((cols/5)),int(239*(rows/480)))
    pt2=(int(4*(cols/5)),int(241*(rows/480)))
    
    #give width array enough elements for all the rows
    for r in range(pt2[0]-pt1[0]):
        array.append(0)

    for i in range(pt1[1],pt2[1],1):
        #array.append(0)
        for j in range(pt1[0],pt2[0],1):
            #k = result[i,j]
            #if k.all()!=0: array[i]+=1
            if result[i,j][1] < 200: array[i]+=1
            #print(result[i,j][1])
            
    filament_width_px = int(100*round((sum(array) / len(array)),2))
    previous_width[9]=filament_width_px
    
    #shift values in array left and add newest value
    for k in range(0,len(previous_width)-1):
        previous_width[k] = previous_width[k+1]
    
    
    #get the average of the last 10 measurements
    width = sum(previous_width) / len(previous_width)
    
    print(width)
    p.send_now("M117 Width=%d"%(width))
    p.send_now("M221 S%d"%(width*2))
    
   
    
    cv2.imshow("frame", image)
    
    key = cv2.waitKey(1)
    rawCapture.truncate(0)
    if key==27:
        break
    
cv2.destroyAllWindows()
