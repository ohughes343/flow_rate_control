#from picamera import PiCamera
#from picamera.array import PiRGBArray

from printrun.printcore import printcore

#camera=PiCamera()
#camera.resolution=(640,480)
#camera.framerate=10
#rawCapture=PiRGBArray(camera,size=(640,480))

p=printcore('/dev/ttyACM0',250000)
p.send_now("M117 honing")