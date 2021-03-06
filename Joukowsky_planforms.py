"""main script for wing planform creation and parameter estimation"""

import os
import shutil
from planform_functions import beta_wing_planform, radius_locations, force_estimate, wshape_plotter
import numpy as np

T_c = 0.05
T = 3
phi = 160
# medium_or_frequency = 'water' #--used for exp cases--
medium_or_frequency = 1  #--used for cfd cases--

Reynolds_no = [1000]
# AR = [3.0]
# r1_hat = [0.5]
# y_off_set = [0.0]
AR = [
    2.02 / 0.67, 13.2 / 4.02, 51.9 / 18.26, 9.8 / 3.08, 12.7 / 2.38, 9.3 / 2.2,
    11.4 / 3.19, 11.2 / 3.23
]
r1_hat = [0.55, 0.49, 0.46, 0.5, 0.56, 0.52, 0.48, 0.47]
y_off_set = [0.0]

x_off_set = [0.0]

out_profile_folder = 'wing_profiles'
out_image_folder = 'wing_profile_images'
#-------------------------------------------
cwd = os.getcwd()
out_profile_path = os.path.join(cwd, out_profile_folder)
out_image_path = os.path.join(cwd, out_image_folder)
if os.path.exists(out_profile_path):
    shutil.rmtree(out_profile_path)
if os.path.exists(out_image_path):
    shutil.rmtree(out_image_path)
os.mkdir(out_profile_path)
os.mkdir(out_image_path)
#-------------------------------------------
with open('wplanform_data.csv', 'w') as f:
    f.write('%s%s\n' % (r't/c = ', str(T_c)))
    f.write('%s%s%s\n' % ('Thickness = ', str(T), ' mm'))
    f.write('%s%s%s\n' % ('flapping amplitude = ', str(phi), ' degree'))
    f.write('%s%s\n' % ('Medium_or_frequency = ', str(medium_or_frequency)))
    f.write(
        '%s\n' %
        r'Re, aspect_ratio, root_offset, r1_h_design, r1_hat, r2_hat, r3_hat, R (mm), R_total (mm), flapping_frequency (Hz), kinematic_viscosity (m^2/s), S (m^2), ref_vel_Ur2 (m/s), max.force (N), max.moment (Nmm)'
    )
#------mm to m-----
T = T / 1000
#------------------
for Re in Reynolds_no:
    for ar, r1 in zip(AR, r1_hat):
        for y_off in y_off_set:
            for x_off in x_off_set:
                R, c_bar, r, c, LE, TE = beta_wing_planform(
                    T_c, ar, T, r1, y_off, x_off, 1000)
                R_total, S, r1_out, r2_out, r3_out = radius_locations(LE, TE)
                frequency, nu, ref_vel, F, M = force_estimate(
                    R_total, c_bar, S, Re, phi, r2_out, r3_out,
                    medium_or_frequency)
                parameters_mm = [
                    Re, ar, y_off, r1, r1_out, r2_out, r3_out, R * 1000,
                    R_total * 1000, frequency, nu, S, ref_vel, F, M * 1000
                ]
                parameters_mm = [str(x) for x in parameters_mm]
                with open('wplanform_data.csv', 'a') as f:
                    f.write('%s\n' % ', '.join(parameters_mm))

                #----------------------------------------------------
                profile_name = 'ar' + '{0:.1f}'.format(ar) + '_ofs' + str(
                    y_off) + '_r1h' + str(r1)
                profile_file = os.path.join(out_profile_path,
                                            profile_name + '.csv')
                image_file = os.path.join(out_image_path,
                                          profile_name + '.png')

                wing_profile = np.append(LE, np.flip(TE, axis=0), axis=0)

                wshape_plotter(wing_profile, image_file)

                with open(profile_file, 'w') as f:
                    f.write('x(chord_dir),y(span_dir)\n')
                for co in wing_profile:
                    co_str = [str(x) for x in co]
                    with open(profile_file, 'a') as f:
                        f.write('%s\n' % ','.join(co_str))
