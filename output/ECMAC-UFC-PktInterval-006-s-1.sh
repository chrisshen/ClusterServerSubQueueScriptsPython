#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash
/home/chris/usr/HCMAC/ECMAC-baseline-DMMAC-UFC/run -u Cmdenv -f omnetpp_express.ini -r 1 -c PktInterval-006
