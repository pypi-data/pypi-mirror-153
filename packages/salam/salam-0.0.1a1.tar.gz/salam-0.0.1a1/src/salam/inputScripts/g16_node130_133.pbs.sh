#!/bin/bash
#PBS -N  test0009
#PBS -q  batch
#PBS -j  oe
#PBS -l  walltime=3000:00:00
#PBS -l  nodes=1:ppn=8
##P#B#S -l  nodes=node131:ppn=16

INPUT_FILE=xxx.com

##environment###
g16root="/home/tucy/software"
GAUSS_SCRDIR="/home/tucy/tmp/Gaussian16"
GAUSS_EXEDIR=$g16root/g16
export g16root GAUSS_SCRDIR GAUSS_EXEDIR
. $g16root/g16/bsd/g16.profile
######
ulimit -s unlimited
ulimit -n 10000

echo "This script pid is $$"
echo "Working directory is $PBS_O_WORKDIR"
cd   $PBS_O_WORKDIR
echo "Runing on host `hostname`"
echo "Time is `date`"
echo Directory is `pwd`
echo "This jobs runs on the following processors:"
echo `cat $PBS_NODEFILE`
NPROCS=`wc -l < $PBS_NODEFILE`
echo "This job has allocated $NPROCS cpucores."

g16  ${INPUT_FILE%.com}.com


if test -f  "$PBS_O_WORKDIR/fort.7"
then
#    mv  "$PBS_O_WORKDIR/fort.7"    "$PBS_O_WORKDIR/${INPUT_FILE%.com}.fort.7"   2>/dev/null 
	rm -f   $PBS_O_WORKDIR/fort.7  2>/dev/null 
fi


echo `date`
