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

    required = ['CrossVoids_steps',
                'void_upper_threshold', 'CrossVoids_sliced_bins', 'NSIDE',
                'scales', 'selected_scales', 'min_count', 'SNR_voids',
                'min_SNR']
    defaults = [1000, -2.5, 15, 1024,
                [31.6, 29.0, 26.4, 23.7, 21.1, 18.5, 15.8, 13.2,
                 10.5, 7.9, 5.3, 2.6], [31.6, 29.0, 26.4, 23.7, 21.1, 18.5,
                                        15.8, 13.2, 10.5], 30, False, -100.]
    types = ['int', 'float', 'int', 'int', 'list', 'list',
             'int', 'bool', 'float']
    return required, defaults, types, stat_type


def CrossVoids(map_w, weights, ctx):
    """
    Calculates Voids on a convergence map.
    :param map_w: A Healpix convergence map
    :param weights: A Healpix map with pixel weights
    :param ctx: Context instance
    :return: Void abundance function
    """

    # standard devaition of map
    sig = np.std(map_w[map_w > hp.pixelfunc.UNSEEN])

    ell = map_w.size

    # Exclude last element
    nside = hp.get_nside(map_w)
    ran = np.arange(ell - 1)

    # restrict to mask
    ran = ran[weights[:-1] > 0.0]

    temp = map_w[-1]
    map_w[-1] = hp.pixelfunc.UNSEEN

    voids = np.zeros(0, dtype=np.int64)

    # calculate all the neighbours, chunked (slow but slim memory)
    num_chunks = 1
    for r in np.array_split(ran, num_chunks):
        neighbours = hp.get_all_neighbours(nside, r)

        edges = np.any(map_w[neighbours] == hp.pixelfunc.UNSEEN, axis=0)

        # Get Void positions (minima)
        ps = np.all(map_w[neighbours] > map_w[r], axis=0)

        # Remove pixels which are next to an UNSEEN pixel
        ps = np.logical_and(ps, np.logical_not(edges))
        voids = np.append(voids, r[ps])

    # Last Value treatment
    map_w[-1] = temp
    n0 = hp.get_all_neighbours(nside, ell - 1)
    if (np.all(map_w[n0] < map_w[ell - 1])):
        voids = np.append(voids, ell - 1)
    n1 = np.reshape(hp.get_all_neighbours(nside, n0).T, (-1))
    voids2 = np.all(np.reshape(map_w[n1], (-1, 8))
                    > map_w[n0].reshape((-1, 1)), axis=1)
    voids2 = n0[voids2]
    voids = _select(n1, voids, voids2)

    # Remove UNSEENS labeled as Voids
    valids = map_w[voids] > -1e+20
    voids = voids[valids]

    # get values
    # and cutting off below threshold coordinates
    void_vals = map_w[voids]

    if ctx['SNR_voids']:
        void_vals /= sig

    # restrict to peaks with SNR < 4.0
    void_vals = void_vals[void_vals / sig >= ctx['min_SNR']]

    # edge case (nothing found)
    if len(void_vals) == 0:
        return np.full(ctx['Voids_steps'] + 1, np.nan)

    # Binning for values
    if len(void_vals) > (ctx['min_count'] * 200.):
        minimum = np.max(
            np.partition(void_vals, ctx['min_count'])[:ctx['min_count']])
        maximum = np.min(
            np.partition(void_vals, -ctx['min_count'])[-ctx['min_count']:])
    else:
        maximum = -1.
        minimum = 1.
    if maximum < minimum:
        minimum = np.min(void_vals)
        maximum = np.max(void_vals)
    void_bins = np.linspace(
        minimum, maximum, ctx['Voids_steps'] - 1)

    void_vals = np.histogram(void_vals, bins=void_bins)[0]
    # first and last bins indicate maximum and minmum of the kappa range
    void_vals = np.hstack((minimum, void_vals, maximum, np.asarray([sig])))
    void_vals = void_vals.reshape(1, void_vals.size)
    return void_vals


def _select(n, p1, p2):
    for i in n:
        if ((i in p1) and (i not in p2)):
            p1 = p1[p1 != i]
        if ((i in p2) and (i not in p1)):
            p1 = np.append(p1, i)
    return p1


def process(data, ctx, scale_to_unity=False):
    # backwards compatibility for data without map std
    if data.shape[1] > ctx['CrossVoids_steps']:
        data = data[:, :-1]

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
    mult = 1
    # number of scales
    num_of_scales = len(ctx['scales'])
    # either mean or sum, for how to assemble the data into the bins
    operation = 'sum'

    n_bins_sliced = ctx['CrossVoids_sliced_bins']

    # if True assumes that first and last entries of the data vector indicate
    # the upper and lower boundaries and that binning scheme indicates
    # bin edges rather than their indices
    range_mode = True

    return num_of_scales, n_bins_sliced, operation, mult, range_mode


def decide_binning_scheme(data, meta, bin, ctx):
    num_of_scales = len(ctx['scales'])
    n_bins_original = ctx['CrossVoids_steps']
    n_bins_sliced = ctx['CrossVoids_sliced_bins']

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
    for scale in ctx['scales']:
        if scale in ctx['selected_scales']:
            f = [True] * \
                ctx['CrossVoids_sliced_bins']
            f = np.asarray(f)
        else:
            f = [False] * \
                ctx['CrossVoids_sliced_bins']
            f = np.asarray(f)
        filter = np.append(filter, f)
    return filter
