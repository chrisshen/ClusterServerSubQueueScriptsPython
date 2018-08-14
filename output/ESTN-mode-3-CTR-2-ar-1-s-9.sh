#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash
python2.7 ./run-estn.py --nogui -e 7200 -s 9 --arrivalRate 1 --CTRMode 2 -m 3
