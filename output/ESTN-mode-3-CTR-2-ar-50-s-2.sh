#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash
python2.7 ./run-estn.py --nogui -e 7200 -s 2 --arrivalRate 50 --CTRMode 2 -m 3