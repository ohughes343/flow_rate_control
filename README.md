# How To
Download my modded version of pronterface onto your Raspberry Pi:
```git clone https://github.com/ohughes343/flow_rate_control/raspberry_pi.git```



Add your gcode file to the folder
Edit the measure.py file to include your gcode file: (filename="my_file.gcode")
Connect your Pi to the printer
Run the script




# flow_rate_control


The aim of this project was to produce high-quality prints *regardless of the quality of the filament.* 
Commercially available filament has tight tolerances (Prusa3D claims +/-0.02mm), but experimental filament is often much worse. Inconsistent diameter or consistently off diameter filament results in poor prints with inaccurate dimensions. To remedy this, I measured the filament diameter during printing and adjusted the flow rate accordingly.

This project should be able to print with filament that varies by as much as 0.2mm from its baseline. Outside those dimensions, the printer will have trouble grabbing the filament and may not extrude at all.

**How it works:** A camera attached to the printhead measures the diameter of the filament ten times per second. If the diameter varies too much, a command is sent to the printer to adjust its flow rate. The command is sent after a short delay as it takes some time for that section of filament to reach the nozzle. 
The code is run on a raspberry pi computer and uses pronterface http://www.pronterface.com/index.html

**Materials:**
* Lulzbot TAZ 6 - This is the printer I based my design on, but the project could be modified for other printers
* Raspberry Pi - I wrote the code for a raspberry pi computer but with a few tweaks it can run on any computer. Just need a serial connection to the printer and a camera.
* Raspberry Pi HQ Camera
* 16mm lens - To zoom in on the filament
* Backlight - Important for accurate optical measurement. I strapped a flashlight on my printer but there is probably a more elegant solution.

**Variable Diameter Filament**\
Print quality is related to fill factor, which requires careful control of extrusion rate. When printing, a normal printer assumes constant diameter filament. If diameter is inconsistent, extrudate diameter is also inconsistent.

![Deformed Filament](https://github.com/ohughes343/flow_rate_control/blob/master/images/deformed.JPG)

Tolerances are good for commercially produced filament, as low as ±0.02mm.
For experimental filament, however, the tolerances are typically more like ±0.2mm. This can result in low quality parts that are significantly weaker.

The goal of this project was to print high quality parts using lab-generated filament with ±0.2mm tolerances.

**Objective and Approach**\
Objective: Develop a low-cost, universal hardware and software modification that allows desktop printers to compensate for filament diameter variations

**Producing Variable Diameter Filament**\
I hung a 50cm length of filament and heated it with a hair dryer to produce necked down sections. I was careful to make sure the diameter stayed above 1.55mm, as the printer would not extrudate anything smaller. 

![Hairdryer](https://github.com/ohughes343/flow_rate_control/blob/master/images/hairdryer.png)



**Optical Imaging Setup**\
I purchased a Raspberry Pi 3 computer, an accompanying HQ camera, and a 16mm lens. I also downloaded an [extruder part](https://download.lulzbot.com/TAZ/6.02/production_parts/printed_parts/extruder_latch/) from Lulzbot and modified it to hold the camera and filament in place.

![Extruder Conduit](https://github.com/ohughes343/flow_rate_control/blob/master/images/extruder_conduit.PNG)

![Final setup on printhead](https://github.com/ohughes343/flow_rate_control/blob/master/images/final_setup.PNG)



**Optical Imaging Software**\
Images were captured and analyzed 10 times per second. Since the filament was moving at 1mm/s relative to the camera, 1mm of filament has 10 data points. I implemented a moving average to reduce noise - every data point is an average of itself and the previous 9 points.

![Before and after smoothing](https://github.com/ohughes343/flow_rate_control/blob/master/images/smoothing_graphs.png)

**Adaptive Algorithm**\
![Deformed Filament](https://github.com/ohughes343/flow_rate_control/blob/master/images/equations.png)

![Deformed Filament](https://github.com/ohughes343/flow_rate_control/blob/master/images/equation_graph.png)

**Pixel Size Calibration**\
I took images of filament and a microscope calibration slide at the same distance from the camera to calibrate my software. A 1.79mm diameter chunk of filament took up 508px, which is roughly 0.003mm/px. This is about the best resolution I could get while sampling 10x per second at 640x480. I was able to get 0.001mm/px resolution at lower sampling rates.

![Alt text](https://github.com/ohughes343/flow_rate_control/blob/master/images/filament_hd.JPG)

**Results: Optical Diameter Measurement**\
Measuring *the same* chunk of filament 3 times resulted in the plot on the left, demonstrating that my system is highly precise and repeatable. Some of the smoothing may be due to my software averaging, but it is clearly responding to real physical changes.
The plot on the right demonstrates the same idea with filament that was stretched out to produce very narrow sections.

In both cases, a digital micrometer confirmed the accuracy of the camera. 
![Variable Filament](https://github.com/ohughes343/flow_rate_control/blob/master/images/variable_diameter.png)

**Results: Adaptive Control**\
I implemented a delay in the system to account for the time it takes for the filament to travel from the camera to the nozzle. 
And this is where I got stuck. I first tried to use a time delay, but this wouldn't work for different speeds or if the motor ever retracted filament. A fixed step delay, which I tried next, is also complicated by retraction. So as of right now, the project *works*, but only if the motor never reverses.
![Variable Filament](https://github.com/ohughes343/flow_rate_control/blob/master/images/delay.png)

**My system vs a Keyence Laser**\
One chunk of **lab-produced** filament was measured 3 times with a Keyence digital micrometer. I measured the same chunk 3 times with my optical system to compare the results.
![Experimental](https://github.com/ohughes343/flow_rate_control/blob/master/images/experimental_vs_laser.png)

I made the same comparison with commercial filament.
![As-received](https://github.com/ohughes343/flow_rate_control/blob/master/images/as_received_vs_laser.png)

**Demonstration Part**\
I printed a thin airfoil part to demonstrate my adaptive control.
![Demo part](https://github.com/ohughes343/flow_rate_control/blob/master/images/demo_part.png) 

**Future Work**
* Universal Mount for other 3D printers
* Use with filament colors other than red


![FFF printer](https://github.com/ohughes343/flow_rate_control/blob/master/images/fff.png)



![Lulzbot TAZ 6](https://github.com/ohughes343/flow_rate_control/blob/master/images/taz.png)
