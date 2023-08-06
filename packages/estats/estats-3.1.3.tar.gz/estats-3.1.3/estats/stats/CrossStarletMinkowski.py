# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp
from estats.stats import CrossMinkowski


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'convergence-cross'

    required = ['Minkowski_max', 'Minkowski_min', 'Minkowski_steps',
                'Minkowski_sliced_bins', 'Starlet_scales',
                'Starlet_selected_scales',
                'NSIDE', 'no_V0']
    defaults = [4.0, -4.0, 10, 10, [48, 65, 89, 121, 164, 223, 303, 412, 560,
                761, 1034, 1405, 1910, 2597, 3530,
                4799, 6523, 8867, 12053, 16384],
                [48, 65, 89, 121, 164, 223, 303, 412, 560,
                 761, 1034, 1405, 1910, 2597, 3530,
                 4799, 6523, 8867, 12053, 16384],
                1024, False]
    types = ['float', 'float', 'int', 'int', 'list', 'list', 'int', 'bool']
    return required, defaults, types, stat_type


def CrossStarletMinkowski(map_w, weights, ctx):
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
    wavelet_counts = np.zeros((len(ctx['Starlet_scales']),
                               ctx['Minkowski_steps'] * 3))

    # count peaks in each filter band
    wave_iter = esd.calc_wavelet_decomp_iter(
        map_w, l_bins=ctx['Starlet_scales'])
    counter = 0
    for ii, wmap in enumerate(wave_iter):
        if ii == 0:
            continue
        # reapply mask
        wmap[np.isclose(weights, 0)] = hp.UNSEEN

        # calc Minkowski functionals
        minks = CrossMinkowski.CrossMinkowski(wmap, weights, ctx)
        wavelet_counts[counter] = minks
        counter += 1

    return wavelet_counts


def process(data, ctx, scale_to_unity=False):
    num_of_scales = len(ctx['Starlet_scales'])

    new_data = np.zeros(
        (int(data.shape[0] / num_of_scales), data.shape[1]
         * num_of_scales))
    for jj in range(int(data.shape[0] / num_of_scales)):
        new_data[jj, :] = data[jj * num_of_scales:
                               (jj + 1) * num_of_scales, :].ravel()
    return new_data


def slice(ctx):
    # number of datavectors for each scale
    mult = 3
    # number of scales
    num_of_scales = len(ctx['Starlet_scales'])
    # either mean or sum, for how to assemble the data into the bins
    operation = 'mean'

    n_bins_sliced = ctx['Minkowski_sliced_bins']

    return num_of_scales, n_bins_sliced, operation, mult


def decide_binning_scheme(data, meta, bin, ctx):
    # For Minkowski perform simple equal bin width splitting.
    # Same splitting for each smoothing scale.
    range_edges = [ctx['Minkowski_min'], ctx['Minkowski_max']]
    n_bins_original = ctx['Minkowski_steps']
    num_of_scales = len(ctx['Starlet_scales'])
    n_bins_sliced = ctx['Minkowski_sliced_bins']
    bin_centers = np.zeros((num_of_scales, n_bins_sliced))
    bin_edge_indices = np.zeros((num_of_scales, n_bins_sliced + 1))

    orig_bin_values = np.linspace(
        range_edges[0], range_edges[1], n_bins_original)

    per_bin = n_bins_original // n_bins_sliced
    remain = n_bins_original % n_bins_sliced
    remain_front = remain // 2
    remain_back = remain_front + remain % 2

    # Get edge indices
    bin_edge_indices_temp = np.arange(
        remain_front, n_bins_original - remain_back, per_bin)
    bin_edge_indices_temp[0] -= remain_front
    bin_edge_indices_temp = np.append(
        bin_edge_indices_temp, n_bins_original)

    # Get bin central values
    bin_centers_temp = np.zeros(0)
    for jj in range(len(bin_edge_indices_temp) - 1):
        bin_centers_temp = np.append(bin_centers_temp, np.nanmean(
            orig_bin_values[bin_edge_indices_temp[jj]:
                            bin_edge_indices_temp[jj + 1]]))

    # Assign splitting to each scale
    for scale in range(num_of_scales):
        bin_centers[scale, :] = bin_centers_temp
        bin_edge_indices[scale, :] = bin_edge_indices_temp

    return bin_edge_indices, bin_centers


def filter(ctx):
    filter = np.zeros(0)
    for scale in reversed(ctx['Starlet_scales']):
        if scale in ctx['Starlet_selected_scales']:
            f = [True] * \
                ctx['Minkowski_sliced_bins']
            f = np.asarray(f)
        else:
            f = [False] * \
                ctx['Minkowski_sliced_bins']
            f = np.asarray(f)

        f = np.tile(f, 3)
        if ctx['no_V0']:
            f[:ctx['Minkowski_sliced_bins']] = False
        filter = np.append(filter, f)
    return filter
