#!/usr/bin/env python
#
# Purpose: Calculate the MSD (me sq dis) from a GROMACS 
#          bilayer simulation. 
# Note: 1.
#         th layers:
#         g 2 -com -fp -ox  
#       2.
# Syntax: calc_thickness.py *.xvg  > dHH.xvg
# Created: 2016/May/19
#

from __future__ import print_function
import numpy as np
import sys


def gate_keeping():
    if len(sys.argv) != 3:
        print("Syntax: calc_msd.py coord.xvg box.xvg")
        sys.exit(0)
    return sys.argv[1:]

def print_captions():
    print("# Time MSD")
    print("# ps   nm^2")

def main(args):

    coordFile = args[0]
    boxFile = args[1]
    nDim = 3
    print ("# Calculated from %s." %coordFile)
    with open(coordFile, 'rt') as f:
        lines = f.readlines()
    with open(boxFile, 'rt') as f:
        boxLines = f.readlines()

    coordArray = []
    boxArray = []
    for line in lines:
        if line[0] in ['#', '@',]:
            continue
        words = line.split()
        coordArray.append(list(map(float, words)))
    for line in boxLines:
        if line[0] in ['#', '@',]:
            continue
        words = line.split()
        boxArray.append(list(map(float, words[:4])))
    coordArray = np.array(coordArray)
    boxArray = np.array(boxArray)

    #TODO check time consistency in box and coord.
    time = coordArray[:, 0]

    if (coordArray.shape[1] - 1) % nDim or (boxArray.shape[1] - 1) != nDim:
        raise ValueError("Input data don't match expected dimensions.")
    nAtoms = coordArray.shape[1] // boxArray.shape[1]
    MSD = np.zeros([coordArray.shape[0], nAtoms])
    for i in range(nAtoms):
        start = i * nDim + 1
        origin = coordArray[0, start:(start + nDim)]
        realCoords = unwrap_coord(coordArray[:, start:(start + nDim)], 
                                  boxArray[:, 1:]
                     )
        for j in range(0, realCoords.shape[0]):
            MSD[j, i] = calc_sd(realCoords[j], origin)

    print_captions()
    for t, r in zip(time, MSD):
        print("%s, %.4f" %(t, r))

def unwrap_coord(coord_series, box_series):
    ''' Given the wrapped coordinates and the wrapping limits (box sizes), 
    calculate the real unwrapped coordinates: 
        If coord displacement > limit/2, the image count +1 (current coord < 
    previous coord) or -1 (current > previous), so iteratively the image 
    count acuumulates, and real coords = coords + counts*limits.

    type_coord_series: np.array
    type_limit_series: np.array
    r_type: np.array
    '''
    real_coord_series = np.array(coord_series)
    real_coord_series[0] = coord_series[0]
    nImage = np.zeros(coord_series.shape[1])

    for i in range(1, coord_series.shape[0]):
        coords = coord_series[i, :]
        coordsPre = coord_series[i-1, :]
        limits = box_series[i, :] * 0.5
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
