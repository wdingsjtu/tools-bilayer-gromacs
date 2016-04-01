#!/bin/bash
#
#    memgro.sh
#
# Created: 29/Mar/2016
# Updated: 01/Apr/2016
#

TOOLS_PATH="/home/weiding/WORK/Simulation/membraneGRO/tools"

if [[ $# -eq 0 ]]; then
  printf "Gromacs-Bilayer Toolkit (wding.sjtu@gmail.com)\n"
  printf "\n"
  printf "Usage: memgro [Tool]\n"
  exit 0
fi

${TOOLS_PATH}/$*

