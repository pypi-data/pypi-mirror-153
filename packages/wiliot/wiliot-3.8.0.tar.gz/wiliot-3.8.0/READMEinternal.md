# PyWiliot #

PyWiliot is a python library for accessing Wiliot's tools including:
* Wiliot's cloud services from Python
* Wiliot's Gateway control
* Wiliot's tester utilities
In addition, examples and scripts for Wiliot testers are provided

## Public Library

### MAc Installation
#### Getting around SSL issue on Mac with Python 3.7 and later versions

Python version 3.7 on Mac OS has stopped using the OS's version of SSL and started using Python's implementation instead. As a result, the CA
certificates included in the OS are no longer usable. To avoid getting SSL related errors from the code when running under this setup you need
to execute Install Certificates.command Python script. Typically you will find it under
~~~~
/Applications/Python\ 3.7/Install\ Certificates.command
~~~~

#### Python 3 on Mac
The default Python version on mac is 2.x. Since Wiliot package requires Python 3.x you should download Python3 
(e.g.  Python3.7) and make python 3 your default.
There are many ways how to do it such as add python3 to your PATH (one possible solution https://www.educative.io/edpresso/how-to-add-python-to-the-path-variable-in-mac) 

#### Git is not working after Mac update
please check the following solution:
https://stackoverflow.com/questions/52522565/git-is-not-working-after-macos-update-xcrun-error-invalid-active-developer-pa

### Installing pyWiliot
````commandline
pip install wiliot
````

### Using pyWiliot
please check out the [examples](wiliot/examples) folder with [cloud services](wiliot/cloud_apis/management/examples) and [gateway](wiliot/gateway_api/examples) code examples.

For more documentation, please read the manuals under the [management_api](wiliot/cloud_apis/management/README_MNGMT_API.md) folder and [gateway_api](wiliot/gateway_api/README_GW_API.md) folder

## Private Library

### Installing pyWiliot - Using SSH (For Internal Use only)
generate ssh key and load the public key to [bitbucket.com](https://bitbucket.org/account/settings/ssh-keys/) for your computer
(for more details please see [Set SSH - Bitbucket Support](https://support.atlassian.com/bitbucket-cloud/docs/set-up-an-ssh-key/))

then, run the following command:
````commandline
pip install git+ssh://git@bitbucket.org/wiliot/pywiliot_internal.git
````

### Installing pyWiliot - Using Bitbucket user (For Internal Use only)
run the following command:
````commandline
pip install -e git+https://<your bitbucket ID>@bitbucket.org/wiliot/pywiliot_internal.git#egg=pywiliot_internal
````
** *you can find your Bitbucket ID under ‘Your profile and setting’ > Workspace settings> Workspace ID* **

if a password is required after running the above line, generate an app password in your Bitbucket according to: 
[App passwords - Bitbucket Support](https://support.atlassian.com/bitbucket-cloud/docs/app-passwords/), 
and use this password to install the package

See the following images for a quick-password-generation-instructions:

![installation screen 1](wiliot/docs/images/installation1.png)
![installation screen 2](wiliot/docs/images/installation2.png)
