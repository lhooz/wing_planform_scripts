#!/bin/bash --login

#$ -pe smp.pe 4 
#$ -cwd

#$ -m bea
#$ -M hao.lee0019@yahoo.com

rm -r SIM_RESULTS
readarray -t JOB_DIRS < <(find . -mindepth 1 -maxdepth 1 -type d -printf '%P\n')
mkdir SIM_RESULTS

#$ -t 1-36

module load apps/gcc/openfoam/v1906
module load apps/binapps/paraview/5.7.0
source $foamDotFile

TID=$[SGE_TASK_ID-1]
JOBDIR=${JOB_DIRS[$TID]}

cd $JOBDIR
echo "Running SGE_TASK_ID $SGE_TASK_ID in directory $JOBDIR"
sh run_all.sh
cd ..
cp $JOBDIR/backGround/postProcessing/forceCoeffs_object/0/coefficient.dat SIM_RESULTS/$JOBDIR
