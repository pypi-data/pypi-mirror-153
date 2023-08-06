# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'shear'

    required = ['lmax', 'CrossShearCLs_sliced_bins', 'CrossShearCLs_min',
                'CrossShearCLs_max', 'cl_engine']
    defaults = [1000, 20, 100, 1000, 'anafast']
    types = ['int', 'int', 'int', 'int', 'str']
    return required, defaults, types, stat_type


def CrossShearCLs(map_1, map_2, map_1_sec, map_2_sec, weight_map_1,
                  weight_map_2, ctx):
    """
    Calculates cross angular power spectrum of two sets of shear maps.
    :param map_1: A Healpix shear map, first shear component.
    :param map_2: A Healpix shear map, second shear component.
    :param map_1_sec: A second Healpix shear map, first shear component.
    :param map_2_sec: A second Healpix shear map, second shear component.
    :param weight_map_1: A Healpix map with pixel weights
    for the first shear maps
    :param weight_map_2: A Healpix map with pixel weights
    for the second shear maps
    """
    # anafast uses HealPix polarisation -> negate map_1!
    # not sure if this is also true for polspice
    shear_map_1 = [-map_1, map_2]
    shear_map_2 = [-map_1_sec, map_2_sec]

    lmax = ctx['lmax'] - 1

    # check if weights are set
    if len(weight_map_1) == 0:
        weight_map_1 = np.ones_like(map_1)
    if len(weight_map_2) == 0:
        weight_map_2 = np.ones_like(map_1_sec)

    if ctx['cl_engine'] == 'anafast':
        # proper weight masking
        select_seen = weight_map_1 > 0
        select_unseen = ~select_seen
        select_unseen |= shear_map_1[0] == hp.UNSEEN
        select_unseen |= shear_map_1[1] == hp.UNSEEN
        maps_0_w = (shear_map_1[0] * weight_map_1).astype(np.float64)
        maps_1_w = (shear_map_1[1] * weight_map_1).astype(np.float64)
        maps_0_w[select_unseen] = hp.UNSEEN
        maps_1_w[select_unseen] = hp.UNSEEN
        shear_map_1_w = [maps_0_w, maps_1_w]

        select_seen = weight_map_2 > 0
        select_unseen = ~select_seen
        select_unseen |= shear_map_2[0] == hp.UNSEEN
        select_unseen |= shear_map_2[1] == hp.UNSEEN
        maps_0_w = (shear_map_2[0] * weight_map_2).astype(np.float64)
        maps_1_w = (shear_map_2[1] * weight_map_2).astype(np.float64)
        maps_0_w[select_unseen] = hp.UNSEEN
        maps_1_w[select_unseen] = hp.UNSEEN
        shear_map_2_w = [maps_0_w, maps_1_w]

        dummie_map = np.zeros_like(shear_map_2[0])

        _, cl_e1e2, cl_b1b2, _, _, _ = np.array(
            hp.sphtfunc.anafast(
                (dummie_map, shear_map_1_w[0], shear_map_1_w[1]),
                (dummie_map, shear_map_2_w[0], shear_map_2_w[1]),
                lmax=lmax))
        Cl = {'cl_EE': cl_e1e2, 'cl_BB': cl_b1b2}

    else:
        raise Exception("Unknown cl_engine {}".format(ctx['cl_engine']))

    Cl_EE = Cl['cl_EE']
    Cl_EE = Cl_EE.reshape(1, Cl_EE.size)
    Cl_BB = Cl['cl_BB']
    Cl_BB = Cl_BB.reshape(1, Cl_BB.size)
    return (Cl_EE, Cl_BB)


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

    n_bins_sliced = ctx['CrossShearCLs_sliced_bins']

    return num_of_scales, n_bins_sliced, operation, mult


def decide_binning_scheme(data, meta, bin, ctx):
    # Perform simple equal width splitting for Cls.

    range_edges = [ctx['CrossShearCLs_min'], ctx['CrossShearCLs_max']]
    num_of_scales = 1
    n_bins_sliced = ctx['CrossShearCLs_sliced_bins']
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
    return [True] * ctx['CrossShearCLs_sliced_bins']
