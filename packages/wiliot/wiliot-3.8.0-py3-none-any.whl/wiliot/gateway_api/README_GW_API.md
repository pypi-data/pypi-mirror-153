
# PyWiliot #

* [Installation](#Installation)
* [API Structure](#API Structure)
* [Methods](#Methods)

## Installation
run the following command:
````commandline
pip install wiliot
````

for more installation details please see [PyWiliot readme](../../README.md)

### to import the API:

````python
from wiliot.gateway_api.gateway import *
````

## API Structure
![API Highlight](../docs/images/GW_APIhighlight.PNG)

## Methods
````python
WiliotGateway(baud=921600, port=None, auto_connect=False, lock_print=None, logger_name=None, verbose=True)
````
| Input | Description|
| --------|------|
| baud | the GW baud rate |
| port | The GW port if it is already known |
auto_connect | If TRUE, connect automatically to the GW. |
| lock_print | if specified, used as the lock thread for printing messages |
| logging_name | if specified, used go get the logger by name to log all printed message (using ‘logging’ python function) |
| verbose | if FALSE, only warnings will be printing on the console without information debugging

**Output** - None

**Description:**
* the baud rate is set to baud value and saved
* If the port is specified, the GW will connect to this port and baud automatically.
* When auto_connect is TRUE, the function open_port runs on every available port until a connection is established


````python
open_port(port,baud)
````
| Input | Description|
| --------|------|
| port | The GW port |
| baud | the GW baud rate |

**Output** - return TRUE if GW connection was established and FALSE otherwise

**Description:**
* Connect to the port with the specified baud rate.
* If the port is open, The GW version is read.
* If the version name is valid, the GW type (BLE/WIFI/LTI) is saved along with the software version.
* The serial port is closed if the version name is invalid


````python
write(cmd)
````
| Input | Description|
| --------|------|
| cmd | the command to write not including "\r\n" |

**Output** - None

**Description:**
* Check if `cmd` is bytes or a string and if it contains new-line characters.
* If `cmd` is valid, the function tries to write the command to the GW serial port


````python
read_specific_message(msg, read_timeout=1)
````
| Input | Description|
| --------|------|
| msg | the message or part of the message that needed to be read |
| read_timeout | the maximum time to wait until the specific message has arrived |

**Output** - the specific message or empty string if time exceeded read timeout

**Description:**
* read incoming message until it matches the desired message based on `msg`.
* If it finds the specific message it returns the message.


````python
close_port(is_reset=False)
````
| Input | Description|
| --------|------|
| is_reset | If TRUE, running the Reset function before closing the port |

**Output** - None

**Description:**
* Closing GW serial port


````python
reset_gw(reset_gw=True, reset_port=True)
````
| Input | Description|
| --------|------|
|reset_gw | reset GW| 
| reset_port | reset serial port |

**Output** - None

**Description:**
* Reset the GW serial port
* Flush and reset input buffer


````python
reset_buffer()
````

**Input** - None

**Output** - 

**Description:**
* Reset input buffer of the GW serial COM
* Reset raw and processed data queue


````python
stop_all_processes(packet_listener_process=True, packet_analysis_process=True)
````
| Input | Description|
| --------|------|
|packet_listener_process | stop packet listener thread |
| packet_analysis_process | stop process packet thread |

**Output** - None

**Description:**
* stop threads of data acquisition and analysis 


````python
config_gw(filter_val=None, pacer_val=None, energy_pattern_val=None, time_profile_val=None, beacons_backoff_val=None, 
          received_channel=None, modulation_val=None,max_wait=1,  check_validity=False, check_current_config_only=False,
          start_gw_app=True)
````
| Input | Description|
| --------|------|
| filter_val | set packet filter. |
| pacer_val | Set pacer interval. |
| energy_pattern_val | set Energizing Pattern. |
| time_profile_val | set Timing Profile where the first element is the ON value and the 2nd element is the period value.|
| beacons_backoff_val | Set beacons backoff. |
| received_channel | the RX channel (37,38,39) |
| modulation_val | set modulation (for most cases supposed to be True=on) |
| max_wait | wait time in milliseconds after each GW config command to prevent buffer overflow | 
| check_validity | if True, a validity check is done on the configuration parameters|
| check_current_config_only | if True only print the current GW configuration without changing it |
| start_gw_app | if True the gw starts to transmit and receive messages immediately after configuration is completed |

*for more details on each parameter, please contact Wiliot*

**Output** - a dictionary of all the configuration parameters that were set

**Description:**
* If`check_validity` is True and one or more of the parameters failed the validation test, no configuration is set.
* Configure all input parameters that are not None.

*Note: Current settings of the time profile and received channel are sent together, therefore if either of them is set, 
they should be both set*


````python
check_current_config()
````
**Output** - None 

**Output** - None

**Description:**
* send a request to the GW to print its current configuration



````python
run_packets_listener(max_packets=None, max_time=None, tag_packets_only=False, do_process=False)
````
| Input | Description|
| --------|------|
| max_packages | The maximum packets to read. If None, read infinite number of packets. The default value is None |
| max_time | The maximum time to read in seconds. If None, read for infinite time. The default value is None |
| tag_packages_only | If True, save only the tag packets without the GW responses. The default value is None |
| do_process | If True, automatically run the `run_process_packet` |

**Output** - if running in blocking mode (max_packages and/or max_time are specified), returns the acquired data

**Description:**
* Run the `com_port_listener` function
* If both `max_packages` and `max_time` are None, then a non-blocking method is applied by defining a thread.
* If `max_packages` and/or `max_time` are specified, then com_port_listener function runs as a blocking function until it finishes. When finished it runs automatically get_data and returns the acquired data

**`com_port_listener` description:**
* An infinite loop with the following stop-conditions:
  - If the GW is not open
  - If the running time of the function has exceeded the `max_time`.
  - If the number of received packets has exceeded the `max_packets`.
  - If process was stop by the user (by calling `stop_processes()`)
* When no valid message has been received for more than five seconds, the input buffer gets reset

````python
run_process_packet(raw_data=None, process_only_current=False)
````
| Input | Description|
| --------|------|
|raw_data | the output of `get_data` . A list of dictionary with ‘raw’ which contains the raw tag packets and ‘time’ which contains the timestamp of each packet. if list contains only one element raw_data can be a dictionary| 
| process_only_current | if True, only the last element is processed (the last packet and its timestamp)|

**Output** - None

**Description:**
* Run the `process_packet` function
* If `raw_data` None, then a non-blocking method is applied by defining a thread.
* If not, then `process_packet` function runs as a blocking function until it finishes

**`process_packet` description:**

* An infinite loop with the following stop-conditions:
  - If process was stop by the user (by calling stop_processes)
* the function outputs the following parameters:
  - `packet`: the packet content without the additional strings.
  - `is_valid_tag_packet`: True if the packet is considered as tag’s packet
  - `adv_address`: the advertising address (unique number of each tag, before brown out).
  - `group_id`: the group id of each tag. relevant for the decryption key.
  - `rssi`: Received signal strength indication - the lower the number the stronger the signal.
  - `n_packet_filter`: number of filtered packets. GW filters identical packets for better performance.
  - `time_from_start`: the timestamp of each packet with respect to the start running time.
  - `counter_tag`: the number of occurrences of the same advertising address



````python
get_data(action_type=ActionType.FIRST_SAMPLES, num_of_packages=1,data_type=DataType.RAW)
````
| Input | Description|
| --------|------|
| action_type | The packets read method. class of enum: 'all_samples', 'first_samples', 'current_samples'. |
| num_of_packages | The number of packets to extract |
| data_type | The data type to extract.  class of enum: ‘raw’ or ‘processed’ |

**Output** - a list of dictionary with all the extracted packets. see `run_process_packet` for more details

**Description:**
* Extract packets according to the following methods:
  - all_samples: return all available packets.
  - first_samples: return the X first packets (the oldest packets ) according to num_of_packages
  - current_samples: return the X last packets (the newest packets ) according to num_of_packages
*If more packets are requested than are available, no data is returned.

````python
update_version(version="Latest", versions_path="", check_only=False)
````
| Input | Description|
| --------|------|
| version | the version string in the following format 'x.x.x'. If version is 'Latest' than the latest version is selected |
| versions_path | the full path of the desired version file. if specified, the GW will be updated by using this specific version |
| check_only | if True, the function only checks the version without updating it|

**Output** - True if GW version is up to date, False if GW version is old and None if a problem occur

**Description:**
* First, compare the GW version with the required version. 
* If the versions are different, it checks if the required version has a matched zip file under the gateway_versions versions folder. 
* If the file exists, a version update is done by send the GW to bootloader mode and burn the version using nRF utils (Nordic package)

````python
get_latest_version_number(version="Latest", versions_path="")
````
| Input | Description|
| --------|------|
| version | the version string in the following format 'x.x.x'. If version is 'Latest' than the latest version is selected |
| versions_path | if needed, the folder path of all versions files. by default, the function access the API geteway version folder|

**Output** - The latest available version number to be installed and its path

**Description:**
* if specified and valid check the versions files under versions_path and return the latest version (unless specified) number and its path.
* if versions_path is not specified uses the default gw_versions folder as part of Wiliot package


````python
exit_gw_api()
````
**Input** - None

**Output** - None

**Description:**
* check the serial port is closed and all threads are stopped. If not, close port and threads.

````python
get_connection_status()
````
**Input** - None

**Output** - output - 

**Description:**
* if gateway is connected, return True, the serial port and baud rate used for the connection. 
  if not, return False, and None for port and baud


````python
get_gw_version()
````
**Input** - None

**Output** - the gateway software version, and the gateway hardware type

````python
is_data_available()
````
**Input** - None

**Output** - if data is available to read

**Description:**
* returns True if data is available to read from `get_data`