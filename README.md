# flow_rate_control

If I published a paper it would be called something like *"Autonomous in-situ flow rate control of fused deposition modeling printers"*

Basically, the aim of this project is to produce high-quality prints regardless of the quality of the filament. 
Commercially available filament has tight tolerances (Prusa3D claims +/-0.02mm), but experimental filament is often much worse. Inconsistent diameter or consistently off diameter filament results in poor prints with inaccurate dimensions. There are even designs online to test for over/under extrusion: https://www.thingiverse.com/thing:1622868

This project should be able to print with filament that varies by as much as 0.2mm from its baseline. Outside those dimensions, the printer will have trouble grabbing the filament and may not extrude at all.

**How it works:** A camera attached to the printhead measures the diameter of the filament ten times per second. If the diameter varies too much, a command is sent to the printer to adjust its flow rate accordingly. The command is sent after a short delay, as it takes some time for that section of filament to reach the nozzle. 
The code is run on a raspberry pi computer and uses pronterface http://www.pronterface.com/index.html

**Materials:**
* Lulzbot TAZ 6 - This is just the printer I based my design on but the project could be modified for other printers
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
Objective: Develop a low-cost, universal hardware and software modification that allows low-cost desktop printers to compensate for filament diameter variations

**Producing Variable Diameter Filament**\
I hung a 50cm length of filament and heated it with a hair dryer to produce necked down sections. I was careful to make sure the diameter stayed above 1.55mm, as the printer would not extrudate anything smaller. 


**Optical Imaging Setup**\
I purchased a Raspberry Pi 3 computer, an accompanying HQ camera, and a 16mm lens. I also download this extruder part from Lulzbot and modified it to hold the camera and filament in place.


**Optical Imaging Software**\

**Adaptive Algorithm**\

**Pixel Size Calibration**\
I took images of filament and a microscope calibration slide at the same distance from the camera to calibrate my software. A 1.79mm diameter chunk of filament took up 508px, which is roughly 0.003mm/px. This is about the best resolution I could get while sampling 10x per second at 640x480. I was able to get 0.001mm/px resolution at lower sampling rates.

**Results: Optical Diameter Measurement**\
![Variable Filament](https://github.com/ohughes343/flow_rate_control/blob/master/images/variable_diameter.png)

**My system vs a Keyence Laser**\
One chunk of **lab-produced** filament was measured 3 times with a Keyence digital micrometer. I measured the same chunk 3 times with my optical system to compare the results.

**Demonstration Part**\
I printed a thin airfoil part to demonstrate my adaptive control. 

**Future Work**\
* Universal Mount for other 3D printers
* Use with filament colors other than red


![FFF printer](https://github.com/ohughes343/flow_rate_control/blob/master/images/fff.png)

![Alt text](https://github.com/ohughes343/flow_rate_control/blob/master/images/filament_hd.JPG)

![Lulzbot TAZ 6](https://github.com/ohughes343/flow_rate_control/blob/master/images/taz.png)
