"""functions for generating shape and calculating wing planform parameters"""

import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.interpolate import UnivariateSpline


def beta_wing_planform(T_c, AR, T, r1_hat, y_off_set, x_off_set, n):
    """beta wing planform function"""
    c_bar = T / T_c
    R = AR * c_bar
    yr = y_off_set * R
    xr = x_off_set * c_bar
    R_total = R + yr

    r2_hat = 0.929 * (r1_hat**0.732)
    p = r1_hat * (((r1_hat * (1 - r1_hat)) / ((r2_hat**2) - (r1_hat**2))) - 1)
    q = (1 - r1_hat) * (((r1_hat * (1 - r1_hat)) / ((r2_hat**2) -
                                                    (r1_hat**2))) - 1)
    B = integrate.quad(lambda x: x**(p - 1) * ((1 - x)**(q - 1)), 0, 1)[0]
    dr = R / n

    r = np.zeros(n + 1)
    r_hat = np.zeros(n + 1)
    c_hat = np.zeros(n + 1)
    c = np.zeros(n + 1)
    y_LE = np.zeros(n + 1)
    y_TE = np.zeros(n + 1)
    x_LE = np.zeros(n + 1)
    x_TE = np.zeros(n + 1)
    for i in range(n + 1):
        r[i] = i * dr
        r_hat[i] = r[i] / R
        c_hat[i] = ((r_hat[i]**(p - 1)) * ((1 - r_hat[i])**(q - 1))) / B
        if r_hat[i] <= 0.5 and c_hat[i] <= 0.2:
            c_hat[i] = 0.2
        c[i] = c_hat[i] * c_bar
        y_LE[i] = yr + r[i]
        y_TE[i] = yr + r[i]
        x_LE[i] = xr + 0.25 * c[i]
        x_TE[i] = xr - 0.75 * c[i]

    r = np.array(r)
    c = np.array(c)
    LE = np.array([[x, y] for x, y in zip(x_LE, y_LE)])
    TE = np.array([[x, y] for x, y in zip(x_TE, y_TE)])

    return R, R_total, r, c, LE, TE


def wshape_plotter(wing_profile, save_file):
    """
    function to plot wing shape

    """
    cwd = os.getcwd()
    wing_profile = np.array(wing_profile) * 1000
    l_width = 3

    fig, ax = plt.subplots(1, 1)

    ax.plot(wing_profile[:, 1],
            wing_profile[:, 0],
            linestyle='solid',
            linewidth=l_width,
            label=r'wing profile')

    ax.set_xlabel('y (mm)')
    ax.set_ylabel('x (mm)')
    ax.set_title('wing planform plot')
    ax.legend()

    if save_file == 'current':
        out_figure_file = os.path.join(cwd, 'wing_planform_plot.png')
        fig.savefig(out_figure_file)
        plt.show()
    else:
        fig.savefig(save_file)
        plt.close()

    return fig


def radius_locations(LE, TE):
    """calculate charateristic radius given LE and TE point arrays"""
    r_0 = max(-np.amax(-LE[:, 1]), -np.amax(-TE[:, 1]))
    r_end = min(np.amax(LE[:, 1]), np.amax(TE[:, 1]))
    R = r_end
    # print(r_end)

    LEspl = UnivariateSpline(LE[:, 1], LE[:, 0], s=0)
    TEspl = UnivariateSpline(TE[:, 1], TE[:, 0], s=0)

    def r_c_function(r):
        if r <= r_0:
            c = 0
        else:
            c = np.abs(LEspl(r) - TEspl(r))
        return c

    r_array = np.linspace(r_0, r_end, 200)
    c_array = []
    s1 = []
    s2 = []
    s3 = []
    for ri in r_array:
        c_array.append(r_c_function(ri))
        s1.append(ri * r_c_function(ri))
        s2.append(ri**2 * r_c_function(ri))
        s3.append(ri**3 * r_c_function(ri))

    S0 = integrate.simps(c_array, r_array)
    S1 = integrate.simps(s1, r_array)
    S2 = integrate.simps(s2, r_array)
    S3 = integrate.simps(s3, r_array)

    S = S0
    r1_hat = S1 / (S0 * R)
    r2_hat = (S2 / (S0 * R**2))**(1 / 2)
    r3_hat = (S3 / (S0 * R**3))**(1 / 3)

    return S, r1_hat, r2_hat, r3_hat


def force_estimate(R, S, Re, phi, r2_hat, r3_hat, medium):
    """estimate maximum forces for flapping wings"""
    if medium == 'water':
        rho = 999.7
        nu = 1.3065e-6
    elif medium == 'air':
        rho = 1.246
        nu = 1.426e-5

    phi = phi * np.pi / 180
    pitch_angle = np.pi / 2

    c_bar = S / R
    ref_vel = Re * nu / c_bar
    max_vel = ref_vel * np.pi / 2
    frequency = max_vel / (phi / 2 * 2 * np.pi * R * r2_hat)

    max_acc = max_vel * 2 * np.pi * frequency
    max_pitch_omega = 2 * np.pi * frequency * pitch_angle / 2
    # max_pitch_acc = 2 * np.pi * frequency * max_pitch_omega

    cf_t = 3.4
    cf_r = 1.6
    force_t = 0.5 * rho * ref_vel**2 * cf_t * S
    force_r = cf_r * rho * (0.5 * max_vel) * max_pitch_omega * c_bar**2 * R
    force_a = np.pi / 4 * c_bar**2 * rho * R * max_acc

    max_force = force_t + force_r + force_a
    max_moment = max_force * r3_hat * R

    return frequency, nu, ref_vel, max_force, max_moment
