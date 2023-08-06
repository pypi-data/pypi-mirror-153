# offline_tester.py #

offline_tester is a multi-thread python script for testing Wiliot's tags

---
## Overview 
This script is the operational code that controls Tadbik's R2R machine.
It is also a reference design for any offline tester which tests Wiliot's tags.
However, this code needs some adaptations in order for it to work with other machines.
For example, please see the offline_tester_example_code which will be simpler to understand and does not 
contain the code needed in order to control Tadbik's R2R machine.

Tadbik's R2R machine include PLC and touch screen for various system commands and configurations (speed change, continuous/step movement etc.).
So this machine alone can roll reel of tags from one side to the other. 
This PLC is also controlling a color identification sensor which help with the step movement accuracy (move a new tag to a testing position above the coupler). 
The PLC is also control the printer by itself.

Wiliot's tester PC communicates with that PLC via Arduino (we don’t control the printer and the sensor but the PLC does). 
The offline_tester.py code relies on the following architecture:

![img_6.png](docs/r2r_communication_diagram.jpg)

*PLC="R2R offline tester controller"

This is the flow in the diagram in words:
At the end of each test, the PC send “pass/fail” signal to the PLC which moves the reel to the next tag and print the desired result on the tested tag.
When a new tag is in place, the PLC sends out a pulse to the GW.
Upon receiving the pulse, the GW is doing some internal configuration (erasing buffer’s older packets, starts a charging phase).
When the GW completes the configurations it sends “start production line…” message to the PC -> PC starts the “new_tag” function (starts a new tag test).
and so on…

Here is an example of the GPIO function over time:

![img_5.png](docs/example_of_timing_diagram.jpg)

The pass/fail commands from the PC tells the PLC to move forward by 1 location and printing pass/fail on the previous tag.
start/stop only tells the PLC to enable/disable the movement.
   

---

## Installation

offline_tester requires Python 3.7 (or higher)


* Add System variables (for more details checkout how to add system variable):
    * Add environment variable:
      * name: tester_station_name
      * value (for logging): <'company name'> + '_' + <'tester station name'> (e.g. Wiliot_Station1)
    * reset system before continue
    

* Install Wiliot API:
````commandline
pip install wiliot
````
---
### Description

offline_tester runs four threads:
1. MainWindow Thread
    * Opens GUI of user inputs (run parameters)
    * Runs main GUI and controls all other threads
2. R2RThread - controls the R2R machine and sends pass/fail to printer
3. TagThread - controls the gateway, tests each tag and saves data to csv output file
4. Printer - asks the printer on printed value and confirm it was desired value
    * Printer thread will open only if user sets "To print?" as "Yes"



* PC that runs offline_tester connects to: 
    * Arduino via USB
    * Wiliot gateway via USB
    * VideoJet printer via Ethernet using 'Zipher' protocol      
        PC checks after each print that the printing value is valid
* The Arduino connects to R2R offline tester controller via GPIO
* The offline tester controller connects to:
  * Wiliot gateway via GPIO
  * VideoJet printer model Videojet 8520 (datasheet in link below)
    
    https://global.videojet.com/wp-content/uploads/dam/pdf/NA%20-%20English/Specification-Sheet/ss-8520-us.pdf
    
    The communication to printer is via RS232 connection 
    
Test Flow:

1. * GUI starts and wait for user inputs:
    
    ![img_1.png](docs/offline_tester_start_gui.png)
   
   * If its printing run ("To print?" set as "Yes"), a second GUI opens for printing parameters:
    
    ![img_2.png](docs/offline_tester_print_sgtin_gui.png)
   
2. Run GUI opens
   
    ![img_3.png](docs/offline_tester_run_gui.png)
   
3. R2R moves (first position will always be considered as "Fail")
4. Gateway (GW) charges tag (using GW API)
5. Tag transmitting packets to GW
6. If tag didn't transmit at the time threshold (set by user),
   
    or didn't reach packet threshold (tag has failed):
    * Send "Fail" to R2R thread
    * R2R controller will send "Fail" to printer
    * Printer will print "Fail" mark on tag
   If tag has passed:
    * Send "Pass" to R2R thread
    * R2R controller will send "Pass" to printer
    * Printer will print "Pass" mark on tag according to format (e.g., QR code)
7. Tag data is appended to output csv 
8. R2R will move to next tag
9. Repeat steps 4 to 8
* The test will continue until all tags done testing unless:
    * An exception occurred (the run will pause)
      * In cases of exception that don't require ending the run,
        
        if the user chooses to press "Continue" the current tag location will be marked as "Fail"
    * User pressed "Pause"
    * User pressed "Stop"
    * Desired amount of tested tags reached (set by user in GUI)
    
10. When user presses "Stop" another GUI opens for uploading data to Wiliot cloud
    
    ![img_4.png](docs/upload_to_cloud_gui.PNG)
    
    The user can choose whether to upload the data to cloud and also, to add final comments on the run 

---

### Output Files

offline tester generates 3 output files:
1. log - documents run parameters, results for each tag, exceptions, etc.


2. Tags data csv file
   
    Tags data contains data for all tags that transmitted (passed/failed).
    
    If a certain tag didn't transmit (at the time threshold), it won't be included in the file
   
    The data saved for each tag is:
    * Advertising Address - unique string which changes every brown-out (tag power cycle).
   
    * Tag location - tag location in the reel.
   
    * External ID - If its printing run, the string printed on the tag.
      
      Else, only tag counter number (corresponding to tag location).  
    * Status - "Passed" or "Failed"
    * Common Run Name - Reel name (set by user) combined with timestamp from run start
    * Temperature From Sensor - temperature read from sensor at testing point 
    * Raw Data - all valid packets received from tag
        
        Raw Data contains encrypted packets that will be decrypted in Wiliot cloud.
    

3. Run data csv file
   Run data contains:
    * User inputs (set in GUIs)
    * Errors occurred during run 
    * Reel name
    * GW parameters 
    * Amount of tested tags
    * Amount of passed tags
    * Run yield (updated at the end of the run)
    
The user can choose to save more parameters to output csv files (run_data or tags_data).

For adding more parameters to output files, the user should add the param header when calling class CsvLog (example below):


````python
# csv file is generated with default headers only
run_data_log = CsvLog(header_type=HeaderType.RUN, path=run_data_path,
                      tester_type=TesterName.OFFLINE)

user_headers = ['header_1', 'header_2']
# csv file is generated with default and additional headers
run_data_log = CsvLog(header_type=HeaderType.RUN, path=run_data_path,
                      headers=user_headers, tester_type=TesterName.OFFLINE)

````