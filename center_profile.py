#!/usr/bin/env python
#
# Purpose: Center the coordinates in a .xvg file to zero, i.e. if the original
#          coordinate ranges from [0, Z], the output range will be [-Z/2, Z/2].           
# Note: Normally, the input .xvg should be a density profile generated from a  
#       processed (lipid-centerred, box-modified) trajectory by "".
# Syntax: center.py *.xvg > centered.xvg
# Created: 2016/Mar/21


from __future__ import print_function
import sys
import re 


if len(sys.argv) is not 2:
    print("Syntax: center.py *.xvg > centerred.*.xvg")
    sys.exit()

with open(sys.argv[1]) as f:
    lines = f.readlines()

#coordPattern = re.compile(r'\S+')
#for line in lines:
#    if line[0] not in ['#', '@']:
#        coord = coordPattern.search(line).group()
#        rest = coordPattern.split(line, maxsplit=1)
#        #print(words)
#        #coord = float(words[0])
#        #values = words[1:]
#        print(rest[0], coord, rest)
#        #print(coord, values)
coords = []
for line in lines:
    if line[0] not in ['#', '@']:
        words = line.split()
        coords.append(float(words[0]))

if len(coords) % 2:
    diff = coords[(len(coords)-1)/2]
else: 
    diff = (coords[len(coords)/2] + coords[len(coords)/2 - 1])/2.0 

print("# Recentered from %s" % sys.argv[1])
for line in lines:
    if line[0] in ['#', '@']:
        print(line, end='')
    else: 
        words = line.split()
        coord = float(words[0]) - diff
        rest = words[1:]
        print(coord, ''.join(rest))
