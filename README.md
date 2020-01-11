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

[Reference](http://hintshop.ludvig.co.nz/show/persistent-names-usb-serial-devices/ "Persistent names for usb-serial devices | HintShop" )

### Connecting 2 XBee S6Bs
Steps:
* 

References:
* [XBee Wi-Fi RF Module User Guide](https://www.digi.com/resources/documentation/digidocs/PDFs/90002180.pdf)
* [What is wrong with my Adhoc Network XBEE Wifi S6B, as the units are not communicating? - Digi Forum](https://www.digi.com/support/forum/53006/what-wrong-with-adhoc-network-xbee-wifi-units-communicating)

### Changing channels on XBee S6Bs
1. Open [XCTU](https://www.digi.com/resources/documentation/digidocs/90001526/tasks/t_download_and_install_xctu.htm) and open the configuration of the respective XBee.
2. Make sure that one XBee is in IBSS Creator and other IBSS Joiner mode. Only change the channel in XBee with IBSS Creator mode.
3. Click the "Switch to Consoles" icon ![Image of ICON](https://cdn.sparkfun.com/assets/learn_tutorials/2/2/3/console-icon.png) in the upper-right part of the window.
4. **open a serial connection** on each device by clicking the connect icon ![Image of ICON](https://cdn.sparkfun.com/assets/learn_tutorials/2/2/3/open-connect-icon.png). The icon will change, and the border of the console will turn green.
5. Type the following in the console section:
   * There should be 3 seconds gap between the previous command and the next command, w.r.t. the command:```+++```. A red-coloured ```OK``` will be printed in the console, if done correct. This switches the XBee into command mode.
   * Use ```atch``` to view the channel in Hexadecimal and ```atch <hex channel>``` to change the channnel of the XBee.
   * Use ```atwr``` to write the changes made in the channel.
   * Use ```atcn``` to close the command mode in XBee.
6. Disconnect the serial connection.
  
