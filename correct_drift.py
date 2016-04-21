#!/usr/bin/env python
#
# Purpose: Correct the drifting in the calculated dipole potential 
#          profile due to discrete integrating amplifying effect.
#  
# Created: 2015/Jul/10
# Syntax:  c_d.py file 
# Example: c_d.py 11_uncorrected.dat > 11.dat


from __future__ import print_function

import sys
from string import split

def gate_keeping():
    if len(sys.argv) != 2:
        print ("Syntax: shift.py dpp.dat > corrected.dat")
        sys.exit()

def main(inFileName):
    with open(inFileName, 'r') as inFile:
        lines = inFile.readlines()
    
    coords = []
    values = []
    for line in lines: 
        if line[0] in ['#', '@']:
            print(line, end='')
        else: 
            words = split(line)
            coords.append(words[0])
            values.append(float(words[1]))
    
    deltaValue = (values[-1] - values[0]) / (len(values) - 1)
    
    for i, value in enumerate(values):
        newValue = value - deltaValue * i
        print(coords[i], newValue)
    
if __name__ == "__main__":
    gate_keeping()
    main(sys.argv[1])
