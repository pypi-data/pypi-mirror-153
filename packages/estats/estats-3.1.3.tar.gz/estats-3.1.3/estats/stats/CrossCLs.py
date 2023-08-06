# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'convergence'

    required = ['lmax', 'CrossCLs_sliced_bins', 'CrossCLs_min',
                'CrossCLs_max', 'n_tomo_bins', 'selected_l_range',
                'CrossCLs_custom', 'bin', 'weight_cls']
    defaults = [1000, 15, 100, 1000, 4, '0-10000', [], 0, False]
    types = ['int', 'int', 'int', 'int', 'int', 'str',
             'list', 'int', 'bool']
    return required, defaults, types, stat_type


def CrossCLs(map1, map2, weights1, weights2, ctx):
    """
    Calculates the Cross Angular Power spectrum of two convergence maps.
    :param map1: A Healpix convergence map
    :param map2: A second Healpix convergence map
    :param weights1: A Healpix map with pixel weights
    :param weights2: A second Healpix map with pixel weights
    :param ctx: Context instance
    :return: Cross CLs
    """
    lmax = ctx['lmax'] - 1

    # check if weights are set
    if (not ctx['weight_cls']) | (len(weights1) == 0):
        weights1_ = np.ones_like(map1, dtype=ctx['prec'])
        weights1_[np.isclose(weights1, 0.0)] = 0.0
    else:
        weights1_ = weights1
    if (not ctx['weight_cls']) | (len(weights2) == 0):
        weights2_ = np.ones_like(map2, dtype=ctx['prec'])
        weights2_[np.isclose(weights2, 0.0)] = 0.0
    else:
        weights2_ = weights2

    # proper weight masking
    select_seen = weights1_ > 0
    select_unseen = ~select_seen
    select_unseen |= map1 == hp.UNSEEN
    map1_w = (map1 * weights1_).astype(np.float64)
    map1_w[select_unseen] = hp.UNSEEN

    select_seen = weights2_ > 0
    select_unseen = ~select_seen
    select_unseen |= map2 == hp.UNSEEN
    map2_w = (map2 * weights2_).astype(np.float64)
    map2_w[select_unseen] = hp.UNSEEN

    cls = np.array(hp.sphtfunc.anafast(map1_w, map2_w, lmax=lmax))
    cls = cls.reshape(1, cls.size)

    return cls


def process(data, ctx, scale_to_unity=False):
    if scale_to_unity:
        data *= 1e4
    return data


def slice(ctx):
    # number of datavectors for each scale
    mult = 1
    # number of scales
    num_of_scales = 1
    # either mean or sum, for how to assemble the data into the bins
    operation = 'mean'

    if len(ctx['CrossCLs_custom']) > 0:
        n_bins_sliced = len(ctx['CrossCLs_custom'])
    else:
        n_bins_sliced = ctx['CrossCLs_sliced_bins']

    return num_of_scales, n_bins_sliced, operation, mult


def decide_binning_scheme(data, meta, bin, ctx):
    # Perform simple equal width splitting for Cls.
    if len(ctx['CrossCLs_custom']) > 0:
        edges = np.asarray(ctx['CrossCLs_custom'])

        num_of_scales = 1
        bin_centers = np.zeros((num_of_scales, edges.shape[0]))
        bin_edge_indices = np.zeros((num_of_scales, edges.shape[0] + 1))

        lower_edges = edges[:, 0]
        upper_edges = edges[:, 1]

        bin_edge_indices[0, :-1] = lower_edges
        bin_edge_indices[0, -1] = upper_edges[-1]
        id_larger = bin_edge_indices > ctx['lmax']
        if np.sum(id_larger) > 1:
            raise Exception(
                "Your custom binning scheme requires more multipols than "
                "given in the data!")
        elif id_larger[0, -1]:
            bin_edge_indices[0, -1] = ctx['lmax']
        bin_centers[0] = bin_edge_indices[0, :-1] \
            + 0.5 * (bin_edge_indices[0, 1:] - bin_edge_indices[0, :-1])
    else:
        range_edges = [ctx['CrossCLs_min'], ctx['CrossCLs_max']]
        num_of_scales = 1
        n_bins_sliced = ctx['CrossCLs_sliced_bins']
        bin_centers = np.zeros((num_of_scales, n_bins_sliced))
        bin_edge_indices = np.zeros((num_of_scales, n_bins_sliced + 1))

        # Cut out desired l range
        minimum = range_edges[0]
        maximum = range_edges[1]
        diff = maximum - minimum

        per_bin = diff // n_bins_sliced
        remain = diff % n_bins_sliced
        remain_front = remain // 2
        remain_back = remain_front + remain % 2

        # Decide on edge indices
        bin_edge_indices_temp = np.arange(
            remain_front + minimum, maximum - remain_back, per_bin)
        bin_edge_indices_temp[0] -= remain_front
        bin_edge_indices_temp = np.append(bin_edge_indices_temp, maximum)

        # Decide on central bin values
        bin_centers_temp = np.zeros(0)
        for jj in range(len(bin_edge_indices_temp) - 1):
            bin_centers_temp = np.append(
                bin_centers_temp,
                np.nanmean(bin_edge_indices_temp[jj:jj + 2]))

        # For consistency with other binning scheme
        # assign same binning to all scales
        for scale in range(num_of_scales):
            bin_centers[scale, :] = bin_centers_temp
            bin_edge_indices[scale, :] = bin_edge_indices_temp

    return bin_edge_indices, bin_centers


def filter(ctx):
    bin_edge_indices = decide_binning_scheme(None, None, None, ctx)[0][0]
    if ',' in ctx['selected_l_range']:
        # assuming list of l ranges. One for each bin combination
        if ctx['n_tomo_bins'] == 0:
            raise Exception(
                "Passed a list of l-ranges for non-tomographic data vector.")
        range = ctx['selected_l_range'].split(',')[ctx['bin']]
    else:
        range = ctx['selected_l_range']

    lower_edge = int(range.split('-')[0])
    upper_edge = int(range.split('-')[1])
    filter = bin_edge_indices[:-1] > lower_edge
    filter &= bin_edge_indices[1:] < upper_edge
    return filter
