#!/usr/bin/env python
#
# Purpose: Calculate the Head-Head Thickness (P-P distance) from a GROMACS 
#          bilayer simulation. 
# Note: 1. Prerequisites:
#            Obtain the COM of P-atoms in both layers:
#              $ gmx traj -f *trr -n *ndx -ng 2 -com -fp -ox  
#       2. Input in "nm", output in "AA^2".
# Syntax: calc_thickness.py *.xvg  > dHH.xvg
# Created: 2016/May/12
#

from __future__ import print_function
import sys
import re 


def gate_keeping():
    if len(sys.argv) != 2:
        print("Syntax: calc_thickness.py com.xvg")
        sys.exit(0)
    return sys.argv[1:]

def main(arg):

    inFile = arg[0]
    print ("# Calculated from %s." %inFile)
    with open(inFile) as f:
        lines = f.readlines()

    time = []
    ppDistance = []
    for line in lines:
        if line[0] in ['#', '@',]:
            continue
        words = line.split()
        time.append(words[0])
        ppDistance.append(abs(float(words[1]) - float(words[2])))
   
    print_captions()
    for t, d in zip(time, ppDistance):    
        print(t, d * 10) # unit in AA

def print_captions():
    print("# Time Thickness")
    print("# ps   AA")

if __name__ == '__main__':
    arguments = gate_keeping()    
    main(arguments)
