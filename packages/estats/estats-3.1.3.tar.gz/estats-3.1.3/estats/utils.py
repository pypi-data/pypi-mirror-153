# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp
import importlib
import pathlib
import glob
import os
from tqdm import tqdm

from ekit import logger

LOGGER = logger.init_logger(__name__)


def _calc_alms(shear_map_1, shear_map_2, mode='A', method='KS',
               shear_1_err=[], shear_2_err=[], lmax=None):
    """
    Calculates spherical harmonics given two shear maps.
    Then converts to convergence spin-0 alms using indicated mass
    mapping technique.

    :param shear_map_1: First component Healpix shear map
    :param shear_map_2: Second component Healpix shear map
    :param mode: If E return E modes only, if B return B modes only,
                 if A return both
    :param method: Mass mapping method.
                   Currently only Kaiser-Squires supported.
    :param shear_1_err: Standard deviation of shear
                        component 1 pixel by pixel.
    :param shear_1_err: Standard deviation of shear
                        component 2 pixel by pixel.
    :param lmax: Maximum ell to consider for the alms.
    :return: spherical harmonics E and B modes for spin-0 convergence field.
    """

    if lmax is None:
        lmax = 3 * hp.npix2nside(shear_map_1.size) - 1

    if (len(shear_map_1) == 0) | (len(shear_map_2) == 0):
        if mode == 'A':
            return [], []
        elif mode == 'E':
            return []
        elif mode == 'B':
            return []

    if method == 'KS':
        # Spin spherical harmonic decomposition

        # numerical problems can lead to some pixels being inf / nan
        # remove manually

        is_inf = np.logical_or(np.isinf(shear_map_1), np.isinf(shear_map_2))
        is_nan = np.logical_or(np.isnan(shear_map_1), np.isnan(shear_map_2))
        is_bad = np.logical_or(is_inf, is_nan)
        shear_map_1[is_bad] = 0.0
        shear_map_2[is_bad] = 0.0

        # manually set UNSEENs to 0 since healpy messes this up sometimes
        shear_map_1[np.logical_not(shear_map_1 > hp.UNSEEN)] = 0.0
        shear_map_2[np.logical_not(shear_map_2 > hp.UNSEEN)] = 0.0

        alm_T, alm_E, alm_B = hp.map2alm(
            [np.zeros_like(shear_map_1), shear_map_1, shear_map_2], lmax=lmax)

        ell = hp.Alm.getlm(lmax)[0]
        ell[ell == 1] = 0

        # Multiply by the appropriate factor for spin convertion
        fac = np.where(np.logical_and(ell != 1, ell != 0),
                       - np.sqrt(((ell + 1.0) * ell) / ((ell + 2.0)
                                                        * (ell - 1.0))), 0)
        if mode == 'A':
            alm_E *= fac
            alm_B *= fac
            return alm_E, alm_B
        elif mode == 'E':
            alm_E *= fac
            return alm_E
        elif mode == 'B':
            alm_B *= fac
            return alm_B
    elif method == 'N0oB':
        LOGGER.error("N0oB is not supported anymore!")
        # NOTE: Not sure about healpix sign convention yet
        if (len(shear_1_err) == 0) | (len(shear_2_err) == 0):
            raise Exception(
                "Not all maps given that are needed to use Null B mode "
                "prior method")

        # Need std(shear_i) and galaxy count in each pixel (n1, n2, n_gals)
        noise_map_1 = shear_1_err
        noise_map_2 = shear_2_err
        mask = shear_map_1 > hp.UNSEEN
        shear_map_1[~mask] = 0.0
        shear_map_2[~mask] = 0.0
        noise_map_1[~mask] = 0.0
        noise_map_2[~mask] = 0.0

        assert np.all(noise_map_1 >= 0.0)
        assert np.all(noise_map_2 >= 0.0)
        # upgrade to higher resolution
        NSIDE_high = 2 * hp.npix2nside(shear_map_1)
        mask = hp.pixelfunc.ud_grade(mask, nside_out=NSIDE_high)
        alm_mute = hp.map2alm(noise_map_1)
        noise_1 = hp.alm2map(alm_mute, nside=NSIDE_high)
        alm_mute = hp.map2alm(noise_map_2)
        noise_2 = hp.alm2map(alm_mute, nside=NSIDE_high)

        noise_1 = np.abs(noise_1)
        noise_2 = np.abs(noise_2)

        # checks noise matrix (sometimes when you upgrade your noise matrix to
        # higher nside, some pixels have a very small value and this might
        # screw up things)
        mask_std = noise_2 < np.mean(noise_2[mask]) - 3 * np.std(noise_2[mask])
        noise_2[mask_std] = np.mean(noise_2[mask]) - 3 * np.std(noise_2[mask])

        mask_std = noise_1 < np.mean(noise_1[mask]) - 3 * np.std(noise_1[mask])
        noise_1[mask_std] = np.mean(noise_1[mask]) - 3 * np.std(noise_1[mask])

        # calc alms of shear
        alm_mute = hp.map2alm(shear_map_1)
        e1 = hp.alm2map(alm_mute, nside=NSIDE_high)
        alm_mute = hp.map2alm(shear_map_2)
        e2 = hp.alm2map(alm_mute, nside=NSIDE_high)

        En, Bn = e1 * 0., e1 * 0.
        power = 1
        iterations = 15
        xx = 2
        ft = np.abs((np.mean(
            (0.5 * ((noise_1**power)[mask] + (noise_2**power)[mask])))))
        for i in tqdm(range(iterations)):
            e1n, e2n = _gk_inv(En, Bn, nside=NSIDE_high,
                               lmax=NSIDE_high * xx - 1)
            d1 = ft * (e1 - e1n) / (noise_1**power)
            d2 = ft * (e2 - e2n) / (noise_2**power)
            REn, RBn, _ = _g2k_sphere_2(
                d1, d2, mask, nside=NSIDE_high, lmax=NSIDE_high * xx,
                nosh=True)
            En = REn + En
            Bn = RBn + Bn
        alm_B = hp.map2alm(Bn, lmax=lmax)
        alm_E = hp.map2alm(En, lmax=lmax)
        if mode == 'A':
            return alm_E, alm_B
        elif mode == 'E':
            return alm_E
        elif mode == 'B':
            return alm_B
    else:
        raise Exception(
            "Mass mapping technique named {} not found.".format(method))


def import_executable(stat, func):
    """
    Import function func from stat plugin.
    :param verbose: Verbose mode
    :param logger: Logging instance
    """
    executable = importlib.import_module(
        '.stats.{}'.format(stat), package='estats')
    executable = getattr(executable, func)
    return executable


def _get_plugin_contexts(alloweds=[], typess=[], defaultss=[]):
    """
    Gets the contexts for the different statistics plugins
    """

    # get all context parameters from the different statistics plugins
    dir = pathlib.Path(__file__).parent.absolute()
    plugin_paths = glob.glob('{}/stats/*.py'.format(dir))
    plugins = []
    for plugin in plugin_paths:
        if ('__init__' in plugin):
            continue
        else:
            plugins.append(os.path.basename(plugin.split('.py')[0]))

    stat_types = {}

    for plugin in plugins:
        allowed, defaults, types, stat_type \
            = import_executable(plugin, 'context')()
        for ii, a in enumerate(allowed):
            if a in alloweds:
                continue
            else:
                alloweds.append(a)
                typess.append(types[ii])
                defaultss.append(defaults[ii])

        stat_types[plugin] = stat_type

    # add extra keywords
    alloweds.append('stat_types')
    defaultss.append(stat_types)
    types.append('dict')
    return alloweds, typess, defaultss


def _gk_inv(K, KB, nside, lmax):
    alms = hp.map2alm(K, lmax=lmax, pol=False)  # Spin transform!
    ell, emm = hp.Alm.getlm(lmax=lmax)
    kalmsE = alms / (1. * ((ell * (ell + 1.))
                           / ((ell + 2.) * (ell - 1))) ** 0.5)
    kalmsE[ell == 0] = 0.0
    alms = hp.map2alm(KB, lmax=lmax, pol=False)  # Spin transform!
    ell, emm = hp.Alm.getlm(lmax=lmax)
    kalmsB = alms / (1. * ((ell * (ell + 1.))
                           / ((ell + 2.) * (ell - 1))) ** 0.5)
    kalmsB[ell == 0] = 0.0
    _, e1t, e2t = hp.alm2map([kalmsE, kalmsE, kalmsB],
                             nside=nside, lmax=lmax, pol=True)
    return e1t, e2t


def _g2k_sphere_2(gamma1, gamma2, mask, nside=1024, lmax=2048, nosh=True):
    """
    Convert shear to convergence on a sphere. In put are all healpix maps.
    """
    gamma1_mask = gamma1 * mask
    gamma2_mask = gamma2 * mask
    KQU_masked_maps = [gamma1_mask, gamma1_mask, gamma2_mask]
    # this fails for some reason
    alms = hp.map2alm(KQU_masked_maps, lmax=lmax, pol=True)  # Spin transform!
    ell, emm = hp.Alm.getlm(lmax=lmax)
    if nosh:
        almsE = alms[1] * 1. * ((ell * (ell + 1.))
                                / ((ell + 2.) * (ell - 1))) ** 0.5
        almsB = alms[2] * 1. * ((ell * (ell + 1.))
                                / ((ell + 2.) * (ell - 1))) ** 0.5
    else:
        almsE = alms[1] * 1.
        almsB = alms[2] * 1.
    almsE[ell == 0] = 0.0
    almsB[ell == 0] = 0.0
    almsE[ell == 1] = 0.0
    almsB[ell == 1] = 0.0
    almssm = [alms[0], almsE, almsB]
    E_map = hp.alm2map(almssm[1], nside=nside, lmax=lmax, pol=False)
    B_map = hp.alm2map(almssm[2], nside=nside, lmax=lmax, pol=False)
    return E_map, B_map, almsE
