#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash
/home/chris/usr/HCMAC/ECMAC-baseline-DMMAC-UFC/run -u Cmdenv -f omnetpp_express.ini -r 3 -c Density2w-40
