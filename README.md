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



