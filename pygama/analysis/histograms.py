"""
pygama convenience functions for histograms.
we don't want to create a monolithic class like TH1 in ROOT,
it encourages users to understand what their code is actually doing.
"""
import numpy as np
import matplotlib.pyplot as plt
import pygama.utils as pgu


def get_hist(np_arr, bins=None, range=None, dx=None, wts=None):
    """
    Wrapper for numpy.histogram, with optional weights for each element.
    Note: there are no overflow / underflow bins.
    Available binning methods:
    - Default (no binning arguments) : 100 bins over an auto-detected range
    - bins=N, range=(x_lo, x_hi) : N bins over the specified range (or leave
      range=None for auto-detected range)
    - bins=[str] : use one of np.histogram's automatic binning algorithms
    - bins=bin_edges_array : array lower bin edges, supports non-uniform binning 
    - dx=dx, range=(x_lo, x_hi): bins of width dx over the specified range.
      Note: dx overrides the bins argument!
    """
    if dx is not None:
        bins = int((range[1] - range[0]) / dx)

    if bins is None: 
        bins = 100 #override np.histogram default of just 10

    hist, bins = np.histogram(np_arr, bins=bins, range=range, weights=wts)

    if wts is None:
        return hist, bins, hist
    else:
        var, bins = np.histogram(np_arr, bins=bins, weights=wts*wts)
        return hist, bins, var


def get_fwhm(hist, bin_centers):
    """
    find a FWHM from a hist
    """
    idxs_over_50 = hist > 0.5 * np.amax(hist)
    first_energy = bin_centers[np.argmax(idxs_over_50)]
    last_energy = bin_centers[len(idxs_over_50) - np.argmax(idxs_over_50[::-1])]
    return (last_energy - first_energy)


def get_bin_centers(bins):
    """
    Returns an array of bin centers from an input array of bin edges. 
    Works for non-uniform binning.
    """
    return (bins[:-1] + bins[1:]) / 2.


def get_bin_widths(bins):
    """
    Returns an array of bin widths from an input array of bin edges. 
    Works for non-uniform binning.
    """
    return (bins[1:] - bins[:-1])


def plot_hist(hist, bins, var=None, show_stats=False, **kwargs):
    """
    plot a step histogram, with optional error bars
    """
    if var is None:
        plt.step(bins, np.concatenate((hist, [0])), where="post")
    else:
        plt.errorbar(get_bin_centers(bins), hist,
                     xerr=get_bin_widths(bins) / 2, yerr=np.sqrt(var),
                     fmt='none', **kwargs)
    if show_stats is True:
        bin_centers = get_bin_centers(bins)
        N = np.sum(hist)
        mean = np.sum(hist*bin_centers)/N
        x2ave = np.sum(hist*bin_centers*bin_centers)/N
        stddev = np.sqrt(N/(N-1) * (x2ave - mean*mean))

        mean, stddev = pgu.get_formatted_stats(mean, stddev, 3)
        stats = '$\mu=%s$\n$\sigma=%s$' % (mean, stddev)
        plt.text(0.95, 0.95, stats, transform=plt.gca().transAxes,
                 verticalalignment='top', horizontalalignment='right')

def get_gaussian_guess(hist, bin_centers):
    """
    given a hist, gives guesses for mu, sigma, and amplitude
    """
    max_idx = np.argmax(hist)
    guess_e = bin_centers[max_idx]
    guess_amp = hist[max_idx]

    # find 50% amp bounds on both sides for a FWHM guess
    guess_sigma = get_fwhm(hist, bin_centers) / 2.355  # FWHM to sigma
    guess_area = guess_amp * guess_sigma * np.sqrt(2 * np.pi)

    return (guess_e, guess_sigma, guess_area)