#!/usr/bin/env python
#
# Purpose: Calculate k*c (product of bending modulus and spontaneous curvature,
#          1st integral moment) and kG (Gaussian modulus, 2nd integral moment) 
#          from a centerred lateral pressure profile. 
# Note: 1. Prerequisite: LPP calculated (stress2lpp.py) and centerred 
#                        (center_profile.py)
#          Input units: coordinate in nm;
#                       pressure in bar (10^5 Pa)
#       2. Output in the unit of "kBT/nm" and "kBT". The final finite integrals 
#          are output both into file and on screen. Accumulative values along 
#          the corrdinates are columned in file.  
#       3. Formula:
#          k*c = int_{0}^{l} z * \Pi(z) dz
#          kG  = int_{0}^{l} z^2 * \Pi(z) dz 
# Syntax: calc_curv.py *.dat > tau.xvg
# Created: 2016/May/04


from __future__ import print_function
import numpy as np
import sys
from constants import kB as kB


def gate_keeping():
    if len(sys.argv) != 2:
        print("Syntax: calc_curv.py *.dat > tau.xvg")
        sys.exit(0)
    return sys.argv[1:]

def print_captions():
    print("# Z k*c kG")
    print("# nm kBT/nm kBT")

def transfer_unit__J_per_nm(value):
    '''
    type_value: float
    r_type: float
    '''
    bar_nm2__in__J_per_nm = 1.0e-22 # atm*A^2 = 1.01325e-24 J/nm
    bar_nm3__in__J = 1.0e-22 # atm*A^3 = 1.01325e-25 J

    return value * bar_nm2__in__J_per_nm

def transfer_unit(value):
    J__in__kBT = 1.0 / (kB*310.0) # kB*Troom = 4.0453e-21 J (Troom=293 K)

    return transfer_unit__J_per_nm(value) * J__in__kBT

def main(args):
    inFile = args[0]
    print("# Calculated from %s" % inFile)
    with open(inFile) as f:
        lines = f.readlines()

    coords_neg = []
    lpp_neg = []
    coords_pos = []
    lpp_pos = []
    for line in lines:
        if line[0] in ['#', '@',]:
            continue
        words = line.split()
        coord = float(words[0])
        if coord < 0.0:
            coords_neg.append(coord)
            lpp_neg.append(float(words[1]))
        else:
            coords_pos.append(coord)
            lpp_pos.append(float(words[1]))
    delta_neg = [x for x in np.diff(coords_neg)] + [abs(coords_neg[-1])]
    delta_pos = [coords_pos[0]] + [x for x in np.diff(coords_pos)]

    screen_msg = ''

    tau1_sum = 0.0
    tau2_sum = 0.0
    tau1_neg = []
    tau2_neg = []
    for z, p, d in reversed(zip(coords_neg, lpp_neg, delta_neg)):
        tau1_sum += abs(z) * p * d
        tau2_sum += z**2 * p * d
        tau1_neg.append(tau1_sum)
        tau2_neg.append(tau2_sum)
    screen_msg += ("## Negative monolayer results: \n"
                   "# tau1 = %s kBT/nm = %s J/nm\n"
                   "# tau2 = %s kBT\n"
                   %(transfer_unit(tau1_sum), transfer_unit__J_per_nm(tau1_sum),
                     tau2_sum,
                   )
    )

    tau1_sum = 0.0
    tau2_sum = 0.0
    tau1_pos = []
    tau2_pos = []
    for z, p, d in zip(coords_pos, lpp_pos, delta_pos):
        tau1_sum += abs(z) * p * d
        tau2_sum += z**2 * p * d
        tau1_pos.append(tau1_sum)
        tau2_pos.append(tau2_sum)
    screen_msg += ("## Positive monolayer results: \n"
                   "# tau1 = %s kBT/nm = %s J/nm\n"
                   "# tau2 = %s kBT\n"
                   %(transfer_unit(tau1_sum), transfer_unit__J_per_nm(tau1_sum),
                     tau2_sum,
                   )
    )

    print_captions()
    print(screen_msg)
    tau1_neg.reverse()
    tau2_neg.reverse()
    for z, t1, t2 in zip(coords_neg + coords_pos,
                         tau1_neg + tau1_pos,
                         tau2_neg + tau2_pos):
        print(z, t1, t2)
    print(screen_msg, file=sys.stderr)

if __name__ == '__main__':
    arguments = gate_keeping()
    main(arguments)
