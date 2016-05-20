#!/usr/bin/env python
#
# Purpose: Calculate MSD (mean squared displacement) from a GROMACS bilayer
#          simulation. 
# Note: 1. Input files needed:
#           coordinates.xvg (data file containing the coordinates of the group
#           of atoms along the time series)
#           box.xvg (box sizes corresponding to the time series)
#       2. 
# Syntax: calc_msd.py coord.xvg box.xvg nDim > msd.xvg
# Created: 2016/May/19
#

from __future__ import print_function
import numpy as np
import sys


def gate_keeping():
    if len(sys.argv) != 4:
        print("Syntax: calc_msd.py coord.xvg box.xvg nDim")
        sys.exit(0)
    print("# Calculated from %s and %s, nDim = %s." % tuple(sys.argv[1:]))
    return sys.argv[1:]

def print_captions():
    print("# Time MSD")
    print("# ps   nm^2")

def main(args):

    coordFile = args[0]
    boxFile = args[1]
    nDim = int(args[2])
    coordArray = []
    boxArray = []
    time = []
    timeFromBox = []

    # Read data
    with open(coordFile, 'rt') as f:
        lines = f.readlines()
    with open(boxFile, 'rt') as f:
        boxLines = f.readlines()
    for line in lines:
        if line[0] in ['#', '@',]:
            continue
        words = line.split()
        time.append(words.pop(0))
        coordArray.append(list(map(float, words)))
    for line in boxLines:
        if line[0] in ['#', '@',]:
            continue
        words = line.split()
        timeFromBox.append(words.pop(0))
        boxArray.append(list(map(float, words[:nDim]))) # words[:nDim]

    # Check consistency
    if time != timeFromBox:
        raise ValueError("Input file lengths don't match.")
    time = np.array(time)
    coordArray = np.array(coordArray)
    boxArray = np.array(boxArray)
    if coordArray.shape[1] % nDim: 
        raise ValueError("Input '%s' doesn't match expected dimensions."
                         % coordFile
        )
    elif boxArray.shape[1] != nDim:
        raise ValueError("Input '%s' doesn't match expected dimensions."
                         % boxFile
                        )

    # Calculation
    nAtoms = coordArray.shape[1] // boxArray.shape[1]
    MSD = np.zeros([coordArray.shape[0], nAtoms])
    for j in range(nAtoms):
        start = j * nDim
        origin = coordArray[0, start:(start + nDim)]
        realCoords = unwrap_coord(coordArray[:, start:(start + nDim)], 
                                  boxArray
                     )
        for i in range(0, realCoords.shape[0]):
            MSD[i, j] = calc_sd(realCoords[i], origin)

    # Print
    print_captions()
    for t, r in zip(time, MSD):
        print("%s %.4f" %(t, np.mean(r)))
#        print(t, r, np.mean(r))

def unwrap_coord(coord_series, box_series):
    ''' Given the wrapped coordinates, and box sizes (limits) in the interested
    dimension(s), calculate the real unwrapped coordinates: 
        If the displacement (from previous step to current step) > limit/2, the
    image count +1 (current coord < previous coord) or -1 (current > previous),
    so iteratively the image count accumulates, and the real coords = 
    coords + counts*limits.

    type_coord_series: np.array
    type_limit_series: np.array
    r_type: np.array
    '''
    real_coord_series = np.copy(coord_series)
    nImage = np.zeros(coord_series.shape[1])

    for i in range(1, coord_series.shape[0]):
        coords = coord_series[i]
        coordsPre = coord_series[i-1]
        limits = box_series[i] * 0.5
        for j in range(0, len(coords)):
            if abs(coords[j] - coordsPre[j]) < limits[j]: 
                pass
            elif coords[j] > coordsPre[j]:
                nImage[j] += -1
            elif coords[j] < coordsPre[j]:
                nImage[j] += 1
        real_coord_series[i] = coords + nImage * 2 * limits
    return real_coord_series

def calc_sd(pos, ref):
    ''' Calculate the squared displacement: (pos - ref)^2, where 'pos' and 
    'ref' are coord vectors.

    type_ref: np.array
    type_pos: np.array
    rtype: float
    '''
    delta = 0.0
    for coordp, coordr in zip(pos, ref):
        delta += np.square(coordp - coordr)
    return delta

if __name__ == '__main__':
    arguments = gate_keeping()
    main(arguments)
