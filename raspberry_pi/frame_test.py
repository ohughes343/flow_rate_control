### simple script to show camera frame preview

import sys
import numpy as np
import argparse
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

#initialize camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size = (640,480))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image=frame.array
    
    cv2.imshow("frame", image)
    
    key = cv2.waitKey(1)
    rawCapture.truncate(0)
    if key==27:
        break
    
    

cv2.destroyAllWindows()