#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash
python2.7 ./run-estn.py --nogui -e 360 -s 9 --arrivalRate 40 --CTRMode 2
