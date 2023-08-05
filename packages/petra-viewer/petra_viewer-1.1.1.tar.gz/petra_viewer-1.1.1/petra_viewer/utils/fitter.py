# Created by matveyev at 15.02.2021

import numpy as np
import scipy
import scipy.optimize
import scipy.signal


# ----------------------------------------------------------------------
def make_fit(x, y, name="linear"):
    funmap = {
        "linear": linear_fit,
        "gaussian": gaussian_fit,
        "lorentzian": lorentzian_fit,
        "step": step_fit, # more?
        "fwhm": fwhm  # more?
    }

    return funmap[name.lower()](x, y)


# ----------------------------------------------------------------------
def fwhm(x, y):
    y_half = (np.max(y) + np.min(y)) * 0.5
    above_half = np.where(y > y_half)

    x_min, x_max = above_half[0][0], above_half[0][-1]
    fwhm = np.fabs(x[x_max] - x[x_min])
    cfwhm = 0.5 * (x[x_min] + x[x_max])
    x_center = np.argmin(np.abs(x - cfwhm))

    print(fwhm, cfwhm)

    y_fit = np.min(y) + (y[x_min] - np.min(y)) * (scipy.signal.unit_impulse(len(x), x_min)) + \
                        (y[x_max] - np.min(y)) * (scipy.signal.unit_impulse(len(x), x_max)) + \
                        (y[x_center] - np.min(y)) * (scipy.signal.unit_impulse(len(x), x_center))


    msg = "FWHM = {:.3e}, Center={:.3e}".format(fwhm, cfwhm)

    return y_fit, msg, [cfwhm]


# ----------------------------------------------------------------------
def step_fit(x, y):

    y_min = np.min(y)
    y = y - y_min

    min = 0
    max = np.max(y)
    center = np.mean(x)
    slope = np.sign(y[-1]-y[0])*10*max/(np.max(x) - np.min(x))

    def _step(x, min, max, center, slope):
        slopeFunct = (max+min)/2 + (x-center) * slope
        return np.minimum(np.maximum(min * np.ones_like(x), slopeFunct), max * np.ones_like(x))

    popt, pcov = scipy.optimize.curve_fit(_step, x, y, [min, max, center, slope])

    y_fit = y_min + _step(x, *popt)
    msg = "Center={:.3e}".format(popt[2])

    return y_fit, msg, [popt[2]]


# ----------------------------------------------------------------------
def linear_fit(x, y):

    popt = scipy.polyfit(x, y, 1)
    y_fit = x * popt[0] + popt[1]
    msg = "{:.3e} * x + {:.3e}".format(popt[0], popt[1])
    return y_fit, msg, None


# ----------------------------------------------------------------------
def gaussian_fit(x, y):

    norm = (max(y) - min(y)) * 0.4
    mean = min(x) + (max(x) - min(x)) * 0.5
    sigma = (max(x) - min(x)) * 0.4
    sh = min(y)

    print("initial guess:", norm, mean, sigma, sh)

    def _gauss(x, norm, mean, sigma, sh=0.0):
        return norm * np.exp(-(x - mean)**2 / sigma**2) + sh

    popt, pcov = scipy.optimize.curve_fit(_gauss, x, y, [norm, mean, sigma, sh])        # try levmar instead?
    print("optimized params:", popt)

    y_fit = _gauss(x, *popt[:4])
    msg = "Center = {:.3e}, <font>&sigma;<sup>2</sup></font>={:.3e} (G)".format(popt[3], popt[2] ** 2)
    return y_fit, msg, [popt[1], popt[2] ** 2]


# ----------------------------------------------------------------------
def lorentzian_fit(x, y):

    # initial params guess
    norm = (max(y) - min(y)) * 0.4
    x0 = min(x) + (max(x) - min(x)) * 0.5
    gamma = (max(x) - min(x)) * 0.5

    def _lorentz(x, norm, x0, gamma):
        return norm * gamma / (2 * np.pi * ((x - x0) ** 2 + (gamma * 0.5) ** 2))

    popt, pcov = scipy.optimize.curve_fit(_lorentz, x, y, [norm, x0, gamma])

    y_fit = _lorentz(x, *popt[:3])
    msg = "Center= {:.3e},  FWHM={:.3e} (L)".format(popt[1], popt[2])
    return y_fit, msg, [popt[1], popt[2]]