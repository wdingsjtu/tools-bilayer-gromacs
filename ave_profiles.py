#!/usr/bin/env python
#
# Purpose: Average profiles obtained from temporal blocks. 
# Note: 1. Coordinates in each single profile can be a subset of one another.
#          E.g. one with [1,2,3,4] and another with [1,2,3,4,5] are accepted.
#       2. However, they cannot be totally different.
#          E.g. [1, 2, 3, 4] and [1.1, 2.1, 3.1, 4.1] are not handled well.
#       So, use the "interpolate.py" to pre-process the profiles in prior.
# Syntax: ave_profiles.py [files] > data.ave
# Created: 2016/May/12
#

from __future__ import print_function
import sys


def gate_keeping():
    if len(sys.argv) == 1:
        print("Syntax: ave_profiles.py [files]")
        sys.exit(0)
    return sys.argv[1:]

def print_captions(filenames):
    '''
    type_filenames: str

    '''
    print("# Aved from %s" %filenames)

def main(args):
    '''
    '''
    #TODO: calculate STD.
    valueDict = {}
    for inFile in args:
        with open(inFile) as f:
            lines = f.readlines()
    
        for line in lines:
            if line[0] in ['#', '@',]:
                continue
            words = line.split()
            if words[0] not in valueDict: 
                valueDict[words[0]] = [float(words[1])]
            else:
                valueDict[words[0]].append(float(words[1]))

    print_captions(' '.join(args))
    for coord in sorted(valueDict, key=lambda x: float(x)):
        vArray = valueDict[coord]
        print(coord, sum(vArray)/len(vArray))

if __name__ == '__main__':
    arguments = gate_keeping()    
    main(arguments)
