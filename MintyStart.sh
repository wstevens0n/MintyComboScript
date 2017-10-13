#!/usr/bin/env bash

python /home/pi/MintyComboScript/MintyCombo.py &
sleep 20
python /home/pi/MintyComboScript/MintyBatteryMonitor.py &
