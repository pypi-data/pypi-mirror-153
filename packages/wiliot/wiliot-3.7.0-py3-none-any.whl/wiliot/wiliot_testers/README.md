# Release Note #

All testers 27.04.22 release note

---
## Overview 
* QR Scanner

    * New feature release - QR scanner
    * There is still connection to the printer with TCP for:
        * Initialization
        * Check printer status

    * Main GUI support 3 QR values
        * QR enabling - if we want it to be functional during run - Enable only when printing SGTIN (Production)
        * QR comport - For this stage, since attenuator has the same comport name, we will have to config the comport for QR scanner once - until we will make it automatic
        * QR offset - every setup has different length from GW to QR scanner, the offset refers to the tags between, tags under QR scanner and GW are not included.

* Calibration

    * New Calibration process and GUI was created
    * Will be integrated to all testers
    * Calibration was integrated into offline tester
    * Before calibrating need to place golden tag under GW
    
* Test Suite:

    * New test methodology for tags - performance test
    * Support for Single & Dual band tags, Extended Single Band and Battery tags
    * Tests comes from JSON file located at local configs path

 

    * Tests available:
        * Single Band
        * High power
        * 5 sec test

    * Dual Band
        * Patterns 18/52 - 2 tests
        * Each test 5 sec
        * High power

    * Single Band Extended
        * 2 Tests
        * Different power for each test, mid power and high power
        * High power time - 4 sec, Mid power time - 5 sec

    * Battery (still under development)
        * Energizing pattern 18
        * Test time 40 sec
        * Mid power
        * Will only pass tags with at least 3 secs between two different packets (different counter)

* GUI:

    * Main GUI was changed - relevant fields are visible while other are hidden in extended section
    * Fixed bug when pressing 'Stop' and then 'Cancel'

* Cloud:

    * Most of bugs for serialization were fixed
    * Double serialization for tags that split to 42 bits instead of 58
    * Added serialization in case of exception/critical warning
    * Serialization failed warning message were added

* SampleTest:
    * new GUI entries: test name, operator, antenna version, surface.
    * Option to edit the tags in the test before ending the test (and re-run the test for specific tags).
    * Cloud communication: keep run the test when there is no connection (until the end of the test), warn the user on bad connection.
    * New batch scripts to run from pip/git (under SampleTest dir).
    * COM ports: option to reconnect between test iterations.
    * Save all files (logs, configs) under wiliot/common/SampleTest. (edited) 