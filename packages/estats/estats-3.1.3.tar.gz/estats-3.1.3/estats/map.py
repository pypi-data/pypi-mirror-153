# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp
import copy
import os

from ekit import context
from estats import utils
from ekit import paths
from ekit import logger

LOGGER = logger.init_logger(__name__)


class map:
    """
    The map module handles shear and convergence maps and calculates summary
    statistics from them.

    The summary statistics are defined via plugins that are located in the
    estats.stats folder. This allows users to easily add their own summary
    statistic without having to modify the internals of the code.
    See the :ref:`own_stat` Section to learn how to do that.

    The summary statistics can be calculated from the shear maps, the
    convergence maps or from smoothed convergence maps (multiscale approach
    for extraction of non-Gaussian features).

    If only one set of weak lensing maps is given the statistics will be
    calculated from that set directly. If two sets are given and the name of
    the statistic to be computed contains the word Cross both sets are passed
    to the statistics plugin. This can be used to calculate cross-correlations
    between maps from different tomographic bins for example.
    In the case of a multiscale statictics the maps are convolved into a
    cross-correlated map.
    If the statitic to compute contains the word Full all maps are passed over.

    The most important functionalities are:

    - convert_convergence_to_shear:

        Uses spherical Kaiser-Squires to convert the internal shear maps to
        convergence maps. The maps are masked using the internal masks.
        By default the trimmed mask is used to allow the user to disregard
        pixels where the spherical harmonics transformation introduced large
        errors.

    - convert_shear_to_convergence:

        Uses spherical Kaiser-Squires to convert the internal E-mode
        convergence map to shear maps. The maps are masked using the internal
        masks. By default the trimmed mask is used to allow the user to
        disregard pixels where the spherical harmonics transformation
        introduced large errors.

    - smooth_maps:

        Applies a Gaussian smoothing kernel to all internal convergence maps
        (E- and B-modes). The fwhm parameter decides on the FWHM of the
        Gaussian smoothing kernel. It is given in arcmin.

    - calc_summary_stats:

        Main functionality of the module. Allows to use statistics plugins
        located in the estats.stats folder to calculate map based statistics.

        See the :ref:`own_stat` Section to learn how the statistics plugins
        look like and how to make your own one.

        The summary statistics can be calculated from the shear maps, the
        convergence maps or from a smoothed convergence maps (multiscale
        approach for extraction of non-Gaussian features).

        Instead of using the internal masks for masking, extra masks can be
        used. This allows to use maps with multiple survey cutouts on it and
        select a different cutout each time the function is called.

        If use_shear_maps is set to True the function will convert the shear
        maps into convergence maps using spherical Kaiser-Squires instead of
        using the convergence maps directly.

        If copy_obj is set to False, no copies of the internal maps are made.
        This can save RAM but it also leads to the internal maps being
        overwritten. If you wish to use the internal maps after the function
        call set this to True!

        By default the function returns the calculated statistics in a
        dictionary. But if write_to_file is set to True it will append to
        files that are defined using the defined_parameters,
        undefined_parameters, output_dir and name arguments using ekit.paths.

    The accepted keywords are:

    - NSIDE:

        default: 1024

        choices: an integer being a power of 2

        The Healpix resolution that is used to produce the map products.

    - scales:

        default:
        [31.6, 29.0, 26.4, 23.7, 21.1, 18.5, 15.8, 13.2, 10.5, 7.9, 5.3, 2.6]

        choices:  A list of floats indicating the FWHM of the Gaussian
        smoothing kernels to be applied in arcmin.

        For summary statistics that are of the multi type (see :ref:`own_stat`)
        the summary statistics are extracted from the convergence maps for
        a number of scales (multiscale approach). To do so the maps are
        smoothed with Gaussian smoothing kernels of different size.
        The scales indicate the FWHM of these scales.

    - polarizations:

        default: 'A'

        choices: 'E', 'B', 'A'

        If E only returns E-mode statistics only when calc_summary_stats is
        used.
        If B only returns B-mode statistics only when calc_summary_stats is
        used.
        If A both E- and B-mode statistics are returned when calc_summary_stats
        is used.

    - prec:

        default: 32

        choices: 64, 32, 16

        Size of the float values in the Healpix maps in bits. For less then 32
        hp.UNSEEN is mapped to -inf -> No RAM optimization anymore
    """

    def __init__(self, gamma_1=[], gamma_2=[], kappa_E=[], kappa_B=[],
                 mask=[], trimmed_mask=[], weights=[],
                 context_in={}, fast_mode=False, verbosity=3, **kwargs):
        """
        Initialization function for the map class.
        For gammas, kappas, weights, masks and trimmed_masks can also pass
        multiple instances in a list.

        :param gamma_1: Map for first shear component
        :param gamma_2: Map for binond shear component
        :param kappa_E: Map for convergence E-modes
        :param kappa_B: Map for convergence B-modes
        :param mask: Optionally can provide a mask that is applied to the maps.
        :param trimmed_mask: Optionally can provide a stricter mask that is
                             applied to the convergence maps if they are
                             generated from the shear maps.
        :param weights: Can provide a map conatining the pixel weights.
        :param context_in: A dictionary containing parameters used by class.
        :param verbosity: Verbosity level (0-4)
        """

        logger.set_logger_level(LOGGER, verbosity)

        LOGGER.debug("Initializing map object")

        # setup context
        allowed = ['NSIDE', 'scales', 'polarizations', 'prec',
                   "alpha_rotations", "dec_rotations", "mirror"]

        types = ['int', 'list', 'str', 'int', 'list', 'list', 'list']

        defaults = [1024, [31.6, 29.0, 26.4, 23.7, 21.1, 18.5, 15.8, 13.2,
                           10.5, 7.9, 5.3, 2.6], 'A', 32,
                    [0], [0], [False]]

        allowed, types, defaults = utils._get_plugin_contexts(
            allowed, types, defaults)
        self.ctx = context.setup_context(
            {**context_in, **kwargs}, allowed, types, defaults,
            verbosity=verbosity)

        self.ctx['prec'] = 'float{}'.format(self.ctx['prec'])

        if fast_mode:
            LOGGER.warning(
                "Fast mode enabled -> Setting lmax to 2 * "
                "NSIDE instead of 3 * NSIDE - 1!")
            self.lmax = 2 * self.ctx['NSIDE']
        else:
            self.lmax = 3 * self.ctx['NSIDE'] - 1

        weights = list(weights)

        mask = list(mask)
        trimmed_mask = list(trimmed_mask)

        gamma_1 = list(gamma_1)
        gamma_2 = list(gamma_2)

        kappa_E = list(kappa_E)
        kappa_B = list(kappa_B)

        self.mask = {}
        for ii, m in enumerate(mask):
            try:
                len(m)
                self.set_mask(m[:], bin=ii, apply=False)
            except TypeError:
                # if object has no length -> not a list of lists but single
                self.set_mask(mask[:], bin=0, apply=False)
                break
        LOGGER.debug(f"Received {len(self.mask.keys())} masks")

        self.trimmed_mask = {}
        for ii, m in enumerate(trimmed_mask):
            try:
                len(m)
                self.set_trimmed_mask(m[:], bin=ii, apply=False)
            except TypeError:
                self.set_trimmed_mask(trimmed_mask[:], bin=0, apply=False)
                break
        LOGGER.debug(f"Received {len(self.trimmed_mask.keys())} trimmed masks")

        self.weights = {}
        for ii, m in enumerate(weights):
            try:
                len(m)
                self.set_weights(m[:], bin=ii)
            except TypeError:
                self.set_weights(weights[:], bin=0)
                break
        LOGGER.debug(f"Received {len(self.weights.keys())} weight maps")

        self.gamma_1 = {}
        self.gamma_2 = {}
        for ii, m in enumerate(gamma_1):
            try:
                len(m)
                self.set_shear_maps(m[:], gamma_2[ii][:], bin=ii)
            except TypeError:
                self.set_shear_maps(gamma_1[:], gamma_2[:], bin=0)
                break
        LOGGER.debug(f"Received {len(self.gamma_1.keys())} shear maps")

        self.kappa_E = {}
        for ii, m in enumerate(kappa_E):
            try:
                len(m)
                self.set_convergence_maps(m[:], None, bin=ii)
            except TypeError:
                self.set_convergence_maps(kappa_E[:], None, bin=0)
                break
        LOGGER.debug(
            f"Received {len(self.kappa_E.keys())} E mode convergence maps")

        self.kappa_B = {}
        for ii, m in enumerate(kappa_B):
            try:
                len(m)
                self.set_convergence_maps(None, m[:], bin=ii)
            except TypeError:
                self.set_convergence_maps(None, kappa_B[:], bin=0)
                break
        LOGGER.debug(
            f"Received {len(self.kappa_B.keys())} B mode convergence maps")

    # ACCESING OBJECTS

    def get_shear_maps(self, trimming=False, bin=0, use_B_modes=False):
        """
        Returns the shear maps. If they are not set tries to
        calculate from internal convergence maps.

        :param trimming: If True apply trimmed mask instead of normal mask to
                         get rid of pixels close to the edges of the mask.
                         If False just the normal mask is applied.
        :param bin: Index of the map instance (starting at 0)
        :param use_B_modes: If True uses B mode convergence maps
                            instead of E modes.
        """
        if len(self.gamma_1.keys()) == 0:
            LOGGER.warning(
                "No shear maps set. Attempting to calculate them from "
                "the convergence maps.")
            gamma_1, gamma_2 = self._convert_kappa_to_gamma(
                bin=bin, trimming=trimming, use_B_modes=use_B_modes)
        elif (len(self.gamma_1[bin]) == 0) | (len(self.gamma_2[bin]) == 0):
            LOGGER.warning(
                "No shear maps set. Attempting to calculate them from "
                "the convergence maps.")
            gamma_1, gamma_2 = self._convert_kappa_to_gamma(
                bin=bin, trimming=trimming, use_B_modes=use_B_modes)
        else:
            gamma_1 = self.gamma_1[bin]
            gamma_2 = self.gamma_2[bin]
        return (gamma_1[:], gamma_2[:])

    def get_weights(self, bin=0):
        """
        Returns the weight maps

        :param bin: Index of the map instance (starting at 0)
        """
        if bin not in self.weights.keys():
            raise IndexError(f"weights object instance {bin} not set.")
        return self.weights[bin][:]

    def get_mask(self, bin=0):
        """
        Returns the mask

        :param bin: Index of the map instance (starting at 0)
        """
        if bin not in self.mask.keys():
            raise IndexError(f"mask object instance {bin} not set.")
        return self.mask[bin][:]

    def get_trimmed_mask(self, bin=0):
        """
        Returns the trimmed mask

        :param bin: Index of the map instance (starting at 0)
        """
        if bin not in self.trimmed_mask.keys():
            raise IndexError(f"trimmed mask object instance {bin} not set.")
        return self.trimmed_mask[bin][:]

    def get_convergence_maps(self, trimming=False, bin=0):
        """
        Returns the convergence maps (E and B mode maps).
        If not set tries to calculate from the internal shear maps.

        :param trimming: If True apply trimmed mask instead of normal mask to
                         get rid of pixels close to mask edge.
                         If False just the normal mask is applied.
        :param bin: Index of the map instance (starting at 0)
        """
        if len(self.kappa_E.keys()) == 0:
            LOGGER.warning(
                "Convergence maps not set. Calculating from "
                "internal shear maps.")
            kappa_E, kappa_B = self._convert_gamma_to_kappa(
                bin=bin, trimming=trimming)
        elif (len(self.kappa_E[bin]) == 0) & (len(self.kappa_B[bin]) == 0):
            LOGGER.warning(
                "Convergence maps not set. Calculating from "
                "internal shear maps.")
            kappa_E, kappa_B = self._convert_gamma_to_kappa(
                bin=bin, trimming=trimming)
        elif len(self.kappa_E[bin]) == 0:
            LOGGER.warning("Only B mode convergence map found.")
            kappa_B = self.kappa_B[bin]
            return kappa_B
        elif len(self.kappa_B[bin]) == 0:
            kappa_E = self.kappa_E[bin]
            return kappa_E
        else:
            kappa_E = self.kappa_E[bin]
            kappa_B = self.kappa_B[bin]
        return (kappa_E[:], kappa_B[:])

    # SETTING OBJECTS

    def set_shear_maps(self, shear_1=[], shear_2=[], bin=0):
        """
        Sets the shear maps

        :param shear_1: First shear map component
        :param shear_2: binond shear map component
        :param bin: Index of the map instance (starting at 0)
        """
        shear_1 = np.asarray(shear_1, dtype=self.ctx['prec'])
        shear_2 = np.asarray(shear_2, dtype=self.ctx['prec'])

        self.gamma_1[bin] = self._apply_mask(
            shear_1, bin=bin, obj_name='shear 1, instance {}'.format(bin))
        self.gamma_2[bin] = self._apply_mask(
            shear_2, bin=bin, obj_name='shear 2, intance {}'.format(bin))
        LOGGER.debug("Set shear maps for instance {}".format(bin))

    def set_convergence_maps(self, kappa_E=[], kappa_B=[], bin=0):
        """
        Sets the convergence E and B maps

        :param kappa_E: E mode convergence map
        :param kappa_B: B mode convergence map
        :param bin: Index of the map instance (starting at 0)
        """
        if kappa_E is not None:
            kappa_E = np.asarray(kappa_E, dtype=self.ctx['prec'])
            self.kappa_E[bin] = self._apply_mask(
                kappa_E,
                obj_name='convergence E-modes, instance {}'.format(bin),
                bin=bin)
        if kappa_B is not None:
            kappa_B = np.asarray(kappa_B, dtype=self.ctx['prec'])
            self.kappa_B[bin] = self._apply_mask(
                kappa_B,
                obj_name='convergence B-modes, instance {}'.format(bin),
                bin=bin)
        LOGGER.debug("Set convergence maps for instance {}".format(bin))

    def set_weights(self, weights=[], bin=0):
        """
        Sets the weight map

        :param weights: The weight map
        :param bin: Index of the map instance (starting at 0)
        """
        weights = np.asarray(weights, dtype=self.ctx['prec'])
        self.weights[bin] = self._apply_mask(
            weights, obj_name='weights, instance {}'.format(bin), bin=bin)
        LOGGER.debug("Set weights for instance{}".format(bin))

    def set_mask(self, mask=[], bin=0, apply=True):
        """
        Sets the mask

        :param mask: The mask to set
        :param bin: Index of the map instance (starting at 0)
        :param apply: If True directly applies the set mask to the weights,
                      convergence maps and shear maps
        """
        mask = np.asarray(mask, dtype=bool)

        self.mask[bin] = mask
        LOGGER.debug("Set mask for instance {}".format(bin))
        if apply:
            LOGGER.info(
                f"Applying internal mask for instance {bin} "
                f"to all maps of instance {bin}")
            self.weights[bin] = self._apply_mask(
                self.weights[bin], bin=bin,
                obj_name='weights, instance {}'.format(bin))
            self.gamma_1[bin] = self._apply_mask(
                self.gamma_1[bin], bin=bin,
                obj_name='shear 1, instance {}'.format(bin))
            self.gamma_2[bin] = self._apply_mask(
                self.gamma_2[bin], bin=bin,
                obj_name='shear 2. instance {}'.format(bin))
            self.kappa_E[bin] = self._apply_mask(
                self.kappa_E[bin], bin=bin,
                obj_name='convergence E, instance {}'.format(bin))
            self.kappa_B[bin] = self._apply_mask(
                self.kappa_B[bin], bin=bin,
                obj_name='convergence B, instance {}'.format(bin))

    def set_trimmed_mask(self, trimmed_mask=[], bin=0, apply=False):
        """
        Sets the trimmed mask

        :param trimmed_mask: The trimmed mask to set
        :param bin: Index of the map instance (starting at 0)
        :param apply: If True directly applies the set mask to the weights,
                      convergence maps and shear maps
        """
        mask = np.asarray(trimmed_mask, dtype=bool)

        self.trimmed_mask[bin] = mask
        LOGGER.debug("Set trimmed mask for instance {}".format(bin))
        if apply:
            LOGGER.info(
                f"Applying internal trimmed mask for instance {bin} "
                f"to all maps of instance {bin}")
            self.weights[bin] = self._apply_mask(
                self.weights[bin], bin=bin,
                obj_name='weights, instance {}'.format(bin),
                trimming=True)
            self.gamma_1[bin] = self._apply_mask(
                self.gamma_1[bin], bin=bin,
                obj_name='shear 1, instance {}'.format(bin),
                trimming=True)
            self.gamma_2[bin] = self._apply_mask(
                self.gamma_2[bin], bin=bin,
                obj_name='shear 2, instance {}'.format(bin),
                trimming=True)
            self.kappa_E[bin] = self._apply_mask(
                self.kappa_E[bin], bin=bin,
                obj_name='convergence E, instance {}'.format(bin),
                trimming=True)
            self.kappa_B[bin] = self._apply_mask(
                self.kappa_B[bin], bin=bin,
                obj_name='convergence B,, instance {}'.format(bin),
                trimming=True)

    # METHODS
    def convert_shear_to_convergence(self, bin=0, trimming=True):
        """
        Calculates convergence maps from the shear maps and sets them
        (retrieve with get_convergence_maps).

        :param bin: Index of the map instance (starting at 0)
        :param trimming: If True apply trimmed mask instead of normal mask to
                         get rid of pixels close to mask edge.
        """
        kappa_E, kappa_B = self._convert_gamma_to_kappa(
            bin=bin, trimming=trimming)
        self.kappa_E[bin] = kappa_E
        self.kappa_B[bin] = kappa_B

    def convert_convergence_to_shear(self, bin=0, trimming=True,
                                     use_B_modes=False):
        """
        Calculates shear maps from the convergence maps and sets them
        (retrieve with get_shear_maps).

        :param bin: Index of the map instance (starting at 0)
        :param trimming: If True apply trimmed mask instead of normal mask to
                         get rid of pixels close to mask edge.
        :param use_B_modes: If True uses B mode convergence maps
                            instead of E modes.
        """
        gamma_1, gamma_2 = self._convert_kappa_to_gamma(
            bin=bin, trimming=trimming, use_B_modes=use_B_modes)

        self.gamma_1[bin] = gamma_1
        self.gamma_2[bin] = gamma_2

    def smooth_maps(self, fwhm=0.0, bin=0):
        """
        Smooth the convergence maps with a Gaussian kernel

        :param fwhm: The FWHM of the smoothing kernel in arcmins
        :param bin: Index of the map instance (starting at 0)
        """

        if bin not in self.kappa_E.keys():
            raise IndexError(
                f"convergence E mode object instance {bin} not set.")
        if bin not in self.kappa_B.keys():
            raise IndexError(
                f"convergence B mode object instance {bin} not set.")
        kappa_E = self.kappa_E[bin]
        kappa_B = self.kappa_B[bin]

        if bin not in self.kappa_E.keys():
            LOGGER.warning(
                f"No E mode convergence map for instance {bin} "
                "found. Not smoothing.")
        else:
            kappa_E = self.kappa_E[bin]
            if fwhm > 0.0:
                kappa_E = np.asarray(
                    hp.sphtfunc.smoothing(
                        kappa_E,
                        fwhm=np.radians(float(fwhm) / 60.), lmax=self.lmax),
                    dtype=self.ctx['prec'])
            kappa_E = self._apply_mask(
                kappa_E, bin=bin, obj_name='convegence E-modes')
            self.kappa_E[bin] = kappa_E
            LOGGER.info(
                f"Smoothed E mode convergence maps "
                f"for instance {bin} with a Gaussian "
                f"smoothing kernel with a FWHM of {fwhm} arcmin")

        if bin not in self.kappa_B.keys():
            LOGGER.warning(
                f"No B mode convergence map for instance {bin} "
                "found. Not smoothing.")
        else:
            kappa_B = self.kappa_B[bin]
            if fwhm > 0.0:
                kappa_B = np.asarray(
                    hp.sphtfunc.smoothing(
                        kappa_B,
                        fwhm=np.radians(float(fwhm) / 60.), lmax=self.lmax),
                    dtype=self.ctx['prec'])
            kappa_B = self._apply_mask(
                kappa_B, bin=bin, obj_name='convegence B-modes')
            self.kappa_B[bin] = kappa_B
            LOGGER.info(
                f"Smoothed B mode convergence maps "
                f"for instance {bin} with a Gaussian "
                f"smoothing kernel with a FWHM of {fwhm} arcmin")

    def calc_summary_stats(self, statistics, extra_mask={},
                           extra_trimmed_mask={}, scales=[],
                           use_shear_maps=False, use_kappa_maps=False,
                           output_dir='.',
                           defined_parameters={},
                           undefined_parameters=[],
                           name='', copy_obj=True, write_to_file=False,
                           method='KS', cross_bins=[0, 1], bin=0,
                           trimming=True):
        """
        Calculates the summary statistics from the maps
        Can provide a mask or trimmed_mask which will be used instead of the
        internal masks, allowing to store multiple cutouts on a single map
        (can save memory)

        :param statistics: Statistcs to calculate.
        :param mask: Can provide an additional mask, otherwise internal mask
                     used
        :param trimmed_mask: Can provide an additional trimmed mask
        :param scales: Smoothing scales to apply for multiscale analysis for
                       Non-Gaussian statistics (multi type) (FWHM in arcmins).
                       If not given uses internal scales from context
        :param use_shear_maps: If set to True will calculate convergence maps
                               from shear maps for convergence map based
                               statistics. Otherwise uses
                               the convergence maps directly.
        :param use_kappa_maps: If set to True will calculate shear maps
                               from kappa maps for shear map based
                               statistics. Otherwise uses
                               the shear maps directly.
        :param output_dir: If write_to_file is True used to build the output
                           path. See ekit docs.
        :param defined_parameters: If write_to_file is True used to build the
                                   output path. See ekit docs
        :param undefined_parameters: If write_to_file is True used to build
                                     the output path. See ekit docs
        :param name: If write_to_file is True used to build the output
                     path. See ekit docs
        :param copy_obj: If True preserves the map objects, otherwise
                         overwrites them with masked maps in the extraction
                         process
        :param write_to_file: If True appends to files directly instead of
                              returning the results as a dictionary
        :param method: Mass mapping method.
                       Currently only Kaiser-Squires supported.
        :param cross_bins: For cross-statistics can indicate which map
                           instances to use.
        :param bin: For single bin statistics can indicate which map
                    instance to use.
        :param trimming: If True uses trimmed mask for convergence statistics.
        """

        if len(statistics) == 0:
            LOGGER.warning("Nothing to compute")
            return

        if copy_obj:
            kappa_E_save = copy.deepcopy(self.kappa_E)
            kappa_B_save = copy.deepcopy(self.kappa_B)
            gamma_1_save = copy.deepcopy(self.gamma_1)
            gamma_2_save = copy.deepcopy(self.gamma_2)
            weights_save = copy.deepcopy(self.weights)
        else:
            LOGGER.warning(
                "Using internal map objects directly and potentially "
                "overwriting them! Do not use this mode if you wish to "
                "further use the map objects of this map instance. "
                "Also make sure that your statistic plugins do not overwrite "
                "maps.")

        if len(scales) == 0:
            LOGGER.debug("Using internal scales")
            scales = self.ctx['scales']

        if 'tomo' in defined_parameters.keys():
            self.ctx['tomo'] = defined_parameters['tomo']
        else:
            self.ctx['tomo'] = '0x0'

        stats = self._get_pol_stats(statistics)

        # divide statistics into classes
        statistic_divided = self._divide_statistics(stats)
        check_shear_maps = False
        check_kappa_maps = False
        for stat_set in statistic_divided['E'].items():
            LOGGER.debug(
                f"Got statistics {stat_set[1]} "
                f"for statistic type {stat_set[0]}")
            if (stat_set[0] == 'shear'):
                if (len(stat_set[1]) > 0):
                    if use_kappa_maps:
                        check_kappa_maps = True
                    else:
                        check_shear_maps = True
            else:
                if (len(stat_set[1]) > 0):
                    if use_shear_maps:
                        check_shear_maps = True
                    else:
                        check_kappa_maps = True

        # import statistics plugins
        plugins = {}
        for statistic in stats['E']:
            LOGGER.debug(f"Importing statistics plugin {statistic}")
            plugins[statistic] = utils.import_executable(
                statistic, statistic)

        # set polarizations
        polarizations = []
        if (self.ctx['polarizations'] == 'A') | \
           (self.ctx['polarizations'] == 'E'):
            polarizations.append('E')
        if (self.ctx['polarizations'] == 'A') | \
           (self.ctx['polarizations'] == 'B'):
            polarizations.append('B')

        # decide how many maps need to be ran
        full = False
        cross = False
        for stat in statistics:
            if 'Cross' in stat:
                cross = True
            if 'Full' in stat:
                full = True
        if cross | full:
            if full:
                if check_shear_maps:
                    map_keys_shear = np.asarray(
                        list(self.gamma_1.keys()), dtype=int)
                else:
                    map_keys_shear = np.zeros(0, dtype=int)
                if check_kappa_maps:
                    map_keys_kappa = np.asarray(
                        list(self.kappa_E.keys()), dtype=int)
                else:
                    map_keys_kappa = np.zeros(0, dtype=int)
                map_keys = np.append(
                    map_keys_shear, map_keys_kappa)
                map_keys = np.unique(map_keys)
            else:
                map_keys = np.asarray(cross_bins, dtype=int)
        else:
            map_keys = np.asarray([bin], dtype=int)

        # check if required maps are available
        if check_shear_maps:
            for key in map_keys:
                if key not in self.gamma_1.keys():
                    raise Exception(
                        f"Shear maps for instance {key} not available. "
                        "Cannot calculate statistics.")
                if key not in self.gamma_2.keys():
                    raise Exception(
                        f"Shear maps for instance {key} not available. "
                        "Cannot calculate statistics.")
        if check_kappa_maps:
            for key in map_keys:
                if 'E' in polarizations:
                    if key not in self.kappa_E.keys():
                        raise Exception(
                            f"Convergence E mode map for instance {key} "
                            "not available."
                            "Pass them on initialization or "
                            "set use_shear_maps=True.")
                if 'B' in polarizations:
                    if key not in self.kappa_B.keys():
                        raise Exception(
                            f"Convergence B mode map for instance {key} "
                            "not available."
                            "Pass them on initialization or "
                            "set use_shear_maps=True.")

        mask = {}
        if not isinstance(extra_mask, dict):
            # if array was passed
            mask[0] = extra_mask
        else:
            for key in extra_mask.keys():
                mask[key] = extra_mask[key]
        for key in map_keys:
            if key not in mask.keys():
                mask[key] = []

        trimmed_mask = {}
        if not isinstance(extra_trimmed_mask, dict):
            # if array was passed
            trimmed_mask[0] = extra_trimmed_mask
        else:
            for key in extra_trimmed_mask.keys():
                trimmed_mask[key] = extra_trimmed_mask[key]
        for key in map_keys:
            if key not in trimmed_mask.keys():
                trimmed_mask[key] = []

        # first masking
        if check_shear_maps:
            for key in map_keys:
                self.gamma_1[key] = self._apply_mask(
                    self.gamma_1[key], mask=mask[key], bin=key,
                    obj_name=f'shear 1 instance {key}')
                self.gamma_2[key] = self._apply_mask(
                    self.gamma_2[key], mask=mask[key], bin=key,
                    obj_name=f'shear 2, instance {key}')
        if check_kappa_maps:
            for key in map_keys:
                if 'E' in polarizations:
                    self.kappa_E[key] = self._apply_mask(
                        self.kappa_E[key], mask=mask[key],
                        obj_name=f'convergence E modes instance {key}',
                        trimming=False)
                if 'B' in polarizations:
                    self.kappa_B[key] = self._apply_mask(
                        self.kappa_B[key], mask=mask[key],
                        obj_name=f'convergence B modes instance {key}',
                        trimming=False)

        # masking weights
        for key in map_keys:
            if key not in self.weights.keys():
                # if weight map does not exist create equally weighted map
                LOGGER.warning(
                    f"Weights not set for instance {key}. "
                    "Using equal weighting.")
                if check_shear_maps:
                    weights = np.zeros_like(self.gamma_1[0], dtype=bool)
                    weights[self.gamma_1[0] > hp.UNSEEN] = True
                else:
                    if 'E' in polarizations:
                        weights = np.zeros_like(self.kappa_E[0], dtype=bool)
                        weights[self.kappa_E[0] > hp.UNSEEN] = True
                    else:
                        weights = np.zeros_like(self.kappa_B[0], dtype=bool)
                        weights[self.kappa_B[0] > hp.UNSEEN] = True
                self.weights[key] = weights
            self.weights[key] = self._apply_mask(
                self.weights[key], mask=mask[key],
                obj_name=f'weights, instance {key}',
                trimming=False)

        # collector array for outputs
        outs = {}

        ##################
        # shear statistics
        ##################
        if len(statistic_divided['E']['shear']) > 0:
            LOGGER.debug("Calculating shear statistics")
            outs = self._calc_shear_stats(statistic_divided['E']['shear'],
                                          plugins, outs, polarizations,
                                          mask, trimmed_mask,
                                          write_to_file, name,
                                          output_dir, defined_parameters,
                                          undefined_parameters, map_keys,
                                          use_shear_maps, cross_bins, bin,
                                          use_kappa_maps, trimming)

        kappa_stats = []
        for pol in polarizations:
            kappa_stats += statistic_divided[pol]['convergence']
            kappa_stats += statistic_divided[pol]['convergence-cross']
            kappa_stats += statistic_divided[pol]['multi']
        full_mode = False
        cross_mode = False
        for stat in kappa_stats:
            if 'Cross' in stat:
                cross_mode = True
            if 'Full' in stat:
                full_mode = True

        if len(kappa_stats) > 0:
            LOGGER.debug("Preparing alms")
            alm = self._prep_alms(trimmed_mask, polarizations,
                                  use_shear_maps, method=method,
                                  map_keys=map_keys,
                                  cross_bins=cross_bins, bin=bin,
                                  full_mode=full_mode, cross_mode=cross_mode,
                                  trimming=trimming)
            for pol in polarizations:
                ########################
                # convergence statistics
                ########################
                if (len(statistic_divided[pol]['convergence']) > 0):
                    LOGGER.debug(
                        "Calculating convergence statistics for polarization "
                        "{}".format(pol))
                    outs = self._calc_convergence_stats(
                        outs, plugins, alm[pol],
                        trimmed_mask, mask,
                        defined_parameters,
                        undefined_parameters, output_dir,
                        statistic_divided[pol]['convergence'],
                        pol, write_to_file, name, map_keys, cross_bins, bin,
                        trimming)

                if (len(statistic_divided[pol]['convergence-cross']) > 0):
                    LOGGER.debug(
                        "Calculating cross-convergence statistics for "
                        "polarization {}".format(pol))
                    outs = self._calc_cross_convergence_stats(
                        outs, plugins, alm[pol],
                        trimmed_mask, mask,
                        defined_parameters,
                        undefined_parameters, output_dir,
                        statistic_divided[pol]['convergence-cross'],
                        pol, write_to_file, name, cross_bins, trimming)

                ###################################
                # multiscale convergence statistics
                ###################################
                if len(statistic_divided[pol]['multi']) > 0:
                    LOGGER.debug(
                        "Calculating multi statistics for polarization "
                        "{}".format(pol))
                    outs = self._calc_multi_stats(
                        outs, scales, plugins, alm[pol],
                        trimmed_mask, mask,
                        defined_parameters,
                        undefined_parameters, output_dir,
                        statistic_divided[pol]['multi'],
                        pol, write_to_file, name, map_keys,
                        statistics, cross_bins, bin, trimming)

        # restore
        if copy_obj:
            self.kappa_E = kappa_E_save
            self.kappa_B = kappa_B_save
            self.gamma_2 = gamma_1_save
            self.gamma_1 = gamma_2_save
            self.weights = weights_save
        return outs

    ##################################
    # HELPER FUNCTIONS
    ##################################

    def _stack_stats(self, stat_out, pol, statistic, all_statistics, outs,
                     store_to_files=False, name='', output_dir='',
                     defined_parameters={}, undefined_parameters=[]):
        """
        Stack the extracted summary statistics for the output
        """
        # Init Polariazation dict if non existent
        if pol not in outs.keys():
            outs[pol] = {}

        if statistic == 'Extremes':
            if ('Peaks' in all_statistics) | ('2PCF' in all_statistics):
                out = stat_out[0:2]
                stat = 'Peaks'
                outs = self._stack_stats(out, pol, stat, all_statistics, outs,
                                         store_to_files, name, output_dir,
                                         defined_parameters,
                                         undefined_parameters)
            if ('Voids' in all_statistics) | ('2VCF' in all_statistics):
                out = stat_out[2:4]
                stat = 'Voids'
                outs = self._stack_stats(out, pol, stat, all_statistics, outs,
                                         store_to_files, name, output_dir,
                                         defined_parameters,
                                         undefined_parameters)
        elif (statistic == 'Peaks') & (len(stat_out) == 2):
            if 'Peaks' in all_statistics:
                out = stat_out[0]
                stat = 'Peaks'
                outs = self._stack_stats(out, pol, stat, all_statistics, outs,
                                         store_to_files, name, output_dir,
                                         defined_parameters,
                                         undefined_parameters)
            if '2PCF' in all_statistics:
                out = stat_out[1]
                stat = '2PCF'
                outs = self._stack_stats(out, pol, stat, all_statistics, outs,
                                         store_to_files, name, output_dir,
                                         defined_parameters,
                                         undefined_parameters)
        elif (statistic == 'Voids') & (len(stat_out) == 2):
            if 'Voids' in all_statistics:
                out = stat_out[0]
                stat = 'Voids'
                outs = self._stack_stats(out, pol, stat, all_statistics, outs,
                                         store_to_files, name, output_dir,
                                         defined_parameters,
                                         undefined_parameters)
            if '2PCF' in all_statistics:
                out = stat_out[1]
                stat = '2VCF'
                outs = self._stack_stats(out, pol, stat, all_statistics, outs,
                                         store_to_files, name, output_dir,
                                         defined_parameters,
                                         undefined_parameters)
        else:
            if store_to_files:
                # adding a separation value
                if (statistic == '2PCF') | (statistic == '2PCF'):
                    stat_out = np.vstack(([[-999.0, -999.0]], stat_out))
                # saving
                output_path = paths.create_path(
                    name,
                    output_dir, {
                        **defined_parameters,
                        **{'mode': pol,
                           'stat': statistic}},
                    undefined_parameters,
                    suffix='.npy')
                if os.path.exists(output_path):
                    out_file = np.load(output_path)
                    out_file = np.vstack(
                        (out_file, stat_out))
                else:
                    out_file = stat_out
                np.save(output_path, out_file)
            else:
                # Init Statistics dict if non existent
                if statistic not in outs[pol].keys():
                    outs[pol][statistic] = stat_out
                else:
                    # adding a separation value
                    if (statistic == '2PCF') | (statistic == '2PCF'):
                        stat_out = np.vstack(([[-999.0, -999.0]], stat_out))

                    outs[pol][statistic] = np.vstack(
                        (outs[pol][statistic], stat_out))
        return outs

    def _convert_alm_to_kappa(self, alm, fwhm):
        """
        Converts spherical harmonics to E and B modes Convergence maps.
        Can also apply smoothing.
        """
        # smoothing alms with gaussian kernel
        if fwhm > 0.0:
            alm_ = hp.sphtfunc.smoothalm(
                alm, fwhm=np.radians(float(fwhm) / 60.), inplace=False)
        else:
            alm_ = copy.copy(alm)
        kappa = np.asarray(
            hp.alm2map(alm_, nside=self.ctx['NSIDE'], lmax=self.lmax),
            dtype=self.ctx['prec'])
        return kappa

    def _convert_gamma_to_kappa(self, bin=0, trimming=False, method='KS'):
        """
        Converts two shear maps to convergence maps (E and B modes).
        """
        # Do not touch
        sign_flip = True

        if bin not in self.gamma_1.keys():
            raise IndexError(f"shear 1 object instance {bin} not set.")
        gamma_1 = self.gamma_1[bin]
        if bin not in self.gamma_2.keys():
            raise IndexError(f"shear 2 object instance {bin} not set.")
        gamma_2 = self.gamma_2[bin]

        # spherical harmonics decomposition
        if sign_flip & (len(gamma_1) > 0):
            LOGGER.debug("Applying sign flip")
            gamma_1[gamma_1 > hp.UNSEEN] *= -1.
        alm_E, alm_B = utils._calc_alms(
            gamma_1, gamma_2, method=method, lmax=self.lmax)

        if sign_flip & (len(gamma_1) > 0):
            gamma_1[gamma_1 > hp.UNSEEN] *= -1.

        kappa_E = np.asarray(self._convert_alm_to_kappa(alm_E, fwhm=0.0),
                             dtype=self.ctx['prec'])
        kappa_B = np.asarray(self._convert_alm_to_kappa(alm_B, fwhm=0.0),
                             dtype=self.ctx['prec'])

        kappa_E = self._apply_mask(
            kappa_E, bin=bin, trimming=trimming,
            obj_name=f'convergence E-modes, instance {bin}')
        kappa_B = self._apply_mask(
            kappa_B, bin=bin, trimming=trimming,
            obj_name=f'convergence B-modes, instance {bin}')

        return kappa_E, kappa_B

    def _convert_kappa_to_gamma(self, bin=0, trimming=False,
                                use_B_modes=False):
        """
        Converts a kappa map to two shear maps using Kaiser-Squires
        """

        # Do not touch
        sign_flip = True

        if use_B_modes:
            if bin not in self.kappa_B.keys():
                raise IndexError(
                    f"Convergence B mode object instance {bin} not set.")
            kappa = self.kappa_B[bin]
        else:
            if bin not in self.kappa_E.keys():
                raise IndexError(
                    f"Convergence E mode object instance {bin} not set.")
            kappa = self.kappa_E[bin]

        # spherical harmonics decomposition
        kappa_alm = hp.map2alm(kappa, lmax=self.lmax)
        ell = hp.Alm.getlm(self.lmax)[0]
        ell[ell == 0] = 1

        # Add the apropriate factor to the kappa_alm
        fac = np.where(
            np.logical_and(ell != 1, ell != 0),
            - np.sqrt(((ell + 2.0) * (ell - 1)) / ((ell + 1) * ell)), 0)
        kappa_alm *= fac

        # Spin spherical harmonics
        # Q and U are the real and imaginary parts of the shear map
        T, Q, U = hp.alm2map([np.zeros_like(kappa_alm), kappa_alm,
                              np.zeros_like(kappa_alm)],
                             nside=self.ctx['NSIDE'], lmax=self.lmax)
        Q = np.asarray(Q, dtype=self.ctx['prec'])
        U = np.asarray(U, dtype=self.ctx['prec'])

        # - sign accounts for the Healpix sign flip
        if sign_flip:
            Q = -1. * Q

        gamma_1 = self._apply_mask(
            Q, trimming=trimming, bin=bin, obj_name=f'shear 1, instance {bin}')
        gamma_2 = self._apply_mask(
            U, trimming=trimming, bin=bin, obj_name=f'shear 2, instance {bin}')

        return (gamma_1, gamma_2)

    def _apply_mask(self, obj, bin=0, trimming=False, mask=[],
                    obj_name=''):
        """
        Apply masks to maps
        """

        if len(obj) == 0:
            LOGGER.debug(
                "Cannot apply mask to {} map since "
                "{} object not set. Ignoring...".format(obj_name, obj_name))
            return obj

        if len(mask) > 0:
            if len(mask) != len(obj):
                raise Exception(
                    "The mask and the object {} that you are trying to mask "
                    "do not have the same size!".format(obj_name))
            if 'weight' in obj_name:
                obj[np.logical_not(mask)] = 0.0
            else:
                obj[np.logical_not(mask)] \
                    = hp.pixelfunc.UNSEEN
            LOGGER.debug("Applied mask to object {}".format(obj_name))
        else:
            LOGGER.debug("Using internal masks for masking")
            try:
                if trimming:
                    if 'weight' in obj_name:
                        obj[np.logical_not(self.trimmed_mask[bin])] = 0.0
                    else:
                        obj[np.logical_not(self.trimmed_mask[bin])] \
                            = hp.pixelfunc.UNSEEN
                else:
                    if 'weight' in obj_name:
                        obj[np.logical_not(self.mask[bin])] = 0.0
                    else:
                        obj[np.logical_not(self.mask[bin])] \
                            = hp.pixelfunc.UNSEEN
            except KeyError:
                LOGGER.debug(
                    "No mask found to apply to {} map. Ignoring...".format(
                        obj_name))
        return obj

    def _calc_shear_stats(self, statistics, plugins, outs, pols,
                          mask=[], trimmed_mask=[],
                          write_to_file=False, name='',
                          output_dir='', defined_parameters={},
                          undefined_parameters=[], map_keys=[0],
                          use_shear_maps=False, cross_bins=[0, 1], bin=0,
                          use_kappa_maps=False, trimming=False):

        if len(statistics) == 0:
            return outs

        for stat in statistics:
            LOGGER.debug("Calculating shear statistic {}".format(stat))
            if 'Full' in stat:
                if use_kappa_maps:
                    for key in map_keys:
                        self.convert_convergence_to_shear(
                            bin=key, trimming=trimming)
                stat_out = plugins[stat](
                    self.gamma_1, self.gamma_2,
                    self.weights, self.ctx)
            elif 'Cross' in stat:
                if use_kappa_maps:
                    for key in cross_bins:
                        self.convert_convergence_to_shear(
                            bin=key, trimming=trimming)
                stat_out = plugins[stat](
                    self.gamma_1[cross_bins[0]], self.gamma_2[cross_bins[0]],
                    self.gamma_1[cross_bins[1]], self.gamma_2[cross_bins[1]],
                    self.weights[cross_bins[0]], self.weights[cross_bins[1]],
                    self.ctx)
            else:
                if use_kappa_maps:
                    self.convert_convergence_to_shear(
                        bin=bin, trimming=trimming)
                stat_out = plugins[stat](
                    self.gamma_1[bin], self.gamma_2[bin],
                    self.weights[bin], self.ctx)

            if 'E' in pols:
                outs = self._stack_stats(
                    stat_out[0], 'E', stat, [], outs,
                    write_to_file, name, output_dir,
                    defined_parameters, undefined_parameters)
            if 'B' in pols:
                outs = self._stack_stats(
                    stat_out[1], 'B', stat, [], outs,
                    write_to_file, name, output_dir,
                    defined_parameters, undefined_parameters)
        return outs

    def _get_pol_stats(self, statistics):
        stats_ = copy.copy(statistics)
        stats = {}
        stats['E'] = copy.copy(stats_)
        stats['B'] = copy.copy(stats_)
        return stats

    def _calc_convergence_stats(self, outs, plugins, alm,
                                trimmed_mask, mask,
                                defined_parameters,
                                undefined_parameters, output_dir,
                                stats, pol,
                                write_to_file, name, map_keys,
                                cross_bins=[0, 1], bin=0, trimming=False):
        if len(stats) == 0:
            return outs

        full_mode = False
        cross_mode = False
        for stat in stats:
            if 'Full' in stat:
                full_mode = True
            elif 'Cross' in stat:
                cross_mode = True
        if full_mode:
            keys = map_keys
        elif cross_mode:
            keys = cross_bins
        else:
            keys = [bin]

        # get unsmoothed kappa maps
        kappa_unsmoothed = {}
        for key in keys:
            if pol == 'E':
                if key in self.kappa_E:
                    # if kappa map exists use directly
                    kappa_unsmoothed[key] = self.kappa_E[key]
                else:
                    # convert alm to kappa
                    kappa_unsmoothed[key] = self._convert_alm_to_kappa(
                        alm[key], 0.0)
            else:
                if key in self.kappa_B:
                    # if kappa map exists use directly
                    kappa_unsmoothed[key] = self.kappa_B[key]
                else:
                    # convert alm to kappa
                    kappa_unsmoothed[key] = self._convert_alm_to_kappa(
                        alm[key], 0.0)

        # masking
        if trimming:
            for key in keys:
                kappa_unsmoothed[key] = self._apply_mask(
                    kappa_unsmoothed[key], mask=trimmed_mask[key],
                    trimming=True,
                    obj_name='convergence {}-modes instance {}'.format(
                        pol, key))
        else:
            for key in keys:
                kappa_unsmoothed[key] = self._apply_mask(
                    kappa_unsmoothed[key], mask=mask[key],
                    trimming=False,
                    obj_name='convergence {}-modes instance {}'.format(
                        pol, key))

        for stat in stats:
            LOGGER.debug("Calculating statistic {}".format(stat))
            if 'Full' in stat:
                stat_out = plugins[stat](
                    kappa_unsmoothed,
                    self.weights, self.ctx)
            elif 'Cross' in stat:
                stat_out = plugins[stat](
                    kappa_unsmoothed[cross_bins[0]],
                    kappa_unsmoothed[cross_bins[1]],
                    self.weights[cross_bins[0]],
                    self.weights[cross_bins[1]], self.ctx)
            else:
                stat_out = plugins[stat](
                    kappa_unsmoothed[bin],
                    self.weights[bin], self.ctx)
            outs = self._stack_stats(
                stat_out, pol, stat, [], outs,
                write_to_file, name, output_dir,
                defined_parameters, undefined_parameters)
        return outs

    def _calc_cross_convergence_stats(self, outs, plugins, alm,
                                      trimmed_mask, mask,
                                      defined_parameters,
                                      undefined_parameters, output_dir,
                                      stats, pol,
                                      write_to_file, name,
                                      cross_bins=[0, 1], trimming=False):
        if len(stats) == 0:
            return outs

        kappa_cross = self._convert_alm_to_kappa(
            np.sqrt(alm[cross_bins[cross_bins[0]]])
            * np.sqrt(alm[cross_bins[cross_bins[1]]]), 0.0)

        # masking
        if trimming:
            for key in cross_bins:
                kappa_cross = self._apply_mask(
                    kappa_cross, mask=trimmed_mask[key], trimming=True,
                    obj_name='convergence {}-modes'.format(pol))
        else:
            for key in cross_bins:
                kappa_cross = self._apply_mask(
                    kappa_cross, mask=mask[key], trimming=False,
                    obj_name='convergence {}-modes'.format(pol))

        # take average of the weights and mask again
        weights = (self.weights[cross_bins[0]]
                   + self.weights[cross_bins[1]]) / 2.
        if trimming:
            for key in cross_bins:
                weights = self._apply_mask(
                    weights, mask=trimmed_mask[key], obj_name='weights',
                    trimming=True)
        else:
            for key in cross_bins:
                weights = self._apply_mask(
                    weights, mask=mask[key], obj_name='weights',
                    trimming=False)

        for stat in stats:
            LOGGER.debug("Calculating statistic {}".format(stat))
            if 'Cross' in stat:
                stat_out = plugins[stat](
                    kappa_cross, weights, self.ctx)
            else:
                raise Exception(
                    "If the stat_type is convergence-cross the "
                    "statistic must also be a cross statistic!")
            outs = self._stack_stats(
                stat_out, pol, stat, [], outs,
                write_to_file, name, output_dir,
                defined_parameters, undefined_parameters)
        return outs

    def _divide_statistics(self, stats):
        stat_types = {'E': {}, 'B': {}}
        for key in ['shear', 'convergence', 'convergence-cross', 'multi']:
            stats_ = np.asarray(
                list(self.ctx['stat_types'].values())) == key
            stats_ = np.asarray(
                list(self.ctx['stat_types'].keys()))[stats_]
            stat_types['E'][key] = []
            stat_types['B'][key] = []
            for stat in stats_:
                if stat in stats['E']:
                    stat_types['E'][key].append(stat)
                if stat in stats['B']:
                    stat_types['B'][key].append(stat)
        return stat_types

    def _prep_alms(self, trimmed_mask, polarizations,
                   use_shear_maps, method='KS', map_keys=[0],
                   cross_bins=[0, 1], bin=0,
                   full_mode=False, cross_mode=False, trimming=False):

        # Do not touch
        sign_flip = True
        alm = {'E': {}, 'B': {}}
        if full_mode:
            keys = map_keys
        elif cross_mode:
            keys = cross_bins
        else:
            keys = [bin]
        if use_shear_maps:
            # calculate spherical harmonics
            LOGGER.debug(
                "Calculating spherical harmonics "
                "decomposition of shear maps")
            for key in keys:
                if sign_flip:
                    self.gamma_1[key][self.gamma_1[key] > hp.UNSEEN] *= -1.
                a = utils._calc_alms(
                    self.gamma_1[key], self.gamma_2[key],
                    mode='A', method=method,
                    lmax=self.lmax)
                alm['E'][key] = a[0]
                alm['B'][key] = a[1]
                if sign_flip:
                    self.gamma_1[key][self.gamma_1[key] > hp.UNSEEN] *= -1.
        else:
            if 'E' in polarizations:
                for key in keys:
                    alm['E'][key] = hp.map2alm(
                        self.kappa_E[key], lmax=self.lmax)
            if 'B' in polarizations:
                for key in keys:
                    alm['B'][key] = hp.map2alm(
                        self.kappa_B[key], lmax=self.lmax)

        # trim weights
        if trimming:
            for key in keys:
                self.weights[key] = self._apply_mask(
                    self.weights[key], mask=trimmed_mask[key],
                    obj_name='weights', trimming=True)

        return alm

    def _calc_multi_stats(self,
                          outs, scales, plugins, alm,
                          trimmed_mask, mask,
                          defined_parameters,
                          undefined_parameters, output_dir,
                          stats, pol,
                          write_to_file, name, map_keys, statistics,
                          cross_bins=[0, 1], bin=0, trimming=False):

        if len(stats) == 0:
            return outs

        full_mode = False
        cross_mode = False
        norm_mode = False
        for stat in stats:
            if 'Full' in stat:
                full_mode = True
            elif 'Cross' in stat:
                cross_mode = True
            else:
                norm_mode = True

        for scale in scales:
            LOGGER.debug("Hitting on scale {}. Smoothing...".format(scale))
            self.ctx['scale'] = scale

            if full_mode:
                kappas = {}
                for key in map_keys:
                    kappas[key] = self._convert_alm_to_kappa(
                        alm[key], scale)
                    if trimming:
                        kappas[key] = self._apply_mask(
                            kappas[key], mask=trimmed_mask[key],
                            obj_name='kappa', trimming=True)
                    else:
                        kappas[key] = self._apply_mask(
                            kappas[key], mask=mask[key], obj_name='kappa',
                            trimming=False)
                for stat in stats:
                    if 'Full' in stat:
                        stat_out = plugins[stat](
                            kappas, self.weights, self.ctx)
                        outs = self._stack_stats(
                            stat_out, pol, stat, statistics, outs,
                            False, name, output_dir,
                            defined_parameters, undefined_parameters)

            if cross_mode:
                alm_cross = np.sqrt(alm[cross_bins[0]]) \
                    * np.sqrt(alm[cross_bins[1]])
                kappa = self._convert_alm_to_kappa(
                    alm_cross, scale)
                for key in cross_bins:
                    if trimming:
                        kappa = self._apply_mask(
                            kappa, mask=trimmed_mask[key], obj_name='kappa',
                            trimming=True)
                    else:
                        kappa = self._apply_mask(
                            kappa, mask=mask[key], obj_name='kappa',
                            trimming=False)
                weights = (self.weights[cross_bins[0]]
                           + self.weights[cross_bins[1]]) / 2.
                if trimming:
                    for key in cross_bins:
                        weights = self._apply_mask(
                            weights, mask=trimmed_mask[key],
                            obj_name='weights', trimming=True)
                else:
                    for key in cross_bins:
                        weights = self._apply_mask(
                            weights, mask=mask[key], obj_name='weights',
                            trimming=False)
                for stat in stats:
                    if 'Cross' in stat:
                        stat_out = plugins[stat](
                            kappa, weights, self.ctx)
                        outs = self._stack_stats(
                            stat_out, pol, stat, statistics, outs,
                            False, name, output_dir,
                            defined_parameters, undefined_parameters)

            if norm_mode:
                kappa = self._convert_alm_to_kappa(
                    alm[bin], scale)
                if trimming:
                    kappa = self._apply_mask(
                        kappa, mask=trimmed_mask[bin], obj_name='kappa',
                        trimming=True)
                else:
                    kappa = self._apply_mask(
                        kappa, mask=mask[bin], obj_name='kappa',
                        trimming=False)
                for stat in stats:
                    if ('Full' in stat) | ('Cross' in stat):
                        continue
                    else:
                        stat_out = plugins[stat](
                            kappa, self.weights[bin], self.ctx)
                        outs = self._stack_stats(
                            stat_out, pol, stat, statistics, outs,
                            False, name, output_dir,
                            defined_parameters, undefined_parameters)

        if write_to_file:
            # saving all scales at once
            for statistic in stats:
                output_path = paths.create_path(
                    name,
                    output_dir, {
                        **defined_parameters,
                        **{'mode': pol,
                           'stat': statistic}},
                    undefined_parameters,
                    suffix='.npy')
                if os.path.exists(output_path):
                    out_file = np.load(output_path)
                    out_file = np.vstack(
                        (out_file, outs[pol][statistic]))
                else:
                    out_file = outs[pol][statistic]
                np.save(output_path, out_file)
            return {}
        return outs
