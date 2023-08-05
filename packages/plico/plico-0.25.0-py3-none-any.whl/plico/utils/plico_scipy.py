#!/usr/bin/env python

import threading
lock = threading.Lock()


def minimize(*args, **kwargs):
    with lock:
        import lmfit
        return lmfit.minimize(*args, **kwargs)


def leastsq(*args, **kwargs):
    with lock:
        import scipy.optimize
        return scipy.optimize.leastsq(*args, **kwargs)


def medfilt2d(*args, **kwargs):
    with lock:
        import scipy.signal
        return scipy.signal.medfilt2d(*args, **kwargs)


def median_filter(*args, **kwargs):
    with lock:
        import scipy.ndimage.filters
        return scipy.ndimage.filters.median_filter(*args, **kwargs)


def splrep(*args, **kwargs):
    with lock:
        import scipy.interpolate
        return scipy.interpolate.splrep(*args, **kwargs)


def splev(*args, **kwargs):
    with lock:
        import scipy.interpolate
        return scipy.interpolate.splev(*args, **kwargs)


def curve_fit(*args, **kwargs):
    with lock:
        import scipy.optimize
        return scipy.optimize.curve_fit(*args, **kwargs)


def rotate(*args, **kwargs):
    with lock:
        import scipy.ndimage.interpolation
        return scipy.ndimage.interpolation.rotate(*args, **kwargs)


def pinv2(*args, **kwargs):
    with lock:
        import scipy.linalg
        return scipy.linalg.pinv2(*args, **kwargs)


def pinv(*args, **kwargs):
    with lock:
        import scipy.linalg
        return scipy.linalg.pinv(*args, **kwargs)


def gaussian_filter(*args, **kwargs):
    with lock:
        import scipy.ndimage.filters
        return scipy.ndimage.filters.gaussian_filter(*args, **kwargs)


def svdvals(*args, **kwargs):
    with lock:
        import scipy.linalg
        return scipy.linalg.svdvals(*args, **kwargs)


def binom(*args, **kwargs):
    with lock:
        import scipy.special
        return scipy.special.binom(*args, **kwargs)
