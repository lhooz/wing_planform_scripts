#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

foamCleanTutorials

cd wing
runApplication surfaceFeatureExtract
runApplication blockMesh
cp -f system/decomposeParDict.hierarchical system/decomposeParDict
decomposePar
cp -f system/decomposeParDict.ptscotch system/decomposeParDict
runParallel snappyHexMesh -overwrite
runApplication reconstructParMesh -constant -latestTime -mergeTol 1e-6
cd ..

cd backGround
runApplication blockMesh
runApplication mergeMeshes . ../wing -overwrite
runApplication createPatch -overwrite
topoSet
topoSet -dict system/topoSetDict_movingZone

restore0Dir
runApplication checkMesh

touch open.foam
cd ..

cd backGround
runApplication decomposePar
runParallel pimpleFoam
cd ..
