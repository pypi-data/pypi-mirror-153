"""
Functions related to time series analysis.
"""

# from numba import njit
import numpy as np


# noinspection PyShadowingNames
def acorr(a, fft=False):
    r"""
    Compute the lag-:math:`k` autocorrelation :math:`\rho(k)` from dataset :math:`a`.

    .. math :: \rho(k) = \frac{\gamma(k)}{\gamma(0)}

    The function :math:`\gamma` is from :func:`acov`.

    Parameters
    ----------
    a : numpy.ndarray
        One-dimensional array.
    fft : bool
        Should fast Fourier transform be used?

    Returns
    -------
    numpy.ndarray
        Autocorrelation function
    """

    # Compute autocovariance
    gamma = acov(a, fft=fft)
    return gamma / gamma[0]


# noinspection DuplicatedCode,PyShadowingNames
def acov(a, fft=False):
    r"""
    Compute the unbiased auto-covariance function :math:`\gamma(k)` from dataset :math:`a` with :math:`N` samples for
    lag-time :math:`k`.

    .. math :: \gamma(k)=\frac{1}{N-k}\sum_{t=1}^{N-k}(a_t - \mu)(a_{t+k} - \mu)

    Here, we also compute the mean

    .. math :: \mu=\frac{1}{N}\sum_t^Na_t

    Note: by default, all :math:`k` from 0 to N-1 are evaluated. Sampling deteriorates rapidly as :math:`k` increases.
    There is also a *biased* estimator for the autocovariance, which changes the denominator from :math:`n-k` to
    :math:`n` and has an effect of reducing the fluctuations due to error at large :math:`k`. To compute this, see
    :func:`statsmodels.tsa.stattools.acovf`.

    Parameters
    ----------
    a : numpy.ndarray
        1D array.
    fft : bool
        Should Fast-Fourier Transform be used?

    Returns
    -------
    numpy.ndarray
        Autocovariance function

    References
    ----------
    https://www.itl.nist.gov/div898/handbook/eda/section3/autocopl.htm
    """

    # We only want to compute this for 1D arrays
    if a.ndim != 1:
        raise AttributeError('must be 1D')

    # Remove the mean from the observations
    a -= np.mean(a)

    # Compute autocovariance gamma
    if not fft:
        # Compute a * a for all lag times using correlate and the unbiased autocovariance
        len_a = len(a)
        gamma = np.correlate(a, a, mode='full')[(len_a - 1):] / (len_a - np.arange(len_a))

    else:
        # Use statsmodels to compute FFT
        # noinspection PyPackageRequirements
        from statsmodels.tsa.stattools import acovf
        gamma = acovf(a, adjusted=True, demean=False, fft=True, missing='none', nlag=None)

    # Return
    return gamma


# noinspection PyShadowingNames
def inefficiency(a):
    """
    Compute the statistical inefficiency :math:`g` from the equilibration time :math:`\tau_{corr}`.

    .. math :: g = 1 + 2 \tau_{corr}.

    Parameters
    ----------
    a : numpy.ndarray

    Returns
    -------
    float
        Statistical inefficiency.
    """

    return 1. + 2. * tcorr(a)


# Estimate the standard error from the correlation time
# noinspection PyShadowingNames
def sem_tcorr(a, tol=1e-3):
    """
    Estimate of standard error of the mean derived from the correlation time.

    The main assumption is that sqrt(N) ~ sqrt(len(a) / tcorr(a))

    Should only be used for continuous time series data, e.g., from molecular dynamics. Discontinuous trajectories as
    produced by replica exchange or Monte Carlo are not applicable.

    Parameters
    ----------
    a : numpy.ndarray
    tol : float

    Returns
    -------

    """

    return np.std(a) * np.sqrt(tcorr(a) / len(a))


# TODO derive this cleanly
# noinspection PyShadowingNames
def tcorr(a, fft=False):
    r"""
    Compute correlation time :math:`\tau_{corr}` based on the autocorrelation function :math:`\rho(k)`.

    .. math :: \tau_{corr} = \sum_{t=1}^{T} (1 - \frac{t}{T}) \rho_{t}

    Note: only :math:`k` before the first occurrence :math:`\rho(k) = 0` are taken. Estimates after this are
    statistically unreliable.

    Parameters
    ----------
    a : numpy.ndarray
        1D array.
    fft : bool
        Should fast Fourier transform be used?

    Returns
    -------
    float
        Correlation time.

    References
    ----------

    """

    # Compute autocorrelation, reduce to observations before first < 0
    rho_ = acorr(a, fft=fft)[1:]
    rho = rho_[:np.min(np.where(rho_ < 0))]

    t_max = len(a)
    t = np.arange(1, len(rho) + 1)

    return np.sum((1. - t / t_max) * rho)


# noinspection PyShadowingNames
def _acorr(a):
    gamma = _acov(a)
    return gamma / gamma[0]


def _acorr_test(a, decimal=7, plot=True):
    rho0 = acorr(a)
    rho1 = _acorr(a)
    if plot:
        import matplotlib.pyplot as plt
        plt.figure()
        x = np.arange(len(rho0))
        plt.plot(x, rho0)
        plt.plot(x, rho1)
        plt.show()
    np.testing.assert_almost_equal(rho0, rho1, decimal=decimal)


# @njit
def _acov(a):
    n = len(a)
    u = np.mean(a)
    gamma = np.zeros(n)
    for k in range(n):
        gamma[k] = np.mean((a[:n - k] - u) * (a[k:] - u))
    return gamma


def _acov_test(a):
    import time
    start_time = time.time()
    gamma0 = acov(a)
    end_time = time.time()
    print('acov={}'.format(end_time - start_time))

    start_time = time.time()
    gamma1 = acov(a, fft=True)
    end_time = time.time()
    print('acov={}'.format(end_time - start_time))

    start_time = time.time()
    gamma2 = _acov(a)
    end_time = time.time()
    print('acov={}'.format(end_time - start_time))

    np.testing.assert_almost_equal(gamma0, gamma1)
    np.testing.assert_almost_equal(gamma0, gamma2)


if __name__ == '__main__':
    n = 100000
    a = np.random.normal(loc=0, scale=10, size=n)
    print(tcorr(a))
    # _acov_test(a)
    # _acorr_test(a, decimal=5)
    # _tcorr_test(a)

    # print(np.std(a))
    # print(np.sqrt(np.cov(a)))
    # print(np.sqrt(xx - x*x))
    # print(correlation_time(a))
    # print(sem_tcorr(a))

    # import time
    # start_time = time.time()
    # rho = acorr(a)
    # end_time = time.time()
    # print(end_time - start_time)
    # start_time = time.time()
    # tau = tcorr(a)
    # end_time = time.time()
    # print(end_time - start_time)
