from printrun.eventhandler import PrinterEventHandler
import SampleHandler

import getopt
import sys
import getopt


from printrun.printcore import printcore
from printrun.utils import setup_logging
from printrun import gcoder

'''
Sample event handler for printcore.
'''

port='/dev/ttyACM0'
baud=250000
p = printcore(port, baud) #connect to the printer
p.loud = False

filename="petg_neck_test_noprobe.gcode"
gcode = [i.strip() for i in open(filename)]
gcode = gcoder.LightGCode(gcode)

p.send_now("M114")
on_recv(self,"M114")

interp = SampleHander()
interp.onrecv(self,line)





class SampleHandler(PrinterEventHandler):
    
    
    def __init__(self):
        pass

    def __write(self, field, text = ""):
        print("%-15s - %s" % (field, text))

    def on_init(self):
        self.__write("on_init")
        
    def on_send(self, command, gline):
        self.__write("on_send", command)
    
    def on_recv(self, line):
        self.__write("on_recv", line.strip())
    
    def on_connect(self):
        self.__write("on_connect")
        
    def on_disconnect(self):
        self.__write("on_disconnect")
    
    def on_error(self, error):
        self.__write("on_error", error)
        
    def on_online(self):
        self.__write("on_online")
        
    def on_temp(self, line):
        self.__write("on_temp", line)
    
    def on_start(self, resume):
        self.__write("on_start", "true" if resume else "false")
        
    def on_end(self):
        self.__write("on_end")
        
    def on_layerchange(self, layer):
        self.__write("on_layerchange", "%f" % (layer))

    def on_preprintsend(self, gline, index, mainqueue):
        self.__write("on_preprintsend", gline)
    
    def on_printsend(self, gline):
        self.__write("on_printsend", gline)
