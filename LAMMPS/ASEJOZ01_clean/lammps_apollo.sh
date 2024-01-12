#!/bin/bash -l

#PBS -N ASEJOZ01_clean
#PBS -l nodes=c15:ppn=8
#PBS -l walltime=50:00:00
#PBS -l mem=16GB
#PBS -r y
#PBS -j oe
#PBS -V

filename="ASEJOZ01_clean"

#export LAM='/home/yue/lammps-2Aug2023/src/lmp_mpi'

module load lammps/2Aug2023
cd $PBS_O_WORKDIR
export OMP_NUM_THREADS=1

mpirun -np 8 lmp_mpi -in in.${filename} > log.${filename} 1>SCREEN.txt 2>&1


### Automatically analyze the results
environment="lammps"
scriptname="readMeanVol"

module load miniconda
bash
. ~/.bashrc

echo "********************************************"
echo "Input file is ${filename} Running, Output file is ${filename}.out"
conda activate $environment
python3 ${scriptname}.py > ${scriptname}.out
echo "********************************************"

mkdir dump
mv *log* dump
mv *.txt dump
mv *.out dump
mkdir input 
mv data.* in.* input