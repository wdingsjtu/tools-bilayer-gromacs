#!/usr/bin/env python
#
# Purpose: Calculate the Bilayer Bending Modules for a GROMACS bilayer 
#          simulation, from calculated "kA" and "dHH". 
#          Formula:
#            kappaB = kA * (dHH -10)^2 / 24
# Note: 1. Prerequisites: 
#            The Area Compressibilty calculated:
#              "calc_kA.py" 
#            The H-H Thickness calculated:
#              "calc_thickness.py" 
#       2. Output unit is in "Joule" and "kBT".
#       3. Results are accumulated results along the time series, intended 
#          to show the convergence trend, thus they are not independent. 
#          So it's NOT correct to perform average over these values.
# Syntax: calc_bending.py kA.xvg dHH.xvg T > kappa.xvg
# Created: 2016/May/12
#

from __future__ import print_function
try: 
    import intertools.izip as zip
except ImportError:
    pass
import sys
from constants import kB 


def gate_keeping():
    if len(sys.argv) != 4:
        print("Syntax: calc_kA.py kA.xvg dHH.xvg T")
        sys.exit(0)
    return sys.argv[1:]

def print_captions():
    print("# Time kappa kappa ")
    print("# ps   J     kB*T")
    print("# NOTE: Values are accumulated results, thus not independent.")
    print("#       So it's NOT correct to perform average over these values.")

def main(args):

    kFile = args[0]
    dFile = args[1]
    T = float(args[2])
    print ("# Calculated from %s and %s (T = %s K)" %(kFile, dFile, T))
    with open(kFile, "rt") as f:
        kLines = f.readlines()
    with open(dFile, "rt") as f:
        dLines = f.readlines()

    time = []
    kA = []
    dHH = []
    for line in kLines:
        if line[0] in ['#', '@',]:
            continue
        words = line.split()
        time.append(words[0])
        kA.append(float(words[1]))
    for line in dLines:
        if line[0] in ['#', '@',]:
            continue
        words = line.split()
        dHH.append(float(words[1]))
   
    print_captions()
    for t, k, d in zip(time, kA, dHH):
        kappa_in_Joule = calc_kappa_1(k, d) 
        print("%s %.4E %.5f"
              %(t, kappa_in_Joule, kappa_in_Joule / (kB * T))) 

def calc_kappa_1(kA, dHH):
    '''
    kappa = kA * (dHH - 10)**2 / 24
    Units: kA in "mN/m" or "dyn/cm", dHH in "AA^2".
           Output in Joule.

    type_kA: float
    type_dHH: float
    rtype: float
    '''
    return 1e-23 * kA * (dHH - 10.0)**2 / 24.0

if __name__ == '__main__':
    arguments = gate_keeping()    
    main(arguments)
