#!/bin/bash

foamCleanTutorials

cd wing
blockMesh
surfaceFeatureExtract
snappyHexMesh -overwrite | tee log.snappyHexMesh
extrudeMesh
transformPoints -rollPitchYaw '(0 0 45)'
cd ..

cd backGround
blockMesh
transformPoints -translate '(-5 0 0)'
mergeMeshes . ../wing -overwrite
topoSet
topoSet -dict system/topoSetDict_movingZone

rm -r 0
cp -r 0_org 0

checkMesh |  tee log.checkMesh
setFields | tee log.setFields

touch open.foam
cd ..

cd backGround
decomposePar
mpirun -np $NSLOTS renumberMesh -overwrite -parallel | tee log.renumberMesh
mpirun -np $NSLOTS overPimpleDyMFoam -parallel | tee log.solver
cd ..
