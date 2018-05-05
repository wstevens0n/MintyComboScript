#!/usr/bin/env python2.7

'''
Date:  10/08/17
Author:  HoolyHoo
Version:  3.0
Name:  Battery Monitor Script - Utility for the MintyPi project.
Description:  Monitors analog input for voltage and displays battery icon related to the input.  Displays low warning battery video at 25% battery level and displays shutdown video at critical battery level followed by a gracefull safe shutdown.
Usage:  Battery icons can be toggled and state remembered by using shortcut combo, "Mode + A".

'''

import time
import os
import signal
from subprocess import check_output
import Adafruit_ADS1x15
import pickle


# Config
warning = 0
status = 0
debug = 0
iconState = ""
toggleFile = "/home/pi/MintyComboScript/Toggle.txt"
PNGVIEWPATH = "/home/pi/MintyComboScript/Pngview/"
ICONPATH = "/home/pi/MintyComboScript/icons"
statePath = "/home/pi/MintyComboScript/combo.dat"
CLIPS = 1
REFRESH_RATE = 2
VOLT100 = 4.09  # 4.09
VOLT99 = 4.08   # 4.09 
VOLT75 = 3.68   # 3.76
VOLT50 = 3.46   # 3.63
VOLT25 = 3.35    # 3.5
VOLT0 = 3.25     # 3.2
adc = Adafruit_ADS1x15.ADS1015()
GAIN = 1


def readData(filepath):
    with open(filepath, 'rb') as file:
        return pickle.load(file)


def changeicon(percent):
    global iconState
    if iconState != percent:
        iconState = percent
        i = 0
        killid = 0
        os.system(PNGVIEWPATH + "/pngview -b 0 -l 3000" + percent + " -x 650 -y 10 " + ICONPATH + "/battery" + percent + ".png &")
        out = check_output("ps aux | grep pngview | awk '{ print $2 }'", shell=True)
        nums = out.split('\n')
        for num in nums:
            i += 1
            if i == 1:
                killid = num
                os.system("sudo kill " + killid)


def endProcess(signalnum=None, handler=None):
    os.system("sudo killall pngview")
    exit(0)


def readVoltage():
    value = adc.read_adc(0, gain=GAIN)
    return value


def convertVoltage(sensorValue):
    voltage = float(sensorValue) * (4.09 / 2047.0)
    return voltage


# Initial Setup

signal.signal(signal.SIGTERM, endProcess)
signal.signal(signal.SIGINT, endProcess)
comboStates = readData(statePath)


# Begin Battery Monitoring

os.system(PNGVIEWPATH + "/pngview -b 0 -l 299999 -x 650 -y 10 " + ICONPATH + "/blank.png &")

if comboStates['battery'] == 1:
    while True:
        try:
            ret1 = readVoltage()
            time.sleep(.4)
            ret2 = readVoltage()
            time.sleep(.4)
            ret3 = readVoltage()
            time.sleep(.4)
            ret4 = (ret1 + ret2 + ret3) / 3
            ret = convertVoltage(ret4)
            if debug == 1:
                print(ret)
            if ret < VOLT0:
                if status != 0:
                    changeicon("0")
                    if CLIPS == 1:
                        os.system("/usr/bin/omxplayer --no-osd --layer 999999  " + ICONPATH + "/lowbattshutdown.mp4 --alpha 160;")
                        os.system("sudo shutdown -h now")
                status = 0
            elif ret < VOLT25:
                if status != 25:
                    changeicon("25")
                    if warning != 1:
                        if CLIPS == 1:
                            os.system("/usr/bin/omxplayer --no-osd --layer 999999  " + ICONPATH + "/lowbattalert.mp4 --alpha 160")
                        warning = 1
                status = 25
            elif ret < VOLT50:
                if status != 50:
                    changeicon("50")
                status = 50
            elif ret < VOLT75:
                if status != 75:
                    changeicon("75")
                status = 75
            elif ret < VOLT99:
                if status != 99:
                    changeicon("99")
                status = 99
            else:
                if status != 100:
                    changeicon("100")
                status = 100

            time.sleep(REFRESH_RATE)
        except IOError:
            print('No i2c Chip Found!')
            exit(0)

elif comboStates['battery'] == 0:
    while True:
        try:
            ret1 = readVoltage()
            time.sleep(.4)
            ret2 = readVoltage()
            time.sleep(.4)
            ret3 = readVoltage()
            time.sleep(.4)
            ret4 = (ret1 + ret2 + ret3) / 3
            ret = convertVoltage(ret4)
            if debug == 1:
                print(ret)
            if ret < VOLT0:
                if status != 0:
                    changeicon("0")
                    if CLIPS == 1:
                        os.system("/usr/bin/omxplayer --no-osd --layer 999999  " + ICONPATH + "/lowbattshutdown.mp4 --alpha 160;")
                        os.system("sudo shutdown -h now")
                    status = 0
            elif ret < VOLT25:
                if status != 25:
                    changeicon("25")
                    if warning != 1:
                        if CLIPS == 1:
                            os.system("/usr/bin/omxplayer --no-osd --layer 999999  " + ICONPATH + "/lowbattalert.mp4 --alpha 160")
                        warning = 1
                status = 25
            elif ret < VOLT50:
                status = 50
            elif ret < VOLT75:
                status = 75
            elif ret < VOLT99:
                status = 99
            else:
                status = 100

            time.sleep(REFRESH_RATE)
        except IOError:
            print('No i2c Chip Found!')
            exit(0)
