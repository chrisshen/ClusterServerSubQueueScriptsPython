#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash
/home/chris/usr/HCMAC/veins-veins-4.6-EDCA/run -u Cmdenv -f omnetpp_express.ini -r 7 -c Density2w-45
