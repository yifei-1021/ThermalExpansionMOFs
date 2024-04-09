#!/bin/bash

for i in ./* # iterate over all files in current dir
do
    if [[ -d "$i" && $i != './IOscripts' ]] # if it's a directory
    then
        echo "**************************************************************************"\
        ls $i
        echo "Submitting JOB @ ${i}"
        cd $i
        qsub ./lammps*.sh
        cd ..
    fi
done

for i in $( seq 0 10 1000 ); 
do 
  sleep $i
  echo "Status after ${i} seconds"
  qstat
done
