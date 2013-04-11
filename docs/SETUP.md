# Setup info for pINK Raspberry Pi system #

## Directory structure ##

development
|-- python
    |-- projects
    |-- virtualenv

## Packages to install ##

### git ###
sudo apt-get install git

### python-pip ###
sudo apt-get install python-pip
sudo pip install pip --upgrade

### virtualenv ###
sudo pip install virtualenv

### In development/python/virtualenv ###
virtualenv pINK
source pINK/bin/activate

### install python packages ###
pip install requests
pip install python-instagram
pip install watchdog

### cups-pdf ###
sudo apt-get install cups-pdf

## Bluetooth setup ##


## Wifi setup ##

