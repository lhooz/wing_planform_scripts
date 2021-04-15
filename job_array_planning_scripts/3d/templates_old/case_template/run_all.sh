#!/bin/bash

foamCleanTutorials

cd wing
surfaceFeatureExtract
blockMesh
snappyHexMesh -overwrite | tee log.snappyHexMesh
cd ..

cd backGround
blockMesh
mergeMeshes . ../wing -overwrite
createPatch -overwrite
topoSet
topoSet -dict system/topoSetDict_movingZone

rm -r 0
cp -r 0_org 0

checkMesh |  tee log.checkMesh

cd ..
cd backGround

decomposePar
mpirun -np $NSLOTS renumberMesh -overwrite -parallel | tee log.renumberMesh
mpirun -np $NSLOTS pimpleFoam -parallel | tee log.solver
touch open.foam

cd ..
