# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp
from estats.stats import CrossPeaks


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'convergence-cross'

    required = ['Starlet_steps', 'Starlet_scalesDi',
                'Starlet_selected_scalesDi',
                'peak_lower_threshold', 'Starlet_sliced_bins',
                'NSIDE', 'min_count', 'SNR_peaks', 'max_SNR']
    defaults = [1000, [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096],
                [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096],
                2.5, 15, 1024, 30, False, 100.]
    types = ['int', 'list', 'list', 'float', 'int', 'int',
             'int', 'bool', 'float']
    return required, defaults, types, stat_type


def CrossStarletPeaksDi(map_w, weights, ctx):
    """
    Performs the starlet-wavelet decomposition of map and counts the local
    maxima in each filter band.
    :param map: A Healpix convergence map
    :param weights: A Healpix map with pixel weights (integer >=0)
    :param ctx: Context instance
    :return: Starlet counts (num filter bands, Starlet_steps + 1)
    """

    try:
        from esd import esd
    except ImportError:
        raise ImportError(
            "Did not find esd package. "
            "It is required for this module to work properly. "
            "Download from: "
            "https://cosmo-gitlab.phys.ethz.ch/cosmo_public/esd")

    # build decomposition
    # (remove first map that contains remaining small scales)
    wavelet_counts = np.zeros((len(ctx['Starlet_scalesDi']),
                               ctx['Starlet_steps'] + 1))

    # count peaks in each filter band
    wave_iter = esd.calc_wavelet_decomp_iter(
        map_w, l_bins=ctx['Starlet_scalesDi'])
    counter = 0
    for ii, wmap in enumerate(wave_iter):
        if ii == 0:
            continue
        # reapply mask
        wmap[np.isclose(weights, 0)] = hp.UNSEEN

        peak_vals = CrossPeaks.CrossPeaks(wmap, weights, ctx)
        wavelet_counts[counter] = peak_vals
        counter += 1

    return wavelet_counts


def process(data, ctx, scale_to_unity=False):
    # backwards compatibility for data without map std
    if data.shape[1] > ctx['CrossPeaks_steps']:
        data = data[:, :-1]

    num_of_scales = len(ctx['Starlet_scalesDi'])

    new_data = np.zeros(
        (int(data.shape[0] / num_of_scales), data.shape[1]
         * num_of_scales))
    for jj in range(int(data.shape[0] / num_of_scales)):
        new_data[jj, :] = data[jj * num_of_scales:
                               (jj + 1) * num_of_scales, :].ravel()
    return new_data


def slice(ctx):
    # number of datavectors for each scale
    mult = 1
    # number of scales
    num_of_scales = len(ctx['Starlet_scalesDi'])
    # either mean or sum, for how to assemble the data into the bins
    operation = 'sum'

    n_bins_sliced = ctx['Starlet_sliced_bins']

    # if True assumes that first and last entries of the data vector indicate
    # the upper and lower boundaries and that binning scheme indicates
    # bin edges rather than their indices
    range_mode = True

    return num_of_scales, n_bins_sliced, operation, mult, range_mode


def decide_binning_scheme(data, meta, bin, ctx):
    num_of_scales = len(ctx['Starlet_scalesDi'])
    n_bins_original = ctx['Starlet_steps']
    n_bins_sliced = ctx['Starlet_sliced_bins']

    # get the correct tomographic bins
    bin_idx = np.zeros(meta.shape[0], dtype=bool)
    bin_idx[np.where(meta[:, 0] == bin)[0]] = True
    bin_idx = np.repeat(bin_idx, meta[:, 1].astype(int))
    data = data[bin_idx, :]

    # Get bins for each smooting scale
    bin_centers = np.zeros((num_of_scales, n_bins_sliced))
    bin_edges = np.zeros((num_of_scales, n_bins_sliced + 1))
    for scale in range(num_of_scales):
        # cut correct scale and minimum and maximum kappa values
        data_act = data[:,
                        n_bins_original * scale:n_bins_original * (scale + 1)]
        minimum = np.max(data_act[:, 0])
        maximum = np.min(data_act[:, -1])
        new_kappa_bins = np.linspace(minimum, maximum, n_bins_sliced + 1)
        bin_edges[scale, :] = new_kappa_bins

        bin_centers_act = new_kappa_bins[:-1] + 0.5 * \
            (new_kappa_bins[1:] - new_kappa_bins[:-1])
        bin_centers[scale, :] = bin_centers_act
    return bin_edges, bin_centers


def filter(ctx):
    filter = np.zeros(0)
    for scale in reversed(ctx['Starlet_scalesDi']):
        if scale in ctx['Starlet_selected_scalesDi']:
            f = [True] * \
                ctx['Starlet_sliced_bins']
            f = np.asarray(f)
        else:
            f = [False] * \
                ctx['Starlet_sliced_bins']
            f = np.asarray(f)
        filter = np.append(filter, f)
    return filter
