#! /usr/bin/env python
#
#
#  Created: 2016/Apr/18


from __future__ import print_function

import sys
import scipy.interpolate as itp

def gate_keeping():
    if len(sys.argv) != 3:
        print("Syntax: in.py dataFile gridSize")
        sys.exit(0)

def main():
    inFile = sys.argv[1]
    print ("# Interpolated from %s (Grid size = %s)" %(inFile, sys.argv[2]))
    with open(inFile) as f:
        lines = f.readlines()
    
    coords = []
    values = []
    for line in lines:
        if line[0] in ['#','@']:
            print(line, end='')
            continue
        words = line.split()
        coords.append(float(words[0]))
        values.append(words[1])
    
    gridsize = float(sys.argv[2])
    f = itp.interp1d(coords, values)
    new_coords = gen_grid(coords, gridsize)
    for xn, yn in zip(new_coords, f(new_coords)):
        #print("{%.4f} {:f}".format(xn, yn))
        print("%.4f %f" %(xn, yn))

def gen_grid(_list, step):
    '''
    Output a new list that covers the range of the given list(_list), with a
    grid step of the given step size (step).

    _list: float list
    step: float

    rtype: float list
    '''
    # a round-up float number
    start = int(_list[0]/step)*step + step 

    grid = [start]
    while grid[-1] < _list[-1]:
        grid.append(grid[-1] + step)
    return grid[:-1]

if __name__ == '__main__':
    gate_keeping()    
    main()
