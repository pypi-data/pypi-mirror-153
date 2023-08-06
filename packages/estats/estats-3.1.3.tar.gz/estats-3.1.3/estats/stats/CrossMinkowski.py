# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp


def context():
    """
    Defines the paramters used by the plugin
    """
    stat_type = 'multi'

    required = ['Minkowski_max', 'Minkowski_min', 'CrossMinkowski_steps',
                'CrossMinkowski_sliced_bins', 'NSIDE',
                'scales', 'selected_scales', 'no_V0']
    defaults = [4.0, -4.0, 10, 10, 1024,
                [31.6, 29.0, 26.4, 23.7, 21.1, 18.5, 15.8, 13.2,
                 10.5, 7.9, 5.3, 2.6], [31.6, 29.0, 26.4, 23.7, 21.1, 18.5,
                                        15.8, 13.2, 10.5], False]
    types = ['float', 'float', 'int', 'int', 'int', 'list', 'list', 'bool']
    return required, defaults, types, stat_type


def CrossMinkowski_proper(kappa, weights, ctx):
    """
    Proper calculation of Minkowski functionals.
    nvolves a lot of alm decompositions and is therfore
    quite slow.
    For forward modelling use CrossMinkowski function instead.
    :param kappa: A Healpix convergence map
    :param weights: A Healpix map with pixel weights
    :param ctx: Context instance
    :return: Minkowski functionals as V0,V1,V2.
    """
    mask = weights > 0

    alms = hp.sphtfunc.map2alm(
        kappa, use_weights=False, lmax=2*hp.npix2nside(kappa.size))

    # first order covariant derivatives
    # d_phi is d_phi / sin(theta)
    _, d_theta, d_phi = hp.sphtfunc.alm2map_der1(
        alms, hp.npix2nside(kappa.size), lmax=2*hp.npix2nside(kappa.size))
    d_theta[np.isclose(weights, 0.0)] = hp.UNSEEN
    d_phi[np.isclose(weights, 0.0)] = hp.UNSEEN

    # second order covariant derivatives
    alms_d_phi = hp.sphtfunc.map2alm(d_phi, lmax=2*hp.npix2nside(kappa.size))
    alms_d_theta = hp.sphtfunc.map2alm(
        d_theta, lmax=2*hp.npix2nside(kappa.size))
    _, _, d_phi_phi = hp.sphtfunc.alm2map_der1(
        alms_d_phi, hp.npix2nside(kappa.size),
        lmax=2*hp.npix2nside(kappa.size))
    _, d_theta_theta, d_theta_phi = hp.sphtfunc.alm2map_der1(
        alms_d_theta, hp.npix2nside(kappa.size),
        lmax=2*hp.npix2nside(kappa.size))

    # need the inverted tangent at each pixel location
    theta, _ = hp.pix2ang(hp.npix2nside(kappa.size), np.arange(kappa.size))
    arctan = np.arctan(theta)

    # covariant derivatives
    cd_theta = d_theta
    cd_phi = d_phi
    cd_theta_theta = d_theta_theta
    cd_phi_phi = d_phi_phi + arctan * d_theta
    cd_theta_phi = d_theta_phi - arctan * d_phi

    # masking
    kappa_m = kappa[mask]
    cd_theta = cd_theta[mask]
    cd_phi = cd_phi[mask]
    cd_theta_theta = cd_theta_theta[mask]
    cd_phi_phi = cd_phi_phi[mask]
    cd_theta_phi = cd_theta_phi[mask]

    # calculate integrands I1, I2
    denom = np.sum(kappa_m)
    norm = np.power(cd_theta, 2.) + np.power(cd_phi, 2.)
    I1 = np.sqrt(norm) / (4. * denom)
    I2 = (2. * cd_theta * cd_phi * cd_theta_phi - np.power(cd_phi, 2.)
          * cd_theta_theta - np.power(cd_theta, 2.)
          * cd_phi_phi) / (norm * 2. * np.pi * denom)

    # calculate Minkowski functionals
    thresholds = np.linspace(
        ctx['Minkowski_min'], ctx['Minkowski_max'],
        ctx['CrossMinkowski_steps'])

    sigma_0 = np.std(kappa_m)
    thresholds *= sigma_0

    # Minkowski calculation
    res = np.zeros(ctx['Minkowski_steps'] * 3)
    for it, thres in enumerate(thresholds):
        # calc the three MFs
        V0 = np.sum(kappa_m >= thres) / denom
        delta_func = np.isclose(kappa_m, thres, rtol=0.0, atol=1e-6)
        V1 = np.sum(I1[delta_func])
        V2 = np.sum(I2[delta_func])
        res[it * 3] = V0
        res[it * 3 + 1] = V1
        res[it * 3 + 2] = V2

    # reordering
    V0 = res[0::3]
    V1 = res[1::3]
    V2 = res[2::3]
    res = np.append(V0, np.append(V1, V2))
    return res


def CrossMinkowski(kappa_w, weights, ctx):
    """
    Calculates Minkowski functionals on a convergence map.
    This is a very crude approximation that will not match with theory!
    Preferable for forward modelling due to speed.
    :param kappa_w: A Healpix convergence map
    :param weights: A Healpix map with pixel weights
    :param ctx: Context instance
    :return: Minkowski functionals as V0,V1,V2.
    """

    num_chunks = 1

    ell = kappa_w.size
    nside = hp.get_nside(kappa_w)
    ran = np.arange(ell, dtype=np.int32)
    mask = weights > 0.0
    ran = ran[mask]

    # restrict to pixels with neighbours in the mask
    counter = 0
    to_keep = np.ones_like(ran, dtype=bool)
    for r in np.array_split(ran, num_chunks):
        low = counter
        high = counter + len(r)
        neighbours = hp.get_all_neighbours(nside, r)[[1, 3, 5, 7]]
        edges = np.any(kappa_w[neighbours] < -1e20, axis=0)
        to_keep[low:high] = np.logical_and(
            to_keep[low:high], np.logical_not(edges))
        counter += len(r)
    ran = ran[to_keep]

    # calculate first order derivatives (with neighbours only)
    deriv_phi = np.zeros(ell, dtype=np.float32)
    deriv_theta = np.zeros(ell, dtype=np.float32)
    for r in np.array_split(ran, num_chunks):
        neighbours = hp.get_all_neighbours(nside, r)[[1, 3, 5, 7]]
        deriv_phi[r] = -kappa_w[neighbours[0]] + kappa_w[neighbours[2]]
        deriv_theta[r] = -kappa_w[neighbours[3]] + kappa_w[neighbours[1]]

    to_keep = to_keep[to_keep]
    # calculate second order derivatives
    V1 = np.zeros_like(ran, dtype=np.float32)
    V2 = np.zeros_like(ran, dtype=np.float32)
    counter = 0
    for r in np.array_split(ran, num_chunks):
        low = counter
        high = counter + len(r)

        # calculate V1
        ##############
        V1[low:high] = np.power(
            deriv_theta[r], 2.) + np.power(deriv_phi[r], 2.)

        neighbours = hp.get_all_neighbours(nside, r)[[1, 3, 5, 7]]

        # calculate V2 part by part to save RAM
        #######################################
        # term 1
        deriv_phi_theta = -deriv_phi[neighbours[3]] + deriv_phi[neighbours[1]]
        V2[low:high] = 2. * deriv_phi[r] * deriv_phi_theta
        to_keep[low:high] = np.logical_and(
            to_keep[low:high], np.abs(deriv_phi_theta) < 1e10)
        V2[low:high] *= deriv_theta[r]

        # term 2
        deriv_theta_theta = -deriv_theta[neighbours[3]] \
            + deriv_theta[neighbours[1]]
        V2[low:high] -= np.power(deriv_phi[r], 2.) * deriv_theta_theta
        to_keep[low:high] = np.logical_and(
            to_keep[low:high], np.abs(deriv_theta_theta) < 1e10)

        # term 3
        deriv_phi_phi = -deriv_phi[neighbours[0]] + deriv_phi[neighbours[2]]
        V2[low:high] -= np.power(deriv_theta[r], 2.) * deriv_phi_phi
        to_keep[low:high] = np.logical_and(
            to_keep[low:high], np.abs(deriv_phi_phi) < 1e10)

    # removing extreme derivatives
    kappa_m = kappa_w[ran[to_keep]]
    V1 = V1[to_keep]
    V2 = V2[to_keep]

    with np.errstate(divide='ignore'):
        V2 = np.divide(V2, V1)
    V1 = np.sqrt(V1)

    # averaged standard deviation and normalization
    sigma_0 = np.std(kappa_m)

    thresholds = np.linspace(ctx['Minkowski_min'],
                             ctx['Minkowski_max'], ctx['CrossMinkowski_steps'])
    thresholds *= sigma_0

    # Minkowski calculation
    res = np.zeros(ctx['CrossMinkowski_steps'] * 3, dtype=np.float32)
    for it, thres in enumerate(thresholds):
        # calc the three MFs
        V0_ = np.sum(kappa_m >= thres)
        delta_func = (kappa_m > (thres - 1e-6)) & (kappa_m < (thres + 1e-6))
        V1_ = np.sum(V1[delta_func])
        V2_ = np.sum(V2[delta_func])
        res[it * 3] = V0_
        res[it * 3 + 1] = V1_
        res[it * 3 + 2] = V2_

    # reordering
    V0 = res[0::3]
    V1 = res[1::3]
    V2 = res[2::3]
    res = np.append(V0, np.append(V1, V2))

    return res


def process(data, ctx, scale_to_unity=False):
    num_of_scales = len(ctx['scales'])

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
    num_of_scales = len(ctx['scales'])
    # either mean or sum, for how to assemble the data into the bins
    operation = 'mean'

    n_bins_sliced = ctx['CrossMinkowski_sliced_bins']

    return num_of_scales, n_bins_sliced, operation, mult


def decide_binning_scheme(data, meta, bin, ctx):
    # For Minkowski perform simple equal bin width splitting.
    # Same splitting for each smoothing scale.
    range_edges = [ctx['Minkowski_min'], ctx['Minkowski_max']]
    n_bins_original = ctx['CrossMinkowski_steps']
    num_of_scales = len(ctx['scales'])
    n_bins_sliced = ctx['CrossMinkowski_sliced_bins']
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
    for scale in ctx['scales']:
        if scale in ctx['selected_scales']:
            f = [True] * \
                ctx['CrossMinkowski_sliced_bins']
            f = np.asarray(f)
        else:
            f = [False] * \
                ctx['CrossMinkowski_sliced_bins']
            f = np.asarray(f)

        f = np.tile(f, 3)
        if ctx['no_V0']:
            f[:ctx['CrossMinkowski_sliced_bins']] = False
        filter = np.append(filter, f)
    return filter
