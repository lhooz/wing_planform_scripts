"""main script for wing planform creation and parameter estimation"""

import os
import shutil
from planform_functions import beta_wing_planform, radius_locations, force_estimate
import numpy as np

T_c = 0.05
T = 3
Re = 10000
phi = 160
medium = 'water'

AR = [2, 3, 4, 5]
y_off_set = [0, 0.1, 0.2]
r1_hat = [0.4, 0.45, 0.5, 0.55, 0.6]

x_off_set = [0.25]

out_profile_folder = 'wing_profiles'
#-------------------------------------------
cwd = os.getcwd()
out_profile_path = os.path.join(cwd, out_profile_folder)
if os.path.exists(out_profile_path):
    shutil.rmtree(out_profile_path)
os.mkdir(out_profile_path)
#-------------------------------------------
with open('wplanform_data.csv', 'w') as f:
    f.write('%s%s\n' % (r't/c = ', str(T_c)))
    f.write('%s%s%s\n' % ('Thickness = ', str(T), ' mm'))
    f.write('%s%s\n' % ('Re = ', str(Re)))
    f.write('%s%s%s\n' % ('flapping amplitude = ', str(phi), ' degree'))
    f.write('%s%s\n' % ('Medium = ', medium))
    f.write(
        '%s\n' %
        r'aspect_ratio, root_offset, r1_hat, r2_hat, r3_hat, R (mm), R_total (mm), flapping_frequency (Hz), max.force (N), max.moment (Nmm)'
    )
#------mm to m-----
T = T / 1000
#------------------

for ar in AR:
    for y_off in y_off_set:
        for r1 in r1_hat:
            for x_off in x_off_set:
                R, R_total, r, c, LE, TE = beta_wing_planform(
                    T_c, ar, T, r1, y_off, x_off, 200)
                S, r1_out, r2_out, r3_out = radius_locations(LE, TE)
                frequency, F, M = force_estimate(R, S, Re, phi, r2_out, r3_out,
                                                 medium)
                parameters_mm = [
                    ar, y_off, r1_out, r2_out, r3_out, R * 1000,
                    R_total * 1000, frequency, F, M * 1000
                ]
                parameters_mm = [str(x) for x in parameters_mm]
                with open('wplanform_data.csv', 'a') as f:
                    f.write('%s\n' % ', '.join(parameters_mm))

                profile_name = 'ar' + str(ar) + '_ofs' + str(
                    y_off) + '_r1h' + str(r1) + '.csv'
                profile_file = os.path.join(out_profile_path, profile_name)
                wing_profile = np.append(LE, np.flip(TE, axis=0),
                                         axis=0) * 1000

                with open(profile_file, 'w') as f:
                    f.write('x(chord_dir), y(span_dir)\n')
                for co in wing_profile:
                    co_str = [str(x) for x in co]
                    with open(profile_file, 'a') as f:
                        f.write('%s\n' % ', '.join(co_str))
