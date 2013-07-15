# pINK #

Print 'polaroid' style Instagram posts by hashtag. Intended to run on the Raspberry PI. Prototyped on a Mac.

## Installation notes ##

+ `virtualenv /your/env/pINK`
+ `source /your/env/pINK/bin/activate`
+ `pip install requests`
+ `pip install python-instagram`
+ `pip install watchdog`
+ `pip install pyobjc`

+ [Register Instagram client](http://instagram.com/developer/clients/register "Register Instagram client")
+ Rename \_SECRET.py to SECRET.py and fill in client\_id, client\_secret, redirect\_uri
+ Run `python PogoIngress.py`
+ Run `python InstagramHashtagIngress.py [hashtag]`

## Demo ##

http://www.youtube.com/watch?v=zaz_IPAp5tw

## Resources ##

### Related Links ###

+ [Instagram API](http://instagram.com/developer/api-console/ "Instagram API")
+ [Manager Instagram Clients](http://instagram.com/developer/clients/manage "Manage Instagram Clients")
+ [Register Instagram Client](http://instagram.com/developer/clients/register "Register Instagram Client")
+ [Raspberry Pi and Polaroid PoGo Bluetooth Printer](http://opalfruits.net/blog/index.php/2013/02/14/raspberry-pi-and-polaroid-pogo-bluetooth-printer-part-1 "Raspberry Pi and Polaroid PoGo Bluetooth Printer")
+ [Free Instagram Printer](http://leemart.in/instaprinter "Free Instagram Printer")

### Other Instagram Printers ###

+ [Instaprint](http://instaprint.me/ "Instaprint")
+ [Insta Party Box](http://jamsdtf.com/instapartybox/ "Insta Party Box")
+ [Cheapstaprint](http://www.welcometocreature.com/blog/2012/11/20/cheapstaprint.html "Cheapstaprint")

## Bluetooth ##
+ [OS X Bluetooth Framework Reference](https://developer.apple.com/library/mac/#documentation/devicedrivers/Reference/IOBluetooth/_index.html)
+ [Bluetooth on OS X](https://developer.apple.com/library/mac/#documentation/DeviceDrivers/Conceptual/Bluetooth/BT_Bluetooth_On_MOSX/BT_Bluetooth_On_MOSX.html "Bluetooth on OS X")
+ [PyObjC](http://pythonhosted.org/pyobjc/install.html "PyObjC")
+ [Elementary Bluetooth using PyObjC](http://pseudofish.com/elementary-bluetooth-using-pyobjc.html "Elementary Bluetooth using PyObjC")
