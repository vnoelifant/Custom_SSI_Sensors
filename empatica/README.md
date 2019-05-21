## To Run:
1. Open the E4 streaming server
2. Pick an empatica
3. Make sure the empatica usb dongle is attached
4. If it says discovering just hold down the little black button on top left and that should connect, otherwise click start discovery
5. Once it appears in the streaming server click connect
6. Depending on the device that you have use the DeviceID table at the top of empatica_processing.py to swap out the id in line 30 deviceIDs
7. Then to run it, open the command line and enter ```empatica_multiprocessing.pipeline > test_gym.txt```
8. Pipe the command output to a file to catch errors etc for the next run
