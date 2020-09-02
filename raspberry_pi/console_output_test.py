#!/usr/bin/env python3



from printrun.printcore import printcore
from printrun.utils import setup_logging
from printrun import gcoder

import sys
import traceback
import logging
from printrun.pronsole import pronsole
import getopt

import time

if __name__ == "__main__":

    from printrun.printcore import __version__ as printcore_version

    
    port='/dev/ttyACM1'
    baud=250000
    p = printcore(port, baud) #connect to the printer
    p.loud = False
    time.sleep(2)
    #gcode = [i.strip() for i in open(filename)]
    #gcode = gcoder.LightGCode(gcode)
    
    filename="getstatus.gcode"
    gcode = [i.strip() for i in open(filename)]
    gcode = gcoder.LightGCode(gcode)
    p.startprint(gcode)
    
