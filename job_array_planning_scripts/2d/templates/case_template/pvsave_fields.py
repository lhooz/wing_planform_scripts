# trace generated using paraview version 5.7.0
#
#### import the simple module from the paraview
import os
import shutil
from paraview.simple import *

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

cwd = os.getcwd()

pvstate_file = os.path.join(cwd, 'backGround', 'paraview', 'twoD_fields.pvsm')
case_dir = os.path.join(cwd, 'backGround')
foam_file = os.path.join(case_dir, 'open.foam')
vorz_output_folder = os.path.join(cwd, 'vorz_data')
qctr_output_folder = os.path.join(cwd, 'q_data')
ufield_output_folder = os.path.join(cwd, 'ufield_data')
geop_output_folder = os.path.join(cwd, 'geop_data')

if os.path.exists(vorz_output_folder):
    shutil.rmtree(vorz_output_folder)
os.mkdir(vorz_output_folder)

if os.path.exists(qctr_output_folder):
    shutil.rmtree(qctr_output_folder)
os.mkdir(qctr_output_folder)

if os.path.exists(ufield_output_folder):
    shutil.rmtree(ufield_output_folder)
os.mkdir(ufield_output_folder)

if os.path.exists(geop_output_folder):
    shutil.rmtree(geop_output_folder)
os.mkdir(geop_output_folder)

vorz_output_files = os.path.join(vorz_output_folder, 'vorz.csv')
qctr_output_files = os.path.join(qctr_output_folder, 'q.csv')
ufield_output_files = os.path.join(ufield_output_folder, 'ufield.csv')
geop_output_files = os.path.join(geop_output_folder, 'geop.csv')

# load state
LoadState(pvstate_file,
          LoadStateDataFileOptions='Choose File Names',
          openfoamFileName=foam_file,
          openfoam1FileName=foam_file)

# get animation scene
# animationScene1 = GetAnimationScene()

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# find view
# renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')

# set active view
# SetActiveView(renderView1)

# find source
vorZ = FindSource('VorZ')

# set active source
SetActiveSource(vorZ)

# save data
SaveData(vorz_output_files,
         proxy=vorZ,
         WriteTimeSteps=1,
         Filenamesuffix='_%.4d',
         Precision=10,
         UseScientificNotation=1)

# change to Q criterion data
q_criterion = FindSource('Q')
SetActiveSource(q_criterion)

# save data
SaveData(qctr_output_files,
         proxy=q_criterion,
         WriteTimeSteps=1,
         Filenamesuffix='_%.4d',
         Precision=10,
         UseScientificNotation=1)

# change to velocity field criterion data
uField = FindSource('UField')
SetActiveSource(uField)

# save data
SaveData(ufield_output_files,
         proxy=uField,
         WriteTimeSteps=1,
         Filenamesuffix='_%.4d',
         Precision=10,
         UseScientificNotation=1)

# change to wing geometry and pressure data
geometry_P = FindSource('Geometry_P')
SetActiveSource(geometry_P)

# save data
SaveData(geop_output_files,
         proxy=geometry_P,
         WriteTimeSteps=1,
         Filenamesuffix='_%.4d',
         Precision=10,
         UseScientificNotation=1)
