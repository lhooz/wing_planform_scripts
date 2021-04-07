#!/bin/bash
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions
cd backGround
#runParallel splitMeshRegions -cellZones -overwrite
runParallel postProcess -funcs '(vorticity Q)'
cd ..
