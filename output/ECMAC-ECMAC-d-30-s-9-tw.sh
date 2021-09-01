#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash
/home/chris/usr/HCMAC/veins_HCMAC/run -u Cmdenv -f omnetpp_express_SCMAC.ini -r 9 -c Density2w-30
