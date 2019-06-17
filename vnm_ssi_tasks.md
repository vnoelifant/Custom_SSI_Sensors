# EECS 497: Advanced Multimodal Interfaces
# Veronica Medrano
# 6/17/19

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
                *  [![IMAGE ALT TEXT](http://img.youtube.com/vi/vY3h6-k4f7I
    /0.jpg)](http://www.youtube.com/watch?v=vY3h6-k4f7I "EEG,PPG,GSR Signals on SSI")
            * EEG with ECG, GSR
              * See video here!
                *  [![IMAGE ALT TEXT](http://img.youtube.com/vi/tBMmrahfTf8
    /0.jpg)](http://www.youtube.com/watch?v=tBMmrahfTf8 "EEG,ECG,GSR Signals on SSI")
            
            * EEG with PPG, ECG
          * Audio-Visual 
            * Code found [here](https://github.com/tiilt-lab/Custom_SSI_Sensors/tree/master/audio_visual)
            * See video here!
              *  [![IMAGE ALT TEXT](http://img.youtube.com/vi/RmkDWUocLfs
  /0.jpg)](http://www.youtube.com/watch?v=RmkDWUocLfs "Audio and Visual Sensors on SSI")
        * **NOTE**
          * Encountered many issues with parsing EEG data with Muse, Neurosky. Discussions held with Marcelo on this, and finally came to the solution in getting it to work after installing BlueMuse and Muse-LSL on newly purchased windows machine. 
  
  * ### **Next Steps**:
    * Experiment with transformers and Machine Learning Tasks in SSI
    * Utilize sensors I created to work on emotion recognition, maybe integrate smiles and facial landmarks. 




















    * #### What problems were encountered? 
      * None major, slight issues with configuring wifi

    * #### What are the challenges for the coming week?  
      * Updating the config file to use API key and URL vs username and pw,  learning NODE.js 

  * ### **Meeting Minutes**:
    * **Comments from Matthew**:
      * Git workflow suggestions
      * Suggestions on implementing the tone test. Simple action/respone test where LED can shine based on tone, as an example. 
    * **Comments from Team**:
      *  N/A

* ## **Week 1/28/19**
  * Work on Step 2 from the proposal (focus on tone detection)
    * User initiates negative tone 
    * Program robot to respond 
    * Plan out how to go beyond existing demos (ideas are in the proposal)
    * Execute tests

  * ### **Meeting Agenda**:
    * #### What was accomplished? 
      * Configured cloud connectivity 
      * Configured git clone on Raspberry Pi 
      * Updated configuration files ready for testing speech to text, tone analysis, text to speech, and Watson Assistant conversation. 
      * Tested another recipe that tests user asking TJBot to shine a disco light with success 
      * Tested Conversation but need to reconfigure speaker
      * Modified a script from a sentiment analysis recipe that allows TJBot to shine his light based on various moods (analyzed via speech to text). 
      The moods tested were sadness, joy, anger, and fear. 
        * See the videos below to see this tests in action! 
          
        [![IMAGE ALT TEXT](http://img.youtube.com/vi/CHtvny04RFA/0.jpg)](http://www.youtube.com/watch?v=CHtvny04RFA "TJBot LED Responds to Sadness")
         
        [![IMAGE ALT TEXT](http://img.youtube.com/vi/2qLOB8AL_NU/0.jpg)](http://www.youtube.com/watch?v=2qLOB8AL_NU "TJBot LED Responds to Joy")
        
        [![IMAGE ALT TEXT](http://img.youtube.com/vi/em58ocSdvI8/0.jpg)](http://www.youtube.com/watch?v=em58ocSdvI8 "TJBot LED Responds to Anger")
        
        [![IMAGE ALT TEXT](http://img.youtube.com/vi/eUPryh5006c/0.jpg)](http://www.youtube.com/watch?v=eUPryh5006c "TJBot LED Responds to Fear")
      * Researched github licensing to prepare for git push 
        
 
      * TODO: 
        * Week 2/4 goals
        * Refine test 2 for tone (think of ways for TJ to converse and respond)
        * Push to git ensuring the proper citations and license information is included
    

    * #### What problems were encountered? 
      * General research, finding examples 
      * Debugging 
        * Figuring out how to modify Javascript code. 
        * Speaker connected to 3.5 mm jack doesnt work well. It was suggested online to use bluetooth or usb to 3.5mm adaptor. 

    * #### What are the challenges for the coming week?  
      * Learning  more NODE.js /Javascript for adding more code functionality
      * Updating speaker configuration

  * ### **Meeting Minutes**:
    * **Comments from Matthew**:
      * Importance of continually pushing to Git.
    * **Comments from Team**:
      *  Does the tone analyze speech directly? As it only analyzes tone in the text, I thought this question gave me good insight on improvments for the future. 

* ## **Week 2/4/19**
  * Continue Step 2
  * Test, debug, refine

  * ### **Meeting Agenda**:
    * #### What was accomplished? 
      * Configured speaker via usb adaptor and successfully tested conversation with TJ
      * TODO: Step 2 from proposal (Negative tone test). Program in some of my personal favorite things (such as favorite songs, jokes, quotes,movie quotes), and incorporate that the Watson services (Speech to Text, Tone Analyzer, Text to Speech, Watson Assistant). 

* ## **Week 2/11/19**
  * Finish up Step 2 (**see above TODO for week 2/4/19, may need to adjust the dates**)
    * #### Accomplishments-2/18/19
      * Read through Watson Assistant Tutorial: [Creating Dialogue with Watson](https://console.bluemix.net/docs/services/conversation/dialog-overview.html#dialog-overview). Key components to create dialogue is outlined below:
        *  **Create skill**: a container for all of the artifacts that define a conversation flow.
        *  **Create intent**: define's user's goal or purpose, TJ detects this intent identified by a hashtag based on user-defined phrases (User examples in Watson Assistant)
        *  **Add entities**: Watson’s way of handling significant parts of input used to alter way it responds to intent
        *  **Create dialogue**: uses intents and entities plus context from app to interact with user and provide a response
            -  Add nodes in Watson Assistant
                +  Nodes contain triggers and responses
                    *  Triggers are conditions and if the user input matches a certain condition, the response from TJ is executed 
                    *  Trigger can be a context variable.  This is used if the context variable expression that you specify is true. Use the syntax, $variable_name:value or $variable_name == 'value'. This data exists in the .js code and passed to Assistant service. 
        * Can test dialogue in Watson Assistant's Try it Out panel
      
      * ### Outline of dialogue I plan to code this week:
        * #### **Intent**: #receive-support
          * #### **User examples**: "I feel so horrible, I am so sad, I had an awful day" 
          * #### **Example dialogue 1**: (simplest conversation to test first)
            *  **Parent Node 1**: 
              * If $emotion == 'sadness': // trigger is context variable from tj.analyzeTone(text) method in tjbot libary
                * Then: TJ can give any of these responses at random:
                  * "Oh no. It’ll all be better. Trust me. Read your favorite book, watch something silly, and tomorrow is another day!"
                  *  Mar Har! (silly phrase from Amanda Show)
                  * Despite knowing the journey and where it leads, I embrace it and welcome every moment. (Arrival movie quote)
          
          * #### **Example dialogue 2**: (more complex, but more ideal)
         
            * **Parent Node 1**: 
              * If $emotion == 'sadness': // trigger is context variable
                * Then: TJ asks, "why are you sad?" // response
                  * **Child Node 1**: 
                    * If @situation:break-up: // if reason is break-up 
                      *  Then: Tj responds: "I am so sorry, things will be better, I promise you!"
                  * **Child Node 2**: 
                    * If @situation:job-loss: // if reason is a job-loss
                      *  Then: Tj responds: "Oh no! I'm so sorry. I know you are a smart and capable of anything. It'll all work out in the end!"

      * Read through key node.js functions I'll be using 
      
      * **TODO**-2/18/19:
        * Test out dialogue outlined above
        * Integrate dialogue to added code incorporated all Watson services
        * Test code with Watson Assistant 
      
      * **2/19/19**
        * Created very basic first dialogue flow as shown below (Testing IN WORK):
        ![](screenshots/dialogue_test_1.png)
        * Began to add in the node.js code to interface with Watson services (IN WORK)
                        
  * Begin Step 3 from proposal 
    * User initiates positive tone
    * Program robot to respond

* ## **Week 2/18/19**
  * Contine Step 3
  * Test, debug, refine
  
  * ### **Meeting Agenda**:
    * #### What was accomplished? 
      * Code updates toincorporate dialogue with Watson services
      * Incorporated API methods from node-sdk, a Node.js client library to use the Watson APIs.

      * TODO: 
        * Debugging

    * #### What problems were encountered? 
      * Errors of not recognizing "intent.intent", errors not recognizing "text" input passed from Tone Analyzer to tone assistant. 

    * #### What are the challenges for the coming week?  
      * Figuring out what the cause of above issues are

  * ### **Meeting Minutes**:
    * **Comments from Matthew**:
      * 
    * **Comments from Team**:
      * 

* ## **Week 2/25/19**
  * Begin Step 4 from proposal
  * Robot detects quiet environment
  * Program robot to initiate dialogue
  * This is one of the big sretch goals, so if there are issues, or it is too timily to implement, go back and optimize existing functionalities (for instance, explore the facial recognition and Twitter API capabilities) 
  
  * * ### **Meeting Agenda**:
    * #### What was accomplished? 
      * Solved errors with connexting client app with Watson Assistant service
      * Successfully tested dialogue, see image snapshot and video below:
        ![](screenshots/tjbot_dialogue_test_1.png)

        [![IMAGE ALT TEXT](http://img.youtube.com/vi/D4Ysm5rI22U/0.jpg)](http://www.youtube.com/watch?v=D4Ysm5rI22U "TJBot Responds to Sadness and Happiness")

      * TODO: 
        * Improve dialogue flow. Right now the user expresses tone, and the robot responds, but doesn't expect an additional response from user. I will be sure to update this so that the user can say same more on the same topic and the robot will give additional responses based on that.  I'll also probably incorporate entities, so the robot can respond to specific instances or events the user is experiencing. I'll also want to add other features to enhance conversation (facial recognition, Twitter API, LED and arm wave)

    * #### What problems were encountered? 
      * Time to debug, but nothing really major
    * #### What are the challenges for the coming week?  
      * Time to incorporate best features

  * ### **Meeting Minutes**:
    * **Comments from Matthew**:
      *  something like an arm wave to indicate that youve been heard, test of what to say, help me understand what its not understanding, the interaction is key, if i say something what wil it do while waiting, if unsure, what it does?, how to create continuing dialogue. map out user experiences. David im feeling sad. Be complete interaction. Do you feel better? feedback from you so that it's helped. 
    * **Comments from Team**
      * Continuity. Why are you sad. 



* ## **Week 3/4/19**
  * Continue Step 4
  * Test, debug, refine
  * If not implementing Step 4, continue optimizing other functionalities
  
  * * ### **Meeting Agenda**:
    * #### What was accomplished? 
      * Added arm wave and LED light turn on as cues robot hears user's mood. See video for this test:
        
        [![IMAGE ALT TEXT](http://img.youtube.com/vi/Z0xkbjmOUhU/0.jpg)](http://www.youtube.com/watch?v=Z0xkbjmOUhU "TJBot Physical Cues")

      * Code updates to create continuing dialogue (IN WORK). See Watson Assistant images below and test (NOTE robot asks question but goes back to beginning of conversation in cycle. Code updates to fix this are in work.)


        ![](screenshots/tjbot_convo_jumps.png)

        ![](screenshots/tjbot_convo_jumps_2.png)

        [![IMAGE ALT TEXT](http://img.youtube.com/vi/vHk79rIxIoI/0.jpg)](http://www.youtube.com/watch?v=vHk79rIxIoI "Continuing Dialogue Test 1")

      * TODO: 
        * Continue code updates for continuing dialogue, test, add visual recognition and tweet detection to enhance interaction

    * #### What problems were encountered? 
      * Went past the limit for Speech to Text Service, problems with card authorization for upgrades (okay now, contacted IBM)
    
    * #### What are the challenges for the coming week?  
      * Time to incorporate best features

  * ### **Meeting Minutes**:
    * **Comments from Matthew**:
      *  
    * **Comments from Team**
      *  


* ## **Week 3/11/19**
  * Execute working tests
  * Begin final report and video
  * Work on finalizing Github repo
  
  * ### **Meeting Agenda**:
    * #### What was accomplished? 
      * Updated dialogue to show continuing dialogue with sadness tone. See dialogue snapshots and videos below. 
      
      * **Dialogue process summary**: 
        * User expresses a sad phrase, TJBot detect that it is said via context variable passed from the client application, $emotion=='sad'. To create this variable, the node.js code firs calls  Watson Tone Analyzer before sending the user input to the Assistant Service. Since every call in Node.js is asynchronous, we need to wrap the Tone Analyzer API call into a promise and resolve the promise using then() to call the Assistant API via .message method. See snapshots below: 

        ![](screenshots/tone_promise.png)
        
        ![](screenshots/tjbot_tone_context2_var.png)
        

        He asks the user if he would like to talk more about it, and the user can choose yes or no, via intents #yesadvice or #noadvice". If TJBot detects #yesadvice, he asks the user what is going on. Then the user states he is in a breakup via intent #breakup or job loss #jobloss, and TJBot responds accordingly. 
      
        Finally, after receiving TJBots advice, the node Show Appreciation shows user's appreciation via intent #appreciation. More will be added to this flow along with other tones, per meeting discussions. For intance, TJBot gets feedback from user about whether response helped, or if emotion level is not so high, perform different actions, and branch to different tones during conversation of first detected tone. 

        *Intents*
         ![](screenshots/tjbot_intents.png)

         *Intent User Examples (for training)*
         ![](screenshots/tjbot_intents_breakup.png)

         *Context Variable from tone detection*
         ![](screenshots/tjbot_tone_context_var.png)

         *Dialogue Flow-TJ to respond to Sadness*
         ![](screenshots/tjbot_dialogue_sadness_test1.png)
        
         *Dialogue Flow-TJ gives advice*
         ![](screenshots/tjbot_dialogue_sadness2_test1.png)
          
         *User shows appreciation for TJ advice*
         ![](screenshots/tjbot_dialogue_sadness3_test1.png)
         

      [![IMAGE ALT TEXT](http://img.youtube.com/vi/0zMfVJuMsSM/0.jpg)](http://www.youtube.com/watch?v=0zMfVJuMsSM "Sadness Dialogue-Test 1-Breakup")

      [![IMAGE ALT TEXT](http://img.youtube.com/vi/3qBcZ4wKbwc/0.jpg)](http://www.youtube.com/watch?v=3qBcZ4wKbwc "Sadness Dialogue-Test 2-Job Loss")

      [![IMAGE ALT TEXT](http://img.youtube.com/vi/7M7u0vWO89Y/0.jpg)](http://www.youtube.com/watch?v=7M7u0vWO89Y "Sadness Dialogue-Test 3-User Requests Not to Talk")

      * TODO: 
        * Enhance dialogue, incorporate other tones, final report
      
      * **UPDATE 3-18-19**
        * Dialogue updated that allows robot to get feedback from user in whether his response for sadness helped.  See extended dialogue tree and video below:
        *TJBot asks for feedback from sad user: Humor and relatability included*
         ![](screenshots/tjbot_dialogue_sadness_feedback.png)
       
        [![IMAGE ALT TEXT](http://img.youtube.com/vi/a0fzIPhx7YU/0.jpg)](http://www.youtube.com/watch?v=a0fzIPhx7YU "Sadness Dialogue-Test 4-TJBot asks for user feedback in sadness response")
        
      

* ## *Week 3/18/19**
  * Clean up any of the remaining final tasks (report/video/repo)
  * Prepare for demo

## License/Notes
 * This project is licensed under the Apache License, Version 2.0. Full license text is available here: [LICENSE](./LICENSE.txt). This project includes code modifications from IBM's TJBot recipe code [sentiment_analysis](https://github.com/ibmtjbot/tjbot/blob/master/recipes/sentiment_analysis/sentiment.js). The [NOTICE](./NOTICE.txt) file includes more information about the original work, and the original copyright notice and proper citations are included in the [source code](./tj_human_interact.js). 
