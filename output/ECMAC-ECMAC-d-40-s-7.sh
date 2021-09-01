#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash
/home/chris/usr/HCMAC/veins_HCMAC/run -u Cmdenv -f omnetpp_express_SCMAC.ini -r 7 -c Density-40
