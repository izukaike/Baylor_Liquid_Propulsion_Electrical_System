#!/bin/bash

"C:/Program Files/Python312/python.exe" "c:/Users/izuka/OneDrive/Documents/Code/Baylor Aero/LFRE2/Test Folder/DAC Verification/oscope1.py" &
ssh raspberrypi << EOF
    cd /home/pi/lfre2code/
    > pitime.txt
    > data.txt

    echo password123 | sudo -S ./adc_v &

    exit
EOF


scp raspberrypi:/home/pi/lfre2code/data.txt  .
scp raspberrypi:home/pi/lfre2code/pitime.txt .




