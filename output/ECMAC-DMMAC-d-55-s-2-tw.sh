#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash
/home/chris/usr/HCMAC/veins_DMMAC/run -u Cmdenv -f omnetpp_express.ini -r 2 -c Density2w-55
