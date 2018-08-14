#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash
python2.7 ./run-estn.py --nogui -e 7200 -s 4 --arrivalRate 30 --CTRMode 2 -m 3
