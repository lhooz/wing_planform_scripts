"""main script for wing planform creation and parameter estimation"""

from planform_functions import beta_wing_planform, radius_locations, force_estimate

R = 200
T = 3
Re = 10000
phi = 160
medium = 'water'

AR = [2, 3, 4, 5]
y_off_set = [0, 0.1, 0.2]
r1_hat = [0.4, 0.45, 0.5, 0.55, 0.6]

x_off_set = [0.25]

with open('wplanform_data.csv', 'w') as f:
    f.write('%s%s%s\n' % ('R = ', str(R), ' mm'))
    f.write('%s%s%s\n' % ('Thickness = ', str(T), ' mm'))
    f.write('%s%s\n' % ('Re = ', str(Re)))
    f.write('%s%s%s\n' % ('flapping amplitude = ', str(phi), ' degree'))
    f.write('%s%s\n' % ('Medium = ', medium))
    f.write(
        '%s\n' %
        r'aspect_ratio, root_offset, r1_hat, r2_hat, r3_hat, t/c, flapping_frequency (Hz), max.force (N), max.moment (Nmm)'
    )
#------mm to m-----
R = R / 1000
T = T / 1000
#------------------

for ar in AR:
    for y_off in y_off_set:
        for r1 in r1_hat:
            for x_off in x_off_set:
                T_c, r, c, LE, TE = beta_wing_planform(R, ar, T, r1, y_off,
                                                       x_off, 200)
                S, r1_out, r2_out, r3_out = radius_locations(LE, TE)
                frequency, F, M = force_estimate(R, S, Re, phi, r2_out, r3_out,
                                                 medium)
                parameters = [
                    ar, y_off, r1_out, r2_out, r3_out, T_c, frequency, F, M
                ]
                parameters = [str(x) for x in parameters]
                with open('wplanform_data.csv', 'a') as f:
                    f.write('%s\n' % ', '.join(parameters))