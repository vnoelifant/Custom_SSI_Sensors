# Tobii Eye Tracker SSI Pipelines

## Configuring SSI to stream Gaze Coordinates

1. Download the following files:
    * Tobii Eye Tracking .exe file from <https://github.com/tiilt-lab/Custom_SSI_Sensors/blob/master/TobiiEyeTracker/TobiiReceiver/TobiiReceiver/bin/Debug/TobiiReceiver.exe>
    * The pipeline and python sensor files from <https://github.com/tiilt-lab/Custom_SSI_Sensors/tree/master/TobiiEyeTracker>
2. Edit the path to the .exe file in gazesensor.<i></i>py
3. Download the Tobii Eye Tracking sdk and connect the eye tracker to your machine.
4. Confirm that the tracker is working well by turning on the gaze trace option.
5. Run the .pipeline file to test that everything works well. With the path variable set to an empty string you should see the output of the x_coordinate, y_coordinate and timestamp.

## Configuring SSI to Visualize Gaze Color Map

1. Follow steps 1-4 above if you have not setup the eye tracker.
2. Run the visual.pipeline file.

## Potential Issues and fix

1. Missing libraries: Python might throw errors due to missing packages. Most of these will be available via pip so just install them. 
2. Tkinter Issue: Follow the fix provided here <https://github.com/tiilt-lab/Custom_SSI_Sensors/tree/master/pozyx> on the Common Errors/Fixes section.
