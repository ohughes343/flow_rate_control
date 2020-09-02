#Prints a file. does nothing special. does not measure anything

import time
import sys

import io
import os
from time import sleep
import getopt
import sys

from printrun.printcore import printcore
from printrun.utils import setup_logging
from printrun import gcoder



port='/dev/ttyACM1'
baud=250000
p = printcore(port, baud) 
p.loud = False
time.sleep(2)

filename="camera_assembly_full.gcode"
gcode = [i.strip() for i in open(filename)]
gcode = gcoder.LightGCode(gcode)
p.startprint(gcode)

  

    



