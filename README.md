# MintyComboScript
This script is used in conjuction with latest MintyPi board for battery monitoring and the use of a series of shortcut combos to perform various task.

This script will display a battery icon according to battery level and will show a warning video when reaching low level.  Upon critical battery level, the script will show a critical battery level warning video and then introduce a safe shutdown.  The battery monitoring can be toggled on or off with a combo shortcut.

Also included in this script is the ability to perform shorcut combos with the use of a mode button to change volume, dimming level, toggle wifi and bluetooth, and do a quick and graceful shutdown.  Also included is a combo to display the list of combos available.

The mode button is by default an independant button installed to GPIO 7 but the script has the ability to use 'Start' as a mode as well if no indepandent mode button is present.  This option can be changed by altering the value in /boot/mintypi/pinfile.txt from 7 to 15.

## Combo Shortcuts
* Mode + A   = Toggle Battery
* Mode + Y   = Toggle Wifi with Icon
* Mode + B   = Toggle Bluetooth with Icon
* Mode + X   = Initiate Safe Shutdown
* Mode + Dpad Right   = Volume Up with Icon
* Mode + Dpad Left   = Volume Down with Icon
* Mode + Dpad Up   = Dimming Up
* Mode + Dpad Down   = Dimming Down
* Mode + Right Shoulder =  Display Shortcut Cheatsheet

More information can be obtained from this thread:
http://www.sudomod.com/forum/index.php


## Automated Software Install

Go to raspberry command prompt or SSH.
Make sure you are in the home directory by typing ```cd ~ ``` and then type:
```
wget https://raw.githubusercontent.com/HoolyHoo/MintyComboScript/master/MintyInstall.sh
```
Then type:
```
sudo git clone https://github.com/HoolyHoo/MintyComboScript.git
```
Then type:
```
sudo chmod 777 MintyInstall.sh
```
And then type:
```
sudo ./MintyInstall.sh
```
Finally reboot to have it all start on boot with:
```
sudo reboot
```
