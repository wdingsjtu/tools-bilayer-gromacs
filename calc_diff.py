#!/usr/bin/env python
#
# Purpose: Calculate D (2-D diffussion coeffecient) from an MSD (mean squared 
#          displacement) dataset
# Note: 1. Input files needed:
#           msd.dat 
#       2. 
# Syntax: calc_diff.py msd.dat > diff.xvg
# Created: 2016/Oct/26
#

from __future__ import print_function
import numpy as np
from scipy import optimize
import sys


def gate_keeping():
    if len(sys.argv) != 2:
        print("Syntax: calc_diff.py msd.dat > diff.xvg")
        sys.exit(0)
    print("# Calculated from %s." % tuple(sys.argv[1:]))
    return sys.argv[1:]

def print_captions():
    print("# Time D")
    print("# ps   nm^2/ps")

def main(args):

    msdFile = args[0]
    msd = []
    time = []

    # Read data
    with open(msdFile, 'rt') as f:
        lines = f.readlines()
    for line in lines:
        if line[0] in ['#', '@',]:
            continue
        words = line.split()
        time.append(float(words[0]))
        msd.append(float(words[1]))

    # Print
    print_captions()
    print('# Fitted result is (nm2/mus): %.4f'
           %calc_diff_fit(time, msd)
    )
    print('# Divided result is (nm2/mus, n = %s): %.4f \pm %.4f'
           %(calc_diff_ratio(time, msd)[2],
             calc_diff_ratio(time, msd)[0],
             calc_diff_ratio(time, msd)[1],
           )
    )

def calc_diff_fit(t, m):
    fitFunc = lambda p, x: p * x
    errFunc = lambda p, x, y: y - fitFunc(p, x)
    fit = optimize.leastsq(errFunc, 1.0, args=(t, m), full_output=1)

    return fit[0][0] * 1e6 / 4

def calc_diff_ratio(t, m):
    start = int(len(t) * 0.8)
    diff = []
    for ti, mi in zip(t[start:], m[start:]):
        diff.append(1e6 * (mi - m[0]) / (4 * (ti - t[0])))

    return np.mean(diff), np.std(diff), len(diff)

if __name__ == '__main__':
    arguments = gate_keeping()
    main(arguments)
