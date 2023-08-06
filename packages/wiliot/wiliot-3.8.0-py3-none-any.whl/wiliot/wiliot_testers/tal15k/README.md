# tal15k_tester.py #

tal15k_tester is a multi-thread python script for testing Wiliot's tags on Muehlbaur's TAL15K machine 

---

## Installation

tal15k_tester requires Python 3.7 (or higher)


* Add System variables (for more details checkout how to add system variable):
    * Add environment variable:
      * name: TESTER_STATION_NAME
      * value: <tester station name (for logging)> (e.g. Company_name_Station_1), please use your company name in it
    * reset PC before continue
    

* Install Wiliot API:
````commandline
pip install pywiliot
````
* Install Tester Requirements:
````commandline
pip install -r requirements.txt
````
---
### Description

tal15k_tester runs four main threads (GW_API will open some more):
1. MainWindow Thread
    * Opens GUI of user inputs (run parameters)
    * Runs main GUI and controls all other threads
2. LoopThread - controls the testing flow, will send commands to charger/ tester threads
3. ChargerThread - controls the energizing gateway, will charge in the charging phase (start of new batch) and in between tags tests (when the tester is moving)
4. TesterThread - tests each tag and saves data to csv output file, is modular for using multiple testers at the same time




* PC that runs tal15k_tester connects to: 
    * Arduino via USB
    * 1+x Wiliot gateways via USB (1 charger & x testers)
    * Ethernet through LAN cable
* The Arduino connects to TAL15K controller via GPIO
    
Test Flow:

1.  GUI starts and wait for user inputs:
    
    ![settings.png](docs/tal15k_tester_settings_GUI.png)
   
   * wafer_name - tested wafer name 
   * rows_num - number of reels (how many tags in y axis) 
   * columns_num - number of tags tested in each batch in machine direction
   * num_of_testers - number of testers used (currently supports only 1)
   * packet_threshold - number of tag's packet after which the tag will pass
   * inlay_type - tags inlay type (number) 
   * charging_time - how long should the charging phase be, in seconds 
   * time_per_tag - how much time each tag gets before it will tester will send fail (if the packet_threshold was not achieved) 
   
   
2.  Run GUI opens
   
    ![tal15k_tester_run_GUI.png](docs/tal15k_tester_run_GUI.png)

    * this is only a temporary GUI and will be changed
   
3.  User can start the test through the TAL15K machine interface
4.  When starting the test, testers plate will move aside 
     * when done - TAL15K send "new batch" to PC
5.  Charger Gateway (GW) charges tags (using GW API) until PC ends charging time
    * when done - PC sends 'end of charge' to TAL15K
6.  TAL15K will move the tester under the first tag to test
7.  Tag transmitting packets to Tester GW 
8.  If tag didn't transmit at the time threshold (set by user),
    or didn't reach packet threshold (tag has failed):
    * Send "fail<X>" to TAL15K - <X> = tester number
    * TAL15K controller will move to next location 
9.  If tag did transmit before the time threshold (set by user) and
    reach packet threshold (tag has passed): 
    * Send "Pass<X>" to TAL15K  - <X> = tester number
    * TAL15K controller will move to next location
10. Tag data is appended to output csv 
11. TAL15K will move to next tag
    * if it was the last tag in this batch - go to step 4
    * else - TAL15K send "start test" to PC and goes to step 6

* The test will continue until all tags done testing unless:
    * An exception occurred (the run will pause)
    * User pressed "Pause"
    * User pressed "Stop"
    
12. When user presses "Stop" another GUI opens for uploading data to Wiliot cloud
![tal15k_tester_closing_GUI.png](docs/tal15k_tester_closing_GUI.PNG)

The user can choose whether to upload the data to cloud and also to add final comments on the run
14. A window will open to indicate this run final yield 

![tal15k_tester_good.png](docs/tal15k_tester_good.PNG)

![tal15k_tester_bad.png](docs/tal15k_tester_bad.PNG)

* yield = -1% means 0 tags were tested

---

### Output Files

tal15k tester generates 3 output files:
1. log - documents run parameters, results for each tag, exceptions, etc.


2. Tags data csv file
   
    Tags data contains data for all tags that transmitted (passed/failed).
    
    If a certain tag didn't transmit (at the time threshold), it won't be included in the file
   
    The data saved for each tag is:
    * Advertising Address - unique string which changes every brown-out (tag power cycle).
   
    * Tag location - tag location in the reel [batch, column, row]
   
    * Status - "Passed" or "Failed"
    * Common Run Name - Reel name (set by user) combined with timestamp from run start
    * Raw Data - all valid packets received from tag
        
        Raw Data contains encrypted packets that will be decrypted in Wiliot cloud.
    

3. Run data csv file
   Run data contains:
    * testerStationName
    * User inputs (set in GUIs)
    * Errors occurred during run 
    * Wafer name
    * GW parameters 
    * Amount of tested tags
    * Amount of passed tags
    * Run yield (updated at the end of the run)
    