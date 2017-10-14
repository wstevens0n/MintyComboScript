#!/usr/bin/env python2.7

'''
Date:  10/08/17
Author:  HoolyHoo
Version:  3.0
Name:  Combo Shortcut Script - Utility for the MintyPi project.
Description:  Monitors GPIO interrupts to adjust volume with icons, lcd dimming, battery monitor, wifi and bluetooth toggle, and performs safe shutdown.
Usage:  Mode + Y = Toggle Wifi with Icon
        Mode + B = Toggle BT with Icon
        Mode + A = Toggle Battery
        Mode + X = Initiate Safe Shutdown
        Mode + Dpad Right = Volume Up with Icon
        Mode + Dpad Left  = Volume Down with Icon
        Mode + Dpad Up    = Dimming Up
        Mode + Dpad Down  = Dimming Down
        Mode + Right Shoulder = Display Cheat
'''

from gpiozero import Button
from signal import pause
from subprocess import check_call
import wiringpi
import os
import time
import pickle


def grabPin(file, directory):
    try:
        with open(file, 'r') as f:
            pin = f.read()
    except IOError:
        if not os.path.isdir(directory):
            os.makedirs(directory)
            with open(file, 'w') as f:
                f.write('7')
            pin = '7'
        else:
            with open(file, 'w') as f:
                f.write('7')
            pin = '7'
    return int(pin)


pinFile = "/boot/mintypi/pinfile.txt"
pinDirectory = "/boot/mintypi/"
pngviewPath = "/home/pi/MintyComboScript/Pngview/"
iconPath = "/home/pi/MintyComboScript/icons"
statePath = "/home/pi/MintyComboScript/combo.dat"
comboStates = {'wifi': 1, 'bluetooth': 1, 'volume': 60, 'brightness': 1024, 'battery': 1}
functionPin = grabPin(pinFile, pinDirectory)
functionBtn = Button(functionPin)
brightnessUpBtn = Button(4)
brightnessDownBtn = Button(5)
volumeUpBtn = Button(22)
volumeDownBtn = Button(14)
shutdownBtn = Button(26)
monitorBtn = Button(21)
wifiBtn = Button(20)
bluetoothBtn = Button(16)
cheatBtn = Button(6)
led = 1


# Functions
def brightnessUp():
    if brightnessUpBtn.is_pressed:
        comboStates['brightness'] = min(1024, comboStates['brightness'] + 100)
        controlBrightness()


def brightnessDown():
    if brightnessDownBtn.is_pressed:
        comboStates['brightness'] = max(0, comboStates['brightness'] - 100)
        controlBrightness()


def volumeDown():
    comboStates['volume'] = max(0, comboStates['volume'] - 10)
    os.system("amixer sset -q 'PCM' " + str(comboStates['volume']) + "%")
    showVolumeIcon()


def volumeUp():
    comboStates['volume'] = min(100, comboStates['volume'] + 10)
    os.system("amixer sset -q 'PCM' " + str(comboStates['volume']) + "%")
    showVolumeIcon()


def wifiToggle():
    if comboStates['wifi'] == 1:
        os.system("sudo rfkill block wifi")
        os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/wifiOff.png &")
        time.sleep(3)
        killPngview()
        comboStates['wifi'] = 0
    else:
        os.system("sudo rfkill unblock wifi")
        os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/wifiOn.png &")
        time.sleep(3)
        killPngview()
        comboStates['wifi'] = 1


def bluetoothToggle():
    if comboStates['bluetooth'] == 1:
        os.system("sudo rfkill block bluetooth")
        os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/bluetoothOff.png &")
        time.sleep(3)
        killPngview()
        comboStates['bluetooth'] = 0
    else:
        os.system("sudo rfkill unblock bluetooth")
        os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/bluetoothOn.png &")
        time.sleep(3)
        killPngview()
        comboStates['bluetooth'] = 1


def shutdown():
    for i in range(0, 3):
        os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/shutdown.png &")
        time.sleep(1)
        killPngview()
        time.sleep(.5)
    writeData(statePath)
    time.sleep(1)
    check_call(['sudo', 'poweroff'])


def toggleState():
    if comboStates['battery'] == 1:
        os.system('sudo pkill -f "python /home/pi/MintyComboScript/MintyBatteryMonitor.py"')
        comboStates['battery'] = 0
        writeData(statePath)
        time.sleep(2)
        os.system("python /home/pi/MintyComboScript/MintyBatteryMonitor.py &")
        time.sleep(1)
    else:
        os.system('sudo pkill -f "python /home/pi/MintyComboScript/MintyBatteryMonitor.py"')
        comboStates['battery'] = 1
        writeData(statePath)
        time.sleep(2)
        os.system("python /home/pi/MintyComboScript/MintyBatteryMonitor.py &")
        time.sleep(1)


def showVolumeIcon():
    killPngview()
    while volumeUpBtn.is_pressed or volumeDownBtn.is_pressed:
        if volumeUpBtn.is_pressed:
            os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/Volume" + str(comboStates['volume']) + ".png &")
            comboStates['volume'] = min(100, comboStates['volume'] + 10)
            os.system("amixer sset -q 'PCM' " + str(comboStates['volume']) + "%")
            killPngview()
        elif volumeDownBtn.is_pressed:
            os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/Volume" + str(comboStates['volume']) + ".png &")
            comboStates['volume'] = max(0, comboStates['volume'] - 10)
            os.system("amixer sset -q 'PCM' " + str(comboStates['volume']) + "%")
            killPngview()
    else:
        os.system("amixer sset -q 'PCM' " + str(comboStates['volume']) + "%")
        os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/Volume" + str(comboStates['volume']) + ".png &")
        time.sleep(2)
        killPngview()


def controlBrightness():
    wiringpi.pwmWrite(led, comboStates['brightness'])
    time.sleep(.2)


def showCheat():
    os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/cheat.png &")
    time.sleep(5)
    killPngview()


def killPngview():
    os.system("sudo killall -q -15 pngview2")


def readData(filepath):
    with open(filepath, 'rb') as file:
        return pickle.load(file)


def writeData(filepath):
    with open(filepath, 'wb') as file:
        pickle.dump(comboStates, file)


def checkFunction():
    while functionBtn.is_pressed:
        if brightnessUpBtn.is_pressed:
            brightnessUp()
        elif brightnessDownBtn.is_pressed:
            brightnessDown()
        elif volumeUpBtn.is_pressed:
            volumeUp()
        elif volumeDownBtn.is_pressed:
            volumeDown()
        elif shutdownBtn.is_pressed:
            shutdown()
        elif monitorBtn.is_pressed:
            toggleState()
        elif wifiBtn.is_pressed:
            wifiToggle()
        elif bluetoothBtn.is_pressed:
            bluetoothToggle()
        elif cheatBtn.is_pressed:
            showCheat()


# Initial File Setup
try:
    comboStates = readData(statePath)
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(led, 2)
    wiringpi.pwmWrite(led, comboStates['brightness'])
    os.system("amixer sset -q 'PCM' " + str(comboStates['volume']) + "%")
    if comboStates['wifi'] == 1:
        os.system("sudo rfkill unblock wifi")
    else:
        os.system("sudo rfkill block wifi")
    if comboStates['bluetooth'] == 1:
        os.system("sudo rfkill unblock bluetooth")
    else:
        os.system("sudo rfkill block bluetooth")
except:
    writeData(statePath)
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(led, 2)
    wiringpi.pwmWrite(led, comboStates['brightness'])
    os.system("amixer sset -q 'PCM' " + str(comboStates['volume']) + "%")
    if comboStates['wifi'] == 1:
        os.system("sudo rfkill unblock wifi")
    else:
        os.system("sudo rfkill block wifi")
    if comboStates['bluetooth'] == 1:
        os.system("sudo rfkill unblock bluetooth")
    else:
        os.system("sudo rfkill block bluetooth")

# Interrupt
functionBtn.when_pressed = checkFunction
pause()
