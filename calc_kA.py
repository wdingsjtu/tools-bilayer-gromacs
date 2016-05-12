#!/usr/bin/env python
#
# Purpose: Calculate the Area-Compressibility from a GROMACS bilayer 
#          simulation. 
# Note: 1. A prerequisite is to calculate the XY-Area time series using the
#          "calc_area.py" in prior. 
#       2. Input is in "nm", output in "".
#       3. Formula:
#           kA = kB*T*<A> / var(A)
#       4. Results are accumulated results along the time series, intended 
#          to show the convergence trend, thus they are not independent. 
#          So it's NOT correct to perform average over these values.
# Syntax: calc_kA.py *.xvg temperature > kA.xvg
# Created: 2016/May/02
#

from __future__ import print_function
import numpy as np
import sys
from constants import kB as kB


def gate_keeping():
    if len(sys.argv) != 3:
        print("Syntax: calc_kA.py area.xvg T")
        sys.exit(0)
    return sys.argv[1:]

def print_captions():
    print("# Time kA")
    print("# ps   mN/m (dyn/cm)")
    print("# NOTE: Values are accumulated results, thus not independent.")
    print("#       So it's NOT correct to perform average over these values.")

def main(args):

    inFile = args[0]
    temp = float(args[1])
    print ("# Calculated from %s (T = %s)" %(inFile, temp))
    with open(inFile) as f:
        lines = f.readlines()
    
    print_captions()
    xyarea = []
    for line in lines:
        if line[0] in ['#', '@',]:
            continue
        words = line.split()
        xyarea.append(float(words[1]))
   
        mean_A = np.mean(xyarea) 
        var_A = np.var(xyarea) if len(xyarea) is not 1 else float('inf')
        kA__J_per_AA2 = kB * temp * mean_A / var_A
        kA__mN_per_m = kA__J_per_AA2 * 1e23  
        print(words[0], kA__mN_per_m)

if __name__ == '__main__':
    arguments = gate_keeping()    
    main(arguments)
