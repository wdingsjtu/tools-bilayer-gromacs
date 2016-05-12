#!/usr/bin/env python
#
# Purpose: Calculate the XY-Area and Area-Per-Lipid from a GROMACS bilayer 
#          simulation. 
# Note: 1. A necessary processing of the raw output data (*.edr) is:
#          $ echo "box-X box-Y box-Z" | gmx energy -f *.edr -o box.xvg
#       2. Input in "nm", output in "AA^2".
# Syntax: calc_area.py *.xvg NoOfLipids > area.xvg
# Created: 2016/May/02
#

from __future__ import print_function
import sys


def gate_keeping():
    if len(sys.argv) != 3:
        print("Syntax: calc_area.py *.xvg NoOfLipids")
        sys.exit(0)

def main():

    inFile = sys.argv[1]
    nlipids = int(sys.argv[2])
    print ("# Calculated from %s (%s lipids)" %(inFile, nlipids))
    with open(inFile) as f:
        lines = f.readlines()
    
    time = []
    xyarea = []
    for line in lines:
        if line[0] in ['#', '@',]:
            continue
        words = line.split()
        time.append(float(words[0]))
        xyarea.append(float(words[1]) * float(words[2]) * 100)
   
    print_captions()
    for t, A in zip(time, xyarea):    
        print("%s %.8f %8f" %(t, A, A/(nlipids/2)))

def print_captions():
    print("# Time XY-Area AreaPerLipid")
    print("# ps   AA^2    AA^2")

if __name__ == '__main__':
    gate_keeping()    
    main()
