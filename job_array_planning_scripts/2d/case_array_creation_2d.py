"""script for creating job array for wake capture 2d fundamental motion"""

import os
import shutil

template_dir = 'templates'
kinematic_data_dir = '2d_kinematic_cases'
out_job_array_dir = 'wake_capture_2d_job_pack'
#-------------------------------------------------
cwd = os.getcwd()
template_dir_path = os.path.join(cwd, template_dir)
kinematic_data_dir_path = os.path.join(cwd, kinematic_data_dir)
output_folder = os.path.join(cwd, out_job_array_dir)

if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.mkdir(output_folder)

job_batch_file_src = os.path.join(template_dir_path, 'all_current_jobs.sh')
job_batch_file_dist = os.path.join(output_folder, 'all_current_jobs.sh')
shutil.copyfile(job_batch_file_src, job_batch_file_dist)
#-------------------------------------------------
case_names = [
    f.name.split('.dat')[0] for f in os.scandir(kinematic_data_dir_path)
    if f.is_file() and f.name.endswith('.dat')
]

for case in case_names:
    template_case = 'case_template'
    template_folder = os.path.join(template_dir_path, template_case)
    case_folder = os.path.join(output_folder, case)
    shutil.copytree(template_folder, case_folder)

    case_kinematic_data = os.path.join(kinematic_data_dir_path, case + '.dat')
    case_kinematic_image = os.path.join(kinematic_data_dir_path, case + '.png')
    case_cf_file = os.path.join(kinematic_data_dir_path, case + '.cf')
    case_nu_file = os.path.join(kinematic_data_dir_path, case + '.nu')

    kinematic_data_dist = os.path.join(case_folder, 'backGround', 'constant',
                                       '6DoF_2d.dat')
    kinematic_image_dist = os.path.join(case_folder, 'kinematics_plot.png')
    cf_dist = os.path.join(case_folder, 'backGround', 'system',
                           'FOforceCoefficients')
    nu_dist = os.path.join(case_folder, 'backGround', 'constant',
                           'transportProperties')

    shutil.copyfile(case_kinematic_data, kinematic_data_dist)
    shutil.copyfile(case_kinematic_image, kinematic_image_dist)
    shutil.copyfile(case_cf_file, cf_dist)
    shutil.copyfile(case_nu_file, nu_dist)
