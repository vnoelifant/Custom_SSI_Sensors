## EECS 497: Advanced Multimodal Interfaces
## Veronica Medrano
## 6/17/19

This is my documentation for my accomplishments and next steps for class. 

## **Tasks in Order**:

  * ### **SSI Documentation, Installation and Configuration**
    * Successfully Installed SSI on Linux and on Windows Machine
    * Read through SSI documentation
      * Focused on Sensor and Client+Server documentation
      * Ran test scripts from SSI tutorial and pipes folder
  
  * ### **Streaming between 2 machines**:
    * Practiced with Tim in class
      * Could not get working, but practiced debugging, and saught help on Slack
    * Utilized the server and client script from Tim to practice on my own using Windows and Windows Virtualbox Machines
      * Was able to get working, but trouble writing to file. Summary of issues along with attached code was documented on Slack. Below is the Slack message: 
        * I was able to get streaming working from client on windows to server on windows guest in my Linux virtualbox. The audio file played, but only on the windows machine. Wondering what I'd need to change in the server script to play the wav file? I Tested other scenarios but with errors shown in the attached. I've placed the scripts I used here as well. I did run into that "watch check failure that @tim posted too. Seems like an issue with the server side in Linux mobileSSI. I haven't looked much into debugging it, but curious what is going on there. I wanted to explore using the wavwriter  vs file writer as @Marcelo Worsley mentioned. We can chat more tomorrow about it!
    * **See link below for code and other tests/error messages**:
        https://drive.google.com/open?id=16lapFkmV4GCXsoPIj2lVVDkHhEP5ICur

    * **IN WORK**: 
        * Try streaming again between Linux and new Windows machine and see if I can solve the file writing issues. 

  * ### **Sensors**:
    * **Major SSI Accomplishments**
        * Developed python code and pipeline scripts for the following sensors uploaded to Github.
          * Physiological sensor code found [here](https://github.com/tiilt-lab/Custom_SSI_Sensors/tree/master/heart_skin_brain) and includes the following sensors:
            * GSR
            * PPG
            * ECG
            * EEG
            * EEG with PPG
            * EEG with GSR
            * EEG with ECG
            * EEG with PPG, GSR
              * See video here!
                *  [![IMAGE ALT TEXT](http://img.youtube.com/vi/vY3h6-k4f7I/0.jpg)](http://www.youtube.com/watch?v=vY3h6-k4f7I "EEG,PPG,GSR Signals on SSI")
            * EEG with ECG, GSR
              * See video here!
                *  [![IMAGE ALT TEXT](http://img.youtube.com/vi/tBMmrahfTf8/0.jpg)](http://www.youtube.com/watch?v=tBMmrahfTf8 "EEG,ECG,GSR Signals on SSI")
            
            * EEG with PPG, ECG
          * Audio-Visual 
            * Code found [here](https://github.com/tiilt-lab/Custom_SSI_Sensors/tree/master/audio_visual)
            * See video here!
              *  [![IMAGE ALT TEXT](http://img.youtube.com/vi/RmkDWUocLfs/0.jpg)](http://www.youtube.com/watch?v=RmkDWUocLfs "Audio and Visual Sensors on SSI")
        * **NOTE**
          * Encountered many issues with parsing EEG data with Muse, Neurosky. Discussions held with Marcelo on this, and finally came to the solution in getting it to work after installing BlueMuse and Muse-LSL on newly purchased windows machine. 
  
  * ### **Next Steps**:
    * Experiment with transformers and Machine Learning Tasks in SSI
    * Utilize sensors I created to work on emotion recognition, maybe integrate smiles and facial landmarks. 




















    