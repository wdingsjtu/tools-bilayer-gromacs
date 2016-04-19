#!/usr/bin/env python
#
# Purpose: Generate a text file which lists all "atomnames" and their
#          corresponding per-atom electron numbers, in the format required by
#          "gmx_density" for calculating the electron density.
#
# Notes: A file which contains all the "atomnames" needs to be provided, which 
#        can be one of the following:
#        * forcefield data file (.top/.itp)
#          -> Don't forget to add OW, HW1, HW2 for water!
#        * topology file (.gro)
#
# Syntax: genElectron.py *.(tpr,itp) > electron.dat
#
# Created: 2016/Mar/14


from __future__ import print_function
import sys


if len(sys.argv) is not 2:
    print("Syntax: genElectron.py *.(top,itp,gro) > electron.dat")
    sys.exit()
else:
    fileSuffix = sys.argv[1][-3:]
    if fileSuffix in ["top", "itp"]:
        fileFlag = "itp"
    elif fileSuffix in ["gro"]:
        fileFlag = "gro"
    else:
        print("File with suffix '.%s' is not supported" % fileSuffix)
        sys.exit()

eNumDict = {
  'H': '1',
  'C': '6',
  'N': '7',
  'O': '8',
  'P': '15',
  'S': '16',
}

with open(sys.argv[1] , 'rt') as ffFile:
    lines = ffFile.readlines()

if fileFlag == "itp":
    section = ''
    atomNames = []
    for line in lines:
        if line[0] == '[':
            section = line.split()[1]
            continue
        if section == 'atoms' and line[0] != ';' and line != '\n':
            atomNames.append(line.split()[4])
elif fileFlag == "gro":
    atomNames = []
    for line in lines[2:-1]:
        if line[10:15].strip() not in atomNames:
            atomNames.append(line[10:15].strip())

print(len(set(atomNames)))
for name in set(atomNames):
    print(' '.join([name, '=', eNumDict[name[0]]]))
