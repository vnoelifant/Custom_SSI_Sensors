# Notes:

You're gonna need one of these [SSI](https://github.com/hcmlab/ssi) or [mobileSSI](https://github.com/hcmlab/mobileSSI).

#### Required Libraries
	matplotlib
    	tkinter (for visualizations)
	pypozyx
	python-osc
	pyserial

#### To Run:

- Update the coordinates and ids of the anchors and tags in use
- Enter pozyx.pipeline into xmlpipe 
	- {path-xmlpipe}/xmlpipe pozyx.pipeline
- Profit!!

---

#### Common Errors/Fixes:

###### tkinter issue
- Follow instructions found here: [StackOverflow Link]( https://stackoverflow.com/questions/37710205/python-embeddable-zip-install-tkinter)
- install python 3.6.4 at same location (vc140)
- move tkinter stuff to root
- confirm tkinter by running help('modules') in the python console

###### Cannot Get Firmware Info for tag ID #...
- The tag you are trying to position is not listed in the script or has the wrong settings
 
###### SerialException: could not open port COM# or PozyxConnectionError: Wrong or busy serial port
- The pozyx dashboard is still running, close it

###### The numbers make no sense?
- Your coordinate system may be flawed
- Enter your measurements into the dashboard first, ensure its visualization works, then use the script

###### Watch check failed, now providing zeros
- Indicative of deeper issues, look for raised errors in the loading dialog