#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash
python2.7 ./run-estn.py --nogui -e 7200 -s 3 --arrivalRate 10 --CTRMode 2
