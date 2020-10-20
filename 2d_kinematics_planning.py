"""script for 2d kinematics planning for fundamental cases"""

import numpy as np

Re = [100, 1000, 10000]
stroke_dist = [3, 5, 7, 9]
acc_time_fraction = [0.125, 0.25, 0.5]  #-include both acc and decc dist-
pitch_time_fraction = [0.125, 0.25, 0.5]
#---------------------------------------
wing_chord = 1
stroke_time = 1
pitch_angle = 90
pitch_acc_time_fraction = 0.25
#--------------------------------------
with open('2d_case_parameters.csv', 'w') as f:
    f.write('wing_chord = %s (m)\n' % str(wing_chord))
    f.write('stroke_time = %s (m)\n' % str(stroke_time))
    f.write('pitch_angle = %s (deg)\n' % str(pitch_angle))
    f.write('pitch_acc_time_fraction = %s\n' % str(pitch_acc_time_fraction))
    f.write(
        '%s\n' %
        r'Re, stroke_dist, acc_time_fraction, pitch_time_fraction, acc_t (s), steady_t (s), pitch_t (s), nu (m^2/s), acc (m/s^2), pitch_acc (deg/s^2), steady_velocity (m/s), acc_dist (chords), steady_dist (chords), pitch_dist (chords), c_U (s)'
    )
#--------------------------------------
for Rei in Re:
    for strokei in stroke_dist:
        for acc_tf in acc_time_fraction:
            acc_t = acc_tf * stroke_time / 2
            for pitch_tfi in pitch_time_fraction:
                steady_t = stroke_time - 2 * acc_t
                pitch_t = pitch_tfi * stroke_time
                steady_velocity = strokei * wing_chord / (1 - acc_t)
                #-------------------------
                c_U = wing_chord / steady_velocity
                acc = steady_velocity / acc_t
                pitch_avel = pitch_angle / (
                    (1 - 0.5 * pitch_acc_time_fraction) * pitch_t)

                #--travel distance calculation--
                acc_dist = (steady_velocity / 2 * acc_t) / wing_chord
                steady_dist = steady_velocity * steady_t / wing_chord
                if pitch_t <= acc_t:
                    pitch_dist = 0.5 * acc * pitch_t**2
                else:
                    pitch_dist = acc_dist
                    pitch_dist += (pitch_t - acc_t) * steady_velocity
                pitch_dist = pitch_dist / wing_chord
                #-------------------------------

                pitch_acc = pitch_avel / (0.5 * pitch_acc_time_fraction *
                                          pitch_t)
                nu = steady_velocity * wing_chord / Rei
                parameters = [
                    Rei, strokei, acc_tf, pitch_tfi, acc_t, steady_t, pitch_t,
                    nu, acc, pitch_acc, steady_velocity, acc_dist, steady_dist,
                    pitch_dist, c_U
                ]
                parameters = [str(x) for x in parameters]

                with open('2d_case_parameters.csv', 'a') as f:
                    f.write('%s\n' % ', '.join(parameters))
