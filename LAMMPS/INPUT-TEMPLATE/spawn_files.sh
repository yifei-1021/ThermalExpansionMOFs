#!/bin/bash
clear
### Purge first
#mv data* IO/
#mv in* IO/
for i in ./IO/data.* 
do
      ### Spawn directory from data. file
      IFS='/' read -ra split <<< "$i"
      folder=${split[-1]}
      folder=${folder:5}
      echo "Making $folder"
      mkdir ./$folder
      cp $i ./$folder
      
      ### merge inputfile with head and tail
      IN_FILE=in.${folder}
      echo $IN_FILE
      cd IO
      python3 merge_all.py --inScriptName $IN_FILE --outfolder ../$folder
      cd ..
done

# iterate over all files in current dir
# Copy in.* data.* to folder

####NOTE DATA FILE NEED TO BE INPUT INDEPENDENTLY
TotalJobs=0

serialJobs=0
shortJobs=0
q12Jobs=0
q20Jobs=0
q24Jobs=0

for i in ./* 
do
    if [[ -d "$i" && $i != './IO' ]] # if it's a directory
    then
        echo ""
        echo "Copying lammps.sh, in.*, data.* files to folder $i"
        cp lammps*sh $i
        cp read*.py "$i" 

        cd $i
        ### RENAME JOB NAME in lammps.sh
        MOF=$( pwd )
        IFS='/' read -ra split <<< "$MOF"
        MOF=${split[-1]}
        JobName="${MOF}"

        dataFile="data.$MOF"
        dataSize=$( du -shk $dataFile | tr -d -c 0-9 )
        #dataSize=$( "$dataSize" | awk '{print $1}' )

        
        
        sed -i s/dummy/$JobName/g ./*lammps*.sh
        TotalJobs=$(( $TotalJobs+1 ))
        cd ..
    fi
done

echo "Serial Jobs: $serialJobs / $TotalJobs"
echo "Short Jobs: $shortJobs / $TotalJobs"
echo "Q12 Jobs: $q12Jobs / $TotalJobs"
echo "Q20 Jobs: $q20Jobs / $TotalJobs"
echo "Q24 Jobs: $q24Jobs / $TotalJobs"