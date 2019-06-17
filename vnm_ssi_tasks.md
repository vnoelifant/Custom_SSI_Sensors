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
    * **Client code**:
      <?xml version="1.0" ?>
        <pipeline ssi-v="1">
          <register>
            <load name="ioput"/>
            <load name="audio" depend="ssidialog.dll"/>
            <load name="graphic"/>
            <load name="ffmpeg" depend="avcodec-57.dll;avutil-55.dll;postproc-54.dll;swresample-2.dll;swscale-4.dll;avdevice-57.dll;avfilter-6.dll;avformat-57.dll"/>
          </register>
          <framework sync="true" slisten="true" sport="1234"/>
          <sensor create="Audio" option="audio" sr="44100" blockInSamples="512">
            <output channel="audio" pin="audio_send"/>
          </sensor>
          <consumer create="FFMPEGWriter" path="audio" url="udp://127.0.0.1:7777" format="wav" stream="true">
            <input pin="audio_send" frame="0.04s" />
          </consumer>
        </pipeline>

    * **Server code**
      <?xml version="1.0" ?>
        <pipeline ssi-v="1">    
          <register>
            <load name="ssiaudio"/>
            <load name="ssiioput"/>
          </register>
            <framework sync="true" slisten="false" sport="1234" sdialog="true"/>
          <sensor create="Audio" sr="16000.0" option="audio">
            <output channel="audio" pin="audio"/>
          </sensor>    
          <consumer create="FileWriter" path="audio" type="0" overwrite="true">
            <input pin="audio" frame="512"/>
          </consumer>    
          <consumer create="SocketWriter" url="udp://127.0.0.1:7777" format="0">
            <input pin="audio" frame="512"/>
          </consumer>
        </pipeline>
       
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




















    