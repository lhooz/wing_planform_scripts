#!/bin/bash --login

#$ -pe smp.pe 8
#$ -cwd

#$ -m bea
#$ -M hao.lee0019@yahoo.com

#$ -t 1-4
mkdir ./SIM_RESULTS
mkdir ./FIELD_RESULTS
readarray -t JOB_DIRS < <(find . -mindepth 1 -maxdepth 1 -name '*Re*' -printf '%P\n')

module load apps/gcc/openfoam/v1906
module load apps/binapps/paraview/5.7.0
source $foamDotFile

TID=$[SGE_TASK_ID-1]
JOBDIR=${JOB_DIRS[$TID]}

cd $JOBDIR
echo "Running SGE_TASK_ID $SGE_TASK_ID in directory $JOBDIR"
sh run_all.sh
cd ..
cp $JOBDIR/backGround/postProcessing/forceCoeffs_object/0/coefficient.dat ./SIM_RESULTS/$JOBDIR

cd $JOBDIR
sh pvpost.sh
mpiexec -n $NSLOTS pvbatch pvsave_fields.py | tee log.pvpost
cd ..
mkdir ./FIELD_RESULTS/$JOBDIR
cp -r $JOBDIR/vorz_data ./FIELD_RESULTS/$JOBDIR
cp -r $JOBDIR/q_data ./FIELD_RESULTS/$JOBDIR
cp -r $JOBDIR/ufield_data ./FIELD_RESULTS/$JOBDIR
cp -r $JOBDIR/geop_data ./FIELD_RESULTS/$JOBDIR
