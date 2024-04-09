#!/bin/bash

for i in ./* 
do
    if [[ -d "$i" && $i != './IO' ]] # if it's a directory
    then
      echo "Setting up folder $i"
      cp -r ./IO $i
      cp *sh $i
      cp *py $i
      cd $i
      mv data* ./IO
      mv in* ./IO
      cd ..
    fi
done