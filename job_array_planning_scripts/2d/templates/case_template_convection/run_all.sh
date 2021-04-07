#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

foamCleanTutorials

cd wing
runApplication blockMesh
runApplication surfaceFeatureExtract
cp -f system/decomposeParDict.hierarchical system/decomposeParDict
decomposePar
cp -f system/decomposeParDict.ptscotch system/decomposeParDict
runParallel snappyHexMesh -overwrite
runParallel extrudeMesh
runParallel transformPoints -rollPitchYaw '(0 0 45)'
runApplication reconstructParMesh -constant -latestTime -mergeTol 1e-6
cd ..

cd backGround
runApplication blockMesh
runApplication transformPoints -translate '(-3 0 0)'
runApplication mergeMeshes . ../wing -overwrite

checkMesh
runApplication topoSet
runApplication setFields
runApplication checkMesh

touch open.foam
cd ..

cd backGround
runApplication decomposePar
restore0Dir -processor
runParallel overPimpleDyMFoam
cd ..
