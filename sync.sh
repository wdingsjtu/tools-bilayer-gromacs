#!/bin/bash

# Purpose: Sync "membraneGro" simulations in the current folder from the
#          remote machine.
# Syntex:  ./sync.sh *
# Created: 2016/Mar/04

if [ $# -lt 1 ]; then                      
  echo "Syntax: $ sync.sh remoteFile"
  exit 0
elif [ $# -gt 1 ]; then 
  echo "Warning: Be careful about wildcard" 
fi

while true; do 
  echo "Download \"$@\"?(y/n)"
  read is_continue
  if [ ! ${is_continue} ]; then
    continue
  elif [ ${is_continue} == 'y' ]; then
    break
  elif [ ${is_continue} == 'n' ]; then
    exit 0
  fi
done

#
LOCAL_ROOT="/home/weiding/WORK/Simulation/membraneGRO/"
REMOTE_ROOT="/work/e280/e280/ganesh/wding_jobs/membraneGRO/"

if [[ $PWD =~ ^${LOCAL_ROOT} ]]; then
  targetPath=${PWD##${LOCAL_ROOT}}
else
  printf "This only works under the correct root path:\n"
  printf ${LOCAL_ROOT}"\n"
  exit 0
fi

scp ${ARCHERHOME}:${REMOTE_ROOT}${targetPath}/"${1}" .

echo "${ARCHERHOME}:${REMOTE_ROOT}${targetPath}/${1}"
