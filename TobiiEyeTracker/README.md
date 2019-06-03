1. Download the following files:
	- Tobii Eye Tracking .exe file from https://github.com/tiilt-lab/Custom_SSI_Sensors/blob/master/TobiiEyeTracker/TobiiReceiver/TobiiReceiver/bin/Debug/TobiiReceiver.exe
	- The pipeline and python sensor files from https://github.com/tiilt-lab/Custom_SSI_Sensors/tree/master/TobiiEyeTracker
2. Edit the path to the .exe file in gazesensor.py
3. Download the Tobii Eye Tracking sdk and connect the eye tracker to your machine. 
4. Confirm that the tracker is working well by turning on the gaze trace option.
5. Run the .pipeline file to test that everything works well. With the path variable set to an empty string you should see the output of the x_coordinate, y_coordinate and timestamp.
