# Genesys-2.0
A website to control and evaluate the actions of the Rover designed and build for IRC 2020. Technocrats Robotics


### Auto-detect port for XBee using /dev/xbee
In Terminal, do the following
* `cd /etc/udev/rules.d`
* Make a file named **99-usb-serial.rules**
* Add the following content: 
`SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", ATTRS{serial}=="0001", SYMLINK+="xbee"`
* Disconnect and re-connect the XBee
* Now, try `ls -l /dev/xbee` to check, from the root directory in Terminal.
