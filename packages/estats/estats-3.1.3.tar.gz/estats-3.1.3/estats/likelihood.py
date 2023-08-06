# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import os
import pandas as pd
import numpy as np
import copy
from ekit import context
import ekit.paths as paths
import scipy
import scipy.special
from estats import utils
import pickle
from scipy.interpolate import LinearNDInterpolator
from ekit import logger
from tqdm import tqdm
# import numba as nb
LOGGER = logger.init_logger(__name__)

# optional imports
try:
    from sklearn.decomposition import PCA
    PCA_enable = True
except ImportError:
    LOGGER.warning("Did not find sklearn installation. "
                   "Cannot use PCA.")
    PCA_enable = False
try:
    from sklearn.gaussian_process import GaussianProcessRegressor
    import sklearn.gaussian_process.kernels as kernels
    GPR_enable = True
except ImportError:
    LOGGER.warning("Did not find sklearn installation. "
                   "Cannot use GPR emulator mode.")
    GPR_enable = False
try:
    import tensorflow as tf
    LOGGER.debug(f"TensorFlow version: {tf.__version__}")
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.models import Sequential
    from keras.layers.core import Dropout
    NN_enable = True
except ImportError:
    LOGGER.warning("Did not find tensorflow installation. "
                   "Cannot use NN emulator mode.")
    NN_enable = False
try:
    from pypolychord.priors import UniformPrior
    from pypolychord.priors import GaussianPrior
    poly_enable = False
except ImportError:
    LOGGER.warning(
        "Did not find polychord installation. "
        "Cannot evaluate prior in polychord mode "
        "without polychord being installed")
    poly_enable = False


class likelihood:

    """
    Class meant to perform parameter inference based on predictions
    of the data-vectors and covariance matrices at different parameter
    configurations.

    The main functionality is to calculate the negative logarithm of the
    likelihood at a given parameter configuration given a measurement
    data-vector.

    The parameter space is broken down into two parts called parameters and
    nuisances, that are treated differently.

    For the parameter part it is assumed that the space is sampled densly with
    simulations and an emulator is built from the simulations.

    For the nuisances it is assumed that only delta simulations at
    the fiducial parameter configuration are available where only this one
    parameters is varied. In this case polynomial scaling
    relations are fitted for each bin of the data vector that are used
    to describe the influence of the parameter when predicting the statistic.
    This implicitly assumes that these parameters are independent from all
    other parameters.

    The data vectors can also be compressed using PCA or MOPED compression.

    The most important functionalities are:

    - readin_interpolation_data:

        Loads data used for interpolation. The data is expected to be in a
        format as used by the estats.summary module.

    - convert_to_PCA_space:

        Builds PCA compression and converts all data vectors to PCA space.
        All output will be in PCA space afterwards.

    - convert_to_MOPED_space:

        Builds MOPED compression and converts all data vectors to MOPED space.
        Requires emulator to be built before.
        All output will be in MOPED space afterwards.

    - build_emulator:

        Builds the emulator for the parameter space used to interpolate
        the expected data-vectors between different
        parameter configurations. There are three different choices
        for the type of interpolator used at the moment:
        linear: Uses N-Dimensional linear interpolator
        GPR: Gaussian Process Regressor
        NN: Neural network

    - build_scalings:

        Builds the polynomial scaling realtions for the nuisance parameters
        individually for each
        data bin. A polynomial function is fitted for each bin and each
        nuisance parameter.

    - get_neg_loglikelihood:

        Returns negative logarithmic likelihood given a measurement data-vector
        at the location in parameter space indicated.

    The accepted keywords are:

    - statistic:

        default: Peaks

        choices: name of one of the statistic plugins

        Decides which statistic plugin to use. In the likelihood module only
        the filter function is used from the plugin.

    - parameters:

        default: [Om, s8]

        choices: list of strings

        The names of the parameters to consider

    - parameter_fiducials:

        default: [0.276, 0.811]

        choices: list of floats

        The default values of the parameters.
        Used to decide on the fiducial covariance matrix if no interpolation
        of the covariance matrix is used.

    - nuisances:

        default: [IA, m, z]

        choices: list of strings

        The names of the nuisance parameters to consider

    - nuisance_fiducials:

        default: [0.0, 0.0, 0.0]

        choices: list of floats

        The default values of the nuisance parameters.
        Used to decide on the fiducial covariance matrix if no interpolation
        of the covariance matrix is used.

    - n_tomo_bins:

        default: 3

        choices: integer

        The number of tomographic bins considered. Only needed if the special
        emulator is used or a statistic with the name Cross in it.

    - cross_ordering:

        default: []

        choices: a list of labels

        Indicates the order of the tomographic bin labels that is assumed in
        the filter function.

        The labels could be bin1xbin2 for example, and the corresponding
        cross_ordering could be [1x1, 1x2, 2x2, 2x3, 3x3].

    - multi_bin:

        default: [False, True, True]

        choices: A boolean list

        Indicates if a nuisance parameter in nuisances is a global parameter
        (False) or a corresponding parameter should be introduced for each
        tomographic bin (True).
    """

    def __init__(self, context_in={}, verbosity=3, **kwargs):
        """
        Initializes likelihhod instance

        :param context_in: Context instance
        :param verbosity: Verbosity level (0-4)
        """

        logger.set_logger_level(LOGGER, verbosity)

        LOGGER.debug("Initializing likelihood object")

        # setup context
        types = ['int', 'list', 'list', 'list',
                 'list', 'list', 'str', 'list', 'list']

        defaults = [3,
                    ['Omega0', 'Sigma8'], [0.276, 0.811],
                    ['IA', 'm', 'z'], [0.0, 0.0, 0.0],
                    [['flat', 0.07, 0.55], ['flat', 0.47, 1.2],
                     ['flat', -5.5, 5.5],
                     ['flat', -0.1, 0.1], ['flat', -0.1, 0.1]],
                    'Peaks', [], [False, True, True]]

        allowed = ['n_tomo_bins', 'parameters',
                   'parameter_fiducials', 'nuisances', 'nuisance_fiducials',
                   'prior_configuration', 'statistic',
                   'cross_ordering', 'multi_bin']

        allowed, types, defaults = utils._get_plugin_contexts(
            allowed, types, defaults)
        self.ctx = context.setup_context(
            {**context_in, **kwargs}, allowed, types, defaults)

    # GET OBJECTS
    def get_meta(self, params=None):
        """
        Access the meta data table

        :param: params: Dictionary or list of paramters for filtering.
        :return: (Filtered) meta data
        """

        if params is None:
            meta = self.META[:]
        else:
            dict = self._convert_dict_list(params, 'dict')
            idx = self._get_loc(dict)
            meta = self.META[idx]
        if self.input_normalizer is not None:
            LOGGER.debug("Applying normalization")
            meta = self.input_normalizer(meta)
        return meta

    def get_means(self, params=None):
        """
        Access the mean data vectors stored.

        :param: params: Dictionary or list of paramters for filtering.
        :return: Original means
        """
        if params is None:
            means = self.MEANS
        else:
            dict_ = self._convert_dict_list(params, 'dict')

            dict = {}
            for d in dict_.items():
                if (d[0] in self.ctx['parameters']) \
                        | (d[0] in self.ctx['nuisances']):
                    dict[d[0]] = d[1]
            idx = self._get_loc(dict)
            means = self.MEANS[idx, :]
        means = self.transform_datavectors(means)
        return means

    def get_interp_means(self, params):
        """
        Predict interpolated datavector at a parameter configuration.

        :param: params: Dictionary or list of paramters for filtering.
        :return: Interpolated data vector
        """
        list = self._convert_dict_list(params, 'list')
        mean = self._get_interp_data_vector(list)
        return mean

    # METHODS
    def transform_datavectors(self, vecs):
        """
        Applies all the available modifications to raw data vectors,
        meaning normalization, filtering, PCA and MOPED compression
        in this exact order.

        :param vecs: Raw data vectors that should be tranformed.
        :return : The transformed data vectors
        """

        vecs = np.atleast_2d(vecs)
        vecs_out = np.zeros(
            (vecs.shape[0], self._transform_datavector(vecs[0]).shape[1]))
        for ii, vec in enumerate(vecs):
            vecs_out[ii] = self._transform_datavector(vec)
        return vecs_out

    def clear_redundant_data(self):
        """
        Clear out large arrays that are no longer needed after emulator and
        interpolator are built.
        """
        self.MEANS = []
        self.META = []
        self.ERRORS = []
        self.FIDUCIAL_DATA = []
        LOGGER.debug("Deleted MEANS, META, ERRORS and FIDUCIAL_DATA")

    def convert_to_PCA_space(self, PCA_cache_path=None, inc_var=99.999,
                             truncate=0, build_precision_matrix=False,
                             check_inversion=True, neglect_correlation=False,
                             partial_PCA=False):
        """
        Builds PCA compression matrix.
        All results are returned in MOPED space afterwards.

        :param PCA_cache_path: Alternatively provide PCA basis directly via
                         pickle file. If path does not exist will cache
                         built basis to there.
        :param inc_var: Amount of variance included in the PCA in percent.
        :param truncate: Maximum number of PCA components to keep.
                         Overrides inc_var.
        :param build_precision_matrix: To build precision matrix from
                                       fdicuial_data_path realisations.
        :param check_inversion: If True checks numerical stability of inversion
                                of the fiducial covariance matrix
        :param neglect_correlation: Reduces the covariance matrix to its
                                    diagonal
        :param partial_PCA: If True builds a PCA compression for each
                            statistic otherwise builds a single one for
                            the whole statistic (only used in case of a
                            combined statistic)
        """

        if not PCA_enable:
            raise Exception(
                "Cannot use PCA compression if sklearn not installed.")

        if hasattr(self, 'MOPED_matrix'):
            raise Exception(
                "Cannot build PCA on top of MOPED compression!.")

        if PCA_cache_path is None:
            self._build_PCA_basis(
                truncate=truncate, inc_var=inc_var, partial_PCA=partial_PCA)
        else:
            if os.path.exists(PCA_cache_path):
                LOGGER.info(f"Loading PCA from cache {PCA_cache_path}")
                with open(PCA_cache_path, 'rb') as f:
                    self.pca = pickle.load(f)
            else:
                self._build_PCA_basis(
                    truncate=truncate, inc_var=inc_var,
                    partial_PCA=partial_PCA)
                LOGGER.info(f"Saving PCA to cache {PCA_cache_path}")
                with open(PCA_cache_path, 'wb+') as f:
                    pickle.dump(self.pca, f)

        LOGGER.info("Successfully built PCA")

        # build precision matrix
        if build_precision_matrix:
            self.build_precision_matrix(
                check_inversion=check_inversion,
                neglect_correlation=neglect_correlation)

    def convert_to_MOPED_space(self, check_inversion=True,
                               neglect_correlation=False,
                               build_precision_matrix=True,
                               MOPED_cache_dir='',
                               incremental_values={
                                   'Om':  1e-4, 's8': 1e-4,
                                   'IA':  1e-1, 'eta': 1e-1,
                                   'm': 1e-4, 'z': 1e-4, 'Ob': 1e-4,
                                   'ns': 1e-4, 'H0': 1e-1, 'w0': 1e-4}):
        """
        Builds MOPED compression matrix.
        All results are returned in MOPED space afterwards.

        :param check_inversion: If True checks numerical stability of inversion
                                of the fiducial covariance matrix
        :param neglect_correlation: Reduces the covariance matrix to its
                                    diagonal before inverting.
        :param build_precision_matrix: To build precision matrix from
                                       fdicuial_data_path realisations.
        :param MOPED_matrix: Can pass MOPED compression matrix directly
                             instead of building it.
        :param incremental_values: Need to calculate numerical derivatives.
                                   This dictionary defines the incremental
                                   values used to calculate the derivatives
                                   in each parameter direction.
        """

        if os.path.exists(f'{MOPED_cache_dir}/MOPED_matrix.npy'):
            LOGGER.info(
                f"Loading MOPED compression matrix from "
                f"cache {MOPED_cache_dir}/MOPED_matrix.npy.")
            self.MOPED_matrix = np.load(f"{MOPED_cache_dir}/MOPED_matrix.npy")
        else:
            parameters = copy.copy(self.ctx['parameters'])

            # set fiducial and incremental values to build compression matrix
            p0_dict = {}
            d_p0_dict = {}

            for ii, par in enumerate(self.ctx['parameters']):
                if par not in incremental_values:
                    raise Exception(
                        f"No incremental value passed for parameter {par}")
                p0_dict[par] = self.ctx['parameter_fiducials'][ii]
                d_p0_dict[par] = incremental_values[par]

            if len(self.ctx['nuisances']) > 0:
                for ii, par in enumerate(self.ctx['nuisances']):
                    if par not in incremental_values:
                        raise Exception(
                            f"No incremental value passed for parameter {par}")
                    if self.ctx['multi_bin'][ii]:
                        for j in range(len(self.unique_bins)):
                            p = '{}_{}'.format(par, j + 1)
                            parameters += [p]
                            p0_dict[p] = self.ctx['nuisance_fiducials'][ii]
                            d_p0_dict[p] = incremental_values[par]
                    else:
                        parameters += [par]
                        p0_dict[par] = self.ctx['nuisance_fiducials'][ii]
                        d_p0_dict[par] = incremental_values[par]

            # reset fiducial to IA=0.1 to allow for proper eta scaling
            if 'IA' in p0_dict.keys():
                p0_dict['IA'] = 0.1

            # build MOPED compression matrix
            self.MOPED_matrix = self._MOPED_compression(
                parameters, p0_dict, d_p0_dict)

            # caching
            if len(MOPED_cache_dir) > 0:
                paths.mkdir_on_demand(MOPED_cache_dir)
                np.save(
                    f"{MOPED_cache_dir}/MOPED_matrix.npy", self.MOPED_matrix)
                LOGGER.info(
                    f"Cached MOPED compression matrix to "
                    f"{MOPED_cache_dir}/MOPED_matrix.npy.")

        LOGGER.info("Successfully converted to MOPED space")

        # build precision matrix
        if build_precision_matrix:
            self.build_precision_matrix(
                check_inversion=check_inversion,
                neglect_correlation=neglect_correlation)

    def readin_interpolation_data(self, means_path, meta_path='',
                                  error_path='',
                                  check_inversion=True,
                                  fiducial_data_path='', chosen_bins=None,
                                  neglect_correlation=False, filter=None,
                                  build_precision_matrix=True,
                                  reduce_to_selected_scales=True,
                                  parameters=None, nuisances=None,
                                  normalizer_cache=None,
                                  normalize_input=False,
                                  normalize_output=False):
        """
        Loads data used for interpolation. The data is expected to be in a
        format as used by the estats.summary module

        :param means_path: Path to file holding mean datavectors for
                           each cosmology or the data array directly.
                           Shape: (realisations, length of data)
        :param meta_path: Path to file holding meta data table or the data
                          array directly. Shape: (realisations, number of meta
                          data entries)
        :param error_path: Path to file holding error vectors or the data
                           array directly. Shape: (realisations, length of
                           data)
        :param check_inversion: If True checks numerical stability of inversion
                                of the fiducial covariance matrix
        :param fiducial_data_path: Can readin a file containing realisations
                                   at the fiducial parameter setting to build
                                   covariance matrix from there.
        :param chosen_bins: If a list of strings is passed, they indicate the
                            bins that are considered. For example:
                            [1x1, 1x2, 3x4]
        :param neglect_correlation: Reduces the covariance matrix to its
                                    diagonal before inverting.
        :param filter: Can provide a custom filter function instead of using
                       the one built using the plugins.
        :param build_precision_matrix: To build precision matrix from
                                       fdicuial_data_path realisations.
        :param reduce_to_selected_scales: If True reduces the datavetor by
                                          applying the filter function in the
                                          stats plugin.
        :param parameters: Reduce parameters to passed set of parameters.
        :param nuisances: Reduce nuisances to passed set of nuisances.
        :param normalizer_cache: Path to pickle cache file. Normalizers are
                                 loaded from there and saved to there.
        :param normalize_input: If True input features are normalized.
        :param normalize_output: If True output features are normalized.
        """

        if chosen_bins is not None:
            bins = chosen_bins.split(',')
            unique_bins = np.zeros(0)
            for bin in bins:
                unique_bins = np.append(unique_bins, int(bin[:2]))
                unique_bins = np.append(unique_bins, int(bin[-2:]))
            self.unique_bins = np.unique(unique_bins)
            LOGGER.debug(
                f"Got custom bin combination setting. "
                f"Using only bin combinations {bins}")
        else:
            if self.ctx['n_tomo_bins'] == 1:
                self.unique_bins = [0]
            else:
                self.unique_bins = np.arange(1, self.ctx['n_tomo_bins'] + 1)

        select = None
        idx_norm = None

        # load normalizers
        if normalize_input | normalize_output:
            if (normalizer_cache is not None):
                if os.path.exists(normalizer_cache):
                    file = open(normalizer_cache, 'rb')
                    normalizer = pickle.load(file)
                    file.close()
                    if normalize_input:
                        self.input_normalizer = normalizer['input_normalizer']
                        orig_input_normalizer = None
                    else:
                        orig_input_normalizer = normalizer['input_normalizer']
                        self.input_normalizer = None
                    if normalize_output:
                        self.output_normalizer = \
                            normalizer['output_normalizer']
                        orig_output_normalizer = None
                    else:
                        orig_output_normalizer = \
                            normalizer['output_normalizer']
                        self.output_normalizer = None
                    LOGGER.info(
                        f"Using normalizer from cache: {normalizer_cache}")
                else:
                    self.input_normalizer = None
                    self.output_normalizer = None
                    orig_input_normalizer = None
                    orig_output_normalizer = None
            else:
                self.input_normalizer = None
                self.output_normalizer = None
                orig_input_normalizer = None
                orig_output_normalizer = None
        else:
            self.input_normalizer = None
            self.output_normalizer = None

        if len(meta_path) > 0:
            if isinstance(meta_path, str):
                LOGGER.info("Loading meta data from: {}".format(meta_path))
                META = np.load(meta_path)
            else:
                META = meta_path[:]
            select, idx_norm = self._set_meta(
                META, parameters, nuisances,
                normalize_input, normalize_output)
        else:
            raise Exception(
                "Cannot initialize without meta data. Pass meta_path.")

        # set means
        if len(means_path) > 0:
            if isinstance(means_path, str):
                LOGGER.info(
                    "Loading the mean data vectors from {}".format(means_path))
                MEANS = np.load(means_path)
                means_is_path = True
            else:
                MEANS = means_path[:]
                means_is_path = False
        else:
            raise Exception(
                "Cannot initialize without mean datavectors. Pass means_path.")
        self._set_means(MEANS, select, means_is_path)

        # set custom filter
        if filter is not None:
            self.filter = filter
        else:
            self.filter = self._create_filter(
                chosen_bins=chosen_bins,
                reduce_to_selected_scales=reduce_to_selected_scales)
        LOGGER.info(
            f"Filter set. Keeping {np.sum(self.filter)} "
            f"out of {len(self.filter)} data vector elements")

        # readin fiducial data
        if len(fiducial_data_path) > 0:
            if isinstance(fiducial_data_path, str):
                LOGGER.info(
                    "Loading data vector realisations "
                    f"from {fiducial_data_path}")
                self.FIDUCIAL_DATA = np.load(fiducial_data_path)
            else:
                self.FIDUCIAL_DATA = fiducial_data_path[:]
        else:
            LOGGER.warning(
                "No fiducial data vectors passed. Will not be able "
                "to build covariance matrix or calculate likelihood")

        if normalize_output:
            if self.output_normalizer is None:
                if means_is_path:
                    MEANS_norm = MEANS[idx_norm, :]
                else:
                    MEANS_norm = MEANS[:, :]
                self.output_normalizer = Normalizer()
                self.output_normalizer.adapt(np.array(MEANS_norm))
                LOGGER.debug("Fitted output normalizer")

        # cache normalizers
        if normalize_input | normalize_output:
            if normalizer_cache is not None:
                file = open(normalizer_cache, 'wb+')
                if orig_input_normalizer is not None:
                    input_store = orig_input_normalizer
                else:
                    input_store = self.input_normalizer
                if orig_output_normalizer is not None:
                    output_store = orig_output_normalizer
                else:
                    output_store = self.output_normalizer

                pickle.dump({'input_normalizer': input_store,
                            'output_normalizer': output_store}, file)
                file.close()
                LOGGER.info(f"Cached normalizers to {file}")

        # build precision matrix
        if build_precision_matrix:
            self.build_precision_matrix(
                check_inversion=check_inversion,
                neglect_correlation=neglect_correlation)

        # set errors
        # (not really needed for likelihood but can be convenient for plotting)
        if len(error_path) > 0:
            if isinstance(error_path, str):
                LOGGER.info(
                    "Loading the error data "
                    "vectors from {}".format(error_path))
                ERRORS = np.load(error_path)
            else:
                ERRORS = error_path
            self.ERRORS = ERRORS[select, :]
            LOGGER.debug("Set ERRORS")

    def build_emulator(self, interpolation_mode='linear', selector=None,
                       GPR_kernel=None, GP_cache_file='', scales=6.1,
                       NN_cache_file='', pos_drop=-1, n_epochs=100,
                       batchsize=32, learning_rate=0.001,
                       droprate=0.2, n_neurons=[32, 64, 128, 256],
                       load_weights=False, activation='gelu', l2reg=-0.01):
        """
        Build the interpolator for the parameters used to interpolate
        between different parameter setups. The interpolator is buit for all
        parameters and nuisances with nuisance_mode set to full.
        The different interpolation methods are multi and
        GP (Gaussian process).

        :param interpolation_mode: Either linear (N-Dim linear interpolator),
                                   GPR (Gaussian process regressor)
                                   or NN (neural network)
        :param selector: Can provide a boolean array to preselect the mean
                         datavectors to be considered for the construction of
                         the interpolator
        :param GPR_kernel: Can provide a scikit kernel that is used to
                           build the GPR. By default a RBF
                           kernel is used.
        :param GP_cache_file: Optional path to a pickle file loading premade
                              GPR interpolators. If a path is provided that
                              does not exist the built interpolator will be
                              cached there.
        :param scales: Can pass a list of scales for the RBF kernel for the
                       GPR. Default is none and the scales are optimized using
                       cross validation. If scales is passed the
                       RBF(scales, 'fixed') kernel is used.
        :param NN_cache_file: Can provide path to a cache file holding
                              pretrained network weights
        :param pos_drop: Position of dropout layer in the NN.
                        If negative no dropout is used.
        :param n_epochs: Number of epochs for NN training.
        :param batchsize: Batchsize used in NN training.
        :param learning_rate: Adam learning rate used in NN training.
        :param droprate: Dropout rate used by the dropout layer.
        :param n_neurons: Number of neurons for each layer.
        :param load_weights: If True attempts to load pretrained NN weights
                             from the cache file.
        :param activation: Activation funtion for the hidden layers.
        :param l2reg: If positive is interpreted as the fractional contribution
                      of L2 regularizer or the hidden layers to the loss
                      function.
        """

        if (interpolation_mode == 'GPR') & (not GPR_enable):
            raise Exception(
                "Cannot use GPR emulator without scikit-learn installation!")
        if (interpolation_mode == 'NN') & (not NN_enable):
            raise Exception(
                "Cannot use NN emulator without tensorflow installation!")
        LOGGER.info("Building emulator")

        ########################
        # Generate training data
        ########################

        # use only data realisations where nuisances are set to default
        params = {}
        for ii, param in enumerate(self.ctx['nuisances']):
            params[param] = self.ctx['nuisance_fiducials'][ii]
        chosen = self._get_loc(params, preselection=selector)
        LOGGER.debug(f"Using {np.sum(chosen)} inputs to train the emulator")

        # create the meta data
        meta = np.zeros((np.sum(chosen), 0))
        for param in self.ctx['parameters']:
            meta = np.hstack((meta, self.META[param][chosen].reshape(-1, 1)))
        meta_train = np.repeat(
            self.original_parameter_fiducials.reshape(1, -1),
            meta.shape[0], axis=0)
        meta_train[:, self.valid_parameter_positions] = meta

        # normalize meta
        if self.input_normalizer is not None:
            meta_train = self.input_normalizer(meta_train)
            LOGGER.info("Applied input normalization")

        # reduce to required number of parameters
        if not (load_weights & (interpolation_mode == 'NN')):
            meta_train = meta_train[:, self.valid_parameter_positions]
        if len(meta_train.shape) == 1:
            meta_train = meta_train.reshape(-1, 1)

        # create interpolation data
        data_train = self.transform_datavectors(self.MEANS[chosen, :])

        if interpolation_mode == 'linear':
            LOGGER.info("Building Linear ND interpolator")
            self.interpolator = LinearNDInterpolator(meta_train, data_train)

        elif interpolation_mode == 'GPR':
            LOGGER.info("Building GPR emulator")
            # check if cached GPR is available
            if (len(GP_cache_file) > 0) & (os.path.exists(GP_cache_file)):
                LOGGER.info(
                    f"Using cached GPR emulator from file {GP_cache_file}")
                # load cache
                with open(GP_cache_file, 'rb') as f:
                    self.interpolator = pickle.load(f)
            else:
                # build GPR
                if GPR_kernel is not None:
                    kernel = copy.deepcopy(GPR_kernel)
                    LOGGER.info("Training GPR with custom kernel.")
                elif scales is not None:
                    kernel = kernels.RBF(scales, 'fixed')
                    LOGGER.info("Training GPR with RBF kernel.")
                else:
                    kernel = kernels.RBF()
                    LOGGER.info("Training GPR with RBF kernel.")
                gpc = GaussianProcessRegressor(
                    kernel=kernel, n_restarts_optimizer=10,
                    normalize_y=True, copy_X_train=False)
                gpc.fit(meta_train, data_train)
                self.interpolator = gpc

                # caching
                if len(GP_cache_file) > 0:
                    if not os.path.exists(GP_cache_file):
                        with open(GP_cache_file, 'wb+') as f:
                            pickle.dump(self.interpolator, f)
                    LOGGER.info(
                        f"Caching GPR emulator to file {GP_cache_file}")

        elif interpolation_mode == 'NN':
            LOGGER.info("Building NN emulator")

            def gen_nn(activation, pos_drop, droprate,
                       n_neurons, n_bins, meta, l2reg_rate):
                l2reg = tf.keras.regularizers.L2(l2=l2reg_rate)
                model = Sequential()
                for jj in range(len(n_neurons)):
                    if jj == pos_drop:
                        model.add(Dropout(droprate))
                    model.add(Dense(n_neurons[jj], activation=activation,
                              kernel_regularizer=l2reg))
                model.add(Dense(n_bins))

                model.compile()
                model(meta, training=False)
                return model

            if os.path.exists(NN_cache_file):
                self.interpolator = []

                # load all the weights
                model = gen_nn(
                    activation, pos_drop, droprate, n_neurons,
                    data_train.shape[1],
                    tf.convert_to_tensor(
                        np.zeros((1, meta_train.shape[1]))), l2reg)
                if load_weights:
                    model.load_weights(NN_cache_file)
                self.interpolator = model
                LOGGER.info(f"Loaded pretrained NN from {NN_cache_file}")
            else:
                LOGGER.info("Training NN on full dataset.")
                model = gen_nn(
                    activation, pos_drop, droprate, n_neurons,
                    data_train.shape[1],
                    tf.convert_to_tensor(
                        np.zeros((1, meta_train.shape[1]))), l2reg)
                custom_loss = tf.keras.losses.MeanSquaredError()
                optimizer = tf.keras.optimizers.Adam(
                    learning_rate=learning_rate)
                train_loss = tf.keras.metrics.Mean(name='train_loss')
                train_ds = tf.data.Dataset.from_tensor_slices(
                    (meta_train, data_train)).shuffle(10000).batch(batchsize)

                train_losses = []
                for epoch in tqdm(range(n_epochs)):
                    # Reset the metrics at the start of the next epoch
                    train_loss.reset_states()

                # Training. loop over batches
                for features, labels in train_ds:
                    with tf.GradientTape() as tape:
                        predictions = model(features, training=True)
                        loss = custom_loss(labels, predictions)

                    gradients = tape.gradient(loss, model.trainable_variables)
                    # train weight
                    optimizer.apply_gradients(
                        zip(gradients, model.trainable_variables))

                # calculate training loss without dropout
                for features, labels in train_ds:
                    predictions = model(features, training=False)
                    loss = custom_loss(labels, predictions)
                    train_loss.update_state(loss)
                train_losses.append(train_loss.result())

                self.interpolator = model
                LOGGER.info(f"Finalized NN. Final training loss "
                            f"{np.sqrt(train_losses[-1])} sigma")
                if len(NN_cache_file) > 0:
                    # caching
                    model.save_weights(NN_cache_file)
        else:
            raise ValueError(
                f"Invalid value for parameter "
                f"interpolation_mode: {interpolation_mode}")
        self.interpolation_mode = interpolation_mode

    def build_scalings(self, selector=None,
                       fitting='2d-poly'):
        """
        Builds the emulators for the nuisance parameters individually for each
        data bin that have mode fiducial or marginal.
        Fits a polynomial for each nuisance individually
        (assuming each nuisance
        parameter to be independent of the other ones and the parameters).

        :param selector: Can provide a boolean array to preselect the mean
                         datavectors to be considered for the construction of
                         the emulator.
        :param fitting: Method used for fitting. Format is nd-poly,
                       where n indicates the degree of the
                       polynomial to fit.
        """
        if len(self.ctx['nuisances']) == 0:
            LOGGER.warning(
                "Cannot build scalings if no nuisances passed. Skipping...")
        self.emulators = {}
        self.emulators['fiducial'] = {}
        # Build the fiducial emulators
        for idn, nuis in enumerate(self.ctx['nuisances']):
            LOGGER.debug(f"Building scaling relation for nuisance {nuis}")
            self.emulators['fiducial'][nuis] = []
            # choose reference run at fiducial cosmology
            chosen = [True] * self.META.shape[0]
            for idp, param in enumerate(self.ctx['parameters']):
                idx = np.isclose(
                    self.META[param], self.ctx['parameter_fiducials'][idp])
                chosen = np.logical_and(chosen, idx)
            for idp, param in enumerate(self.ctx['nuisances']):
                idx = np.isclose(
                    self.META[param],
                    self.ctx['nuisance_fiducials'][idp])
                chosen = np.logical_and(chosen, idx)
            if np.sum(chosen) > 1:
                raise Exception(
                    "Found more than 1 fiducial run?!")
            elif np.sum(chosen) < 1:
                raise Exception(
                    "Found less than 1 fiducial run?!")

            reference_run = self.MEANS[chosen, :]

            # get the simulations for building the emulator
            chosen = [True] * self.META.shape[0]
            for idp, param in enumerate(self.ctx['parameters']):
                idx = np.isclose(
                    self.META[param], self.ctx['parameter_fiducials'][idp])
                chosen = np.logical_and(chosen, idx)
            for idp, param in enumerate(self.ctx['nuisances']):
                if param == nuis:
                    continue
                idx = np.isclose(
                    self.META[param],
                    self.ctx['nuisance_fiducials'][idp])
                chosen = np.logical_and(chosen, idx)

            if selector is not None:
                chosen = np.logical_and(chosen, selector)
            LOGGER.debug(
                f"Using {np.sum(chosen)} inputs to build scaling relation")
            runs_ = self.MEANS[chosen, :]

            # transform data vectors (only apply filter and normalization)
            runs = np.zeros((runs_.shape[0], np.sum(self.filter)))
            for irun, vec in enumerate(runs_):
                vec = vec.reshape(1, -1)
                if self.output_normalizer is not None:
                    vec = self.output_normalizer(vec)
                vec = vec[:, self.filter]
                runs[irun] = vec

            if self.output_normalizer is not None:
                reference_run = self.output_normalizer(reference_run)
            reference_run = reference_run[:, self.filter]

            meta = self.META[nuis][chosen]
            ratios = (runs - reference_run) / reference_run

            if fitting[1:] != 'd-poly':
                raise ValueError(f"Variable fitting cannot be {fitting}")

            # fit polynomial for each data bin using WLS
            for bin in range(ratios.shape[1]):
                degree = int(fitting[0])

                meta = meta.flatten()
                # no constant term -> force polynom to go through (0,0)
                terms = [meta**ii for ii in range(1, degree + 1)]
                A = np.array(terms).T

                B = ratios[:, bin].flatten()
                W = np.ones_like(B)

                # WLS
                Xw = A * np.sqrt(W)[:, None]
                yw = B * np.sqrt(W)
                yw[np.isnan(B)] = 0.0
                yw[np.isinf(B)] = 0.0
                coeff, r, rank, s = scipy.linalg.lstsq(Xw, yw)
                self.emulators['fiducial'][nuis].append(coeff)
            self.emulators['fiducial'][nuis] = np.array(
                self.emulators['fiducial'][nuis])

        self.fitting = fitting
        LOGGER.info("Built scaling relations")

    def get_neg_loglikelihood(
            self, params, measurement, mean=None, debias=False,
            evaluate_prior=True, prior_mode='emcee'):
        """
        Returns negative loglikelihood given a measurement data vector at the
        location in parameter space indicated by params.
        Can also pass a mean data vector directly to test.
        :param params: List/Dictionary of the parameters at which to calculate
        the neg loglikelihood
        :param measurement: The measurement data vector to compare to
        :param mean: Test data vector instead of calculating the expected
        datavector from the emulator.
        :param debias: If True use likelihood considering estimated precision
        matrix and data vectors
        :param evaluate_prior: If True adds the prior to the likelihood
        :param prior_mode: Either emcee or polychord
        (polychord requires a different kind of prior)
        :return: Negative loglikelihood
        """

        params = self._convert_dict_list(params, t='list')

        if len(params) > len(self.ctx['prior_configuration']):
            raise ValueError(
                "You passed more parameters than there are "
                "entries in your prior!")

        if evaluate_prior:
            # Get prior
            prior = self._get_prior(params, prior_mode)
            if np.isnan(prior):
                LOGGER.debug("Outside of prior range -> Returning -inf")
                return -np.inf

        # prediction of datavector at the given parameters
        if mean is None:
            mean = self._get_interp_data_vector(params)
            if np.any(np.isnan(mean)):
                LOGGER.debug(
                    "Got nan values in data vector prediction "
                    "-> Returning -inf")
                return -np.inf

        if not hasattr(self, 'precision_matrix'):
            raise Exception(
                "Cannot calculate loglikelihood without precision "
                "matrix being built")

        # measurement = self._transform_datavector(measurement)

        # Calculate the likelihood
        Q = self._get_likelihood(
            measurement.reshape(1, -1), mean, self.precision_matrix,
            debias=debias)

        # get neg loglike
        log_like = -0.5 * Q
        if evaluate_prior:
            LOGGER.debug("Adding prior to likelihood")
            log_like -= 0.5 * prior

        if log_like > 0.0:
            return -np.inf
        if np.isnan(log_like):
            return -np.inf
        if not np.isfinite(log_like):
            return -np.inf

        LOGGER.debug(f"Evaluated neg_loglikelihood to {log_like}")
        return log_like

    # HELPER FUNCTIONS
    def _build_PCA_basis(self, truncate=0, inc_var=99.999, partial_PCA=False):
        LOGGER.info("Building PCA basis")

        PCA_means = self.transform_datavectors(self.MEANS)
        self.pca = {}
        if truncate > 0:
            if partial_PCA:
                stats = self.ctx['statistic'].split('-')
                counter = 0
                for stat in stats:
                    pca = PCA(n_components=truncate, whiten=True)
                    pca.fit(PCA_means[
                        :, counter:counter + self.datavectorlengths[stat]])
                    self.pca[stat] = pca
                    LOGGER.info(
                        f'Keeping {len(pca.explained_variance_)} PCA '
                        f'components for statistic {stat}')
                    counter += self.datavectorlengths[stat]
            else:
                pca = PCA(n_components=truncate, whiten=True)
                pca.fit(PCA_means)
                LOGGER.info(
                    f'Keeping {len(pca.explained_variance_)} PCA components')
                self.pca[self.ctx['statistic']] = pca
        else:
            if partial_PCA:
                stats = self.ctx['statistic'].split('-')
                counter = 0
                for stat in stats:
                    pca = PCA(n_components=(inc_var / 100.),
                              svd_solver='full', whiten=True)
                    pca.fit(PCA_means[
                        :, counter:counter + self.datavectorlengths[stat]])
                    self.pca[stat] = pca
                    LOGGER.info(
                        f'Keeping {len(pca.explained_variance_)} PCA '
                        f'components for statistic {stat}')
                    counter += self.datavectorlengths[stat]
            else:
                pca = PCA(n_components=(inc_var / 100.),
                          svd_solver='full', whiten=True)
                pca.fit(PCA_means)
                LOGGER.info(
                    f'Keeping {len(pca.explained_variance_)} PCA components')
                self.pca[self.ctx['statistic']] = pca

    def _scale_peak_func(self, params):
        """
        Get scale factors from emulator which one needs to multiply to
        the datavector
        in order to emulate a certain nuisance configuration
        """

        scale = np.ones(np.sum(self.filter))
        fiducial_keys = np.arange(len(self.ctx['nuisances']))
        degree = int(self.fitting[0])
        scale = _get_scaling(
            scale, params,
            fiducial_keys_pos=fiducial_keys,
            nuisances=np.asarray(self.ctx['nuisances']),
            emulators=self.emulators,
            degree=degree,
            p_index=self.uni_p,
            p_inv=self.uni_p_inv)
        return scale

    def _get_likelihood(self, meas, mean, incov, debias=False):
        """
        Returns likelihood using either standard Gaussian likelihood or using
        debiasing due to estimated cov marix and predicted datavaectors
        (debias=True)
        """
        diff = mean - meas
        Q = np.dot(diff, np.dot(incov, diff.reshape(-1, 1)))[0]
        if debias:
            """
            According to:
            Jeffrey, Niall, and Filipe B. Abdalla. Parameter inference and
            model comparison using theoretical predictions from noisy
            simulations. Monthly Notices of the Royal Astronomical
            Society 490.4 (2019): 5749-5756.
            """

            LOGGER.debug("Debiasing likelihood")
            Q = 1. + Q * self.N_mean / ((self.N_mean + 1.) * (self.N_cov - 1.))
            Q *= self.N_cov

        return Q

    def _create_filter(self, chosen_bins=None,
                       reduce_to_selected_scales=False):
        """
        Creates a filter that cuts out the required data vector elements
        and an array indicating the tomographic bins for the emulator
        as well as some other arrays used by the interpolator.
        """

        def get_tomo_bin_num(stat, ctx):
            if 'Cross' in stat:
                tomo_bins = int(scipy.special.binom(
                    ctx['n_tomo_bins'] + 2 - 1,
                    ctx['n_tomo_bins'] - 1))
            else:
                tomo_bins = self.ctx['n_tomo_bins']
            return tomo_bins

        filter = np.zeros(0, dtype=bool)
        bin_filter = np.zeros(0, dtype=str)

        stats = self.ctx['statistic'].split('-')
        self.datavectorlengths = {}

        for stat in stats:
            vec_length = 0
            plugin = utils.import_executable(stat, 'filter')
            # determine number of different tomographic bins
            tomo_bins = get_tomo_bin_num(stat, self.ctx)

            # build a filter to select the relevant data bins
            for bin in range(tomo_bins):
                if 'Cross' in stat:
                    bin_val = self.ctx['cross_ordering'][bin]
                elif self.ctx['n_tomo_bins'] == 1:
                    bin_val = '00x00'
                else:
                    bin_val = '{}x{}'.format(
                        str(bin + 1).zfill(2), str(bin + 1).zfill(2))
                # add to filter
                self.ctx['bin'] = bin
                f = plugin(self.ctx)
                if not reduce_to_selected_scales:
                    f = np.ones(len(f), dtype=bool)
                # allow to ignore certain bins
                if chosen_bins is not None:
                    if bin_val not in chosen_bins:
                        f = np.full(len(f), False)
                filter = np.append(filter, f)
                vec_length += np.sum(f)
            self.datavectorlengths[stat] = int(vec_length)

            # build an array indicating which data bins belong to which
            # tomographic bin
            for bin in range(tomo_bins):
                if 'Cross' in stat:
                    bin_val = self.ctx['cross_ordering'][bin]
                elif self.ctx['n_tomo_bins'] == 1:
                    bin_val = '00x00'
                else:
                    bin_val = '{}x{}'.format(
                        str(bin + 1).zfill(2), str(bin + 1).zfill(2))
                if chosen_bins is not None:
                    if bin_val not in chosen_bins:
                        if reduce_to_selected_scales:
                            continue

                # add to bin filter
                self.ctx['bin'] = bin
                f = plugin(self.ctx)
                if not reduce_to_selected_scales:
                    f = np.ones(len(f), dtype=bool)

                bin_filter = np.append(
                    bin_filter, [bin_val] * int(np.sum(f)))

        self.bin_array = bin_filter

        # get mapping for each data vector bin and nuisance to the correct
        # location in nuisance parameters
        p_index = np.zeros(
            (int(np.sum(filter)), len(self.ctx['nuisances']), 2), dtype=int)
        for s in range(int(np.sum(filter))):
            bin = self.bin_array[s]
            counter = len(self.ctx['parameters'])
            for ii, param in enumerate(self.ctx['nuisances']):
                if self.ctx['multi_bin'][ii]:
                    # take multi_bin mode into account
                    if int(bin[:2]) == 0:
                        # non-tomographic
                        idx1 = counter + int(bin[:2])
                        idx2 = idx1
                        counter += 1
                    else:
                        idx1 = counter + \
                            np.where(self.unique_bins == int(bin[:2]))[0]
                        idx2 = counter + \
                            np.where(self.unique_bins == int(bin[-2:]))[0]
                        counter += len(self.unique_bins)
                    p_index[s, ii, 0] = idx1
                    p_index[s, ii, 1] = idx2
                else:
                    p_index[s, ii, 0] = counter
                    p_index[s, ii, 1] = counter
                    counter += 1

        # calculate the unique combinations
        self.uni_p = []
        self.uni_p_inv = []
        for ii, param in enumerate(self.ctx['nuisances']):
            uni_p_index, p_index_inv = np.unique(p_index[:, ii, :], axis=0,
                                                 return_inverse=True)
            self.uni_p.append(uni_p_index)
            self.uni_p_inv.append(p_index_inv)
        self.uni_p = tuple(self.uni_p)
        self.uni_p_inv = np.asarray(self.uni_p_inv, dtype=int)

        return filter.astype(bool)

    def _get_loc(self, params, exclude=False, preselection=None):
        """
        Get a filter for data realisations where parameters are set to params
        """
        if preselection is None:
            chosen = [True] * self.META.shape[0]
        else:
            chosen = preselection
        for param in params.keys():
            idx = np.isclose(self.META[param], params[param])
            chosen = np.logical_and(chosen, idx)
        if exclude:
            chosen = np.logical_not(chosen)
        return chosen

    def _get_interp_data_vector(self, params):
        """
        Returns an interpolated data vector at parameters params
        """
        pars = self.original_parameter_fiducials[:]
        pars[self.valid_parameter_positions] = np.asarray(
            params)[self.valid_parameter_positions]
        # normalize
        if self.input_normalizer is not None:
            pars = self.input_normalizer(pars.reshape(1, -1))
            LOGGER.debug("Applied input normalizer")
        pars = np.atleast_2d(pars)

        if self.interpolation_mode == "linear":
            mean = self.interpolator(pars)
            mean = np.asarray(mean).flatten()
        elif self.interpolation_mode == "GPR":
            # get prediction from GPR interpolator
            mean = self.interpolator.predict(pars)
            mean = np.asarray(mean).flatten()
        elif self.interpolation_mode == "NN":
            mean = self.interpolator(
                tf.convert_to_tensor(pars), training=False)
            mean = np.asarray(mean).flatten()

        # scale prediction according to polynomial models
        if len(params) > len(pars):
            LOGGER.debug("Applying scaling relations")
            if hasattr(self, 'pca'):
                if len(list(self.pca.keys())) > 1:
                    # partial pca
                    stats = self.ctx['statistic'].split('-')
                    new_vec = np.zeros(0)
                    counter = 0
                    for stat in stats:
                        vec_partial = mean[
                            counter:counter + self.pca[stat].n_components_]
                        new_vec = np.append(
                            new_vec, self.pca[stat].inverse_transform(
                                vec_partial.reshape(1, -1)).flatten())
                        counter += self.pca[stat].n_components_
                    mean = new_vec
                else:
                    mean = self.pca[self.ctx['statistic']].inverse_transform(
                        mean.reshape(1, -1))

            scale_facs = self._scale_peak_func(params).reshape(1, -1)
            mean = mean * scale_facs

            if hasattr(self, 'pca'):
                if len(list(self.pca.keys())) > 1:
                    # partial pca
                    stats = self.ctx['statistic'].split('-')
                    new_vec = np.zeros(0)
                    counter = 0
                    for stat in stats:
                        vec_partial = mean[
                            :, counter:counter+self.datavectorlengths[stat]]
                        new_vec = np.append(
                            new_vec,
                            self.pca[stat].transform(
                                vec_partial.reshape(1, -1)).flatten())
                        counter += self.datavectorlengths[stat]
                    mean = new_vec
                else:
                    mean = self.pca[self.ctx['statistic']].transform(
                        mean).reshape(1, -1)

        # moped compression
        if hasattr(self, 'MOPED_matrix'):
            LOGGER.debug("Converting to MOPED space")
            mean = np.matmul(
                self.MOPED_matrix, mean.reshape(-1, 1)).reshape(1, -1)
        return mean

    def _invert_cov_matrices(self, check_inversion=True,
                             neglect_correlation=False):
        """
        Inverts covariance matrices
        :param neglect_correlation: Reduces the covariance matrix to its
                                    diagonal before inverting.
        """

        temps = []
        for ii in range(self.precision_matrix.shape[0]):
            # checking stability of inversion
            if neglect_correlation:
                inverse = np.linalg.solve(
                    np.diag(
                        np.diag(self.precision_matrix[ii, :, :])),
                    np.eye(self.precision_matrix[ii, :, :].shape[0]))
            else:
                inverse = np.linalg.solve(
                    self.precision_matrix[ii, :, :],
                    np.eye(self.precision_matrix[ii, :, :].shape[0]))
                if check_inversion:
                    id_check = np.dot(
                        self.precision_matrix[ii, :, :], inverse)
                    id = np.eye(id_check.shape[0])
                    if not np.allclose(id_check, id):
                        raise Exception(
                            "Inversion of Fiducial Covariance matrix "
                            "did not pass numerical stability test")
                    else:
                        LOGGER.debug("Successfully inverted Fiducial "
                                     "Covariance matrix")
            temps.append(inverse)
        self.precision_matrix = np.asarray(temps)
        if self.precision_matrix.shape[0] == 1:
            self.precision_matrix = self.precision_matrix[0]

    def _convert_dict_list(self, obj, t='list'):
        """
        Converts dictionary to list or the othwer way round
        """
        if isinstance(obj, dict):
            f = 'dict'
        elif (isinstance(obj, list)) | (isinstance(obj, np.ndarray)):
            f = 'list'
        else:
            raise Exception("{} is not a list nor a dictionary".format(obj))

        if f == t:
            return obj
        elif (f == 'dict') & (t == 'list'):
            list_ = []
            for key in self.ctx['parameters']:
                if key in list(obj.keys()):
                    list_.append(obj[key])
            for ii, key in enumerate(self.ctx['nuisances']):
                if key in list(obj.keys()):
                    list_.append(obj[key])
                for bin in range(1, 1 + self.ctx['n_tomo_bins']):
                    if '{}_{}'.format(key, bin) in list(obj.keys()):
                        list_.append(obj['{}_{}'.format(key, bin)])
            return list_

        elif (f == 'list') & (t == 'dict'):
            if len(list(obj.keys())) == len(self.ctx['parameters']):
                LOGGER.warning(
                    "The length of the oject {} matches only the number of "
                    "parameters. Assuming that only parameters and no "
                    "nuisances given.".format(obj))
                check = False
            elif len(list(obj.keys())) == \
                    (len(self.ctx['parameters']) + len(self.ctx['nuisances'])):
                check = True
            else:
                raise Exception(
                    "The list {} does not contain the right number of "
                    "parameters. Either only parameters or parameters + "
                    "nuisances".format(obj))

            dict_ = {}
            for ik, key in enumerate(self.ctx['parameters']):
                dict_[key] = obj[ik]
            if check:
                for key in self.ctx['nuisances']:
                    if key in list(obj.keys()):
                        list.append(obj[key])
            return dict_

    def _MOPED_compression(self, parameters, p0_dict, d_p0_dict):
        '''
        In order to compress a given data vector,
        you need to be able to compute the derivative
        of your data vector wrt all the parameters in your analysis
        (cosmological + nuisance).
        The output will be a matrix of length (N_params,len_uncompressed_DV).
        Then you just need to do:
        t_matrix # this the compression matrix
        compressed_cov =
        np.matmul(t_matrix,np.matmul(uncompressed_cov,t_matrix.T))
        compressed_DV = np.matmul(t_matrix,uncompressed_DV)
        Credits: Marco Gatti
        '''

        try:
            inv_cov = self.precision_matrix
            len_uncompressed_DV = inv_cov.shape[0]
        except AttributeError:
            raise Exception(
                "Cannot build MOPED compression because precision matrix "
                "was not built -> Set build_precision_matrix=True in "
                "readin_interpolation_data")
        if not hasattr(self, 'interpolator'):
            raise Exception(
                "Cannot build MOPED compression without emulator. "
                "Run build_emulator() first")

        # this  initialises the compression matrix.
        transf_matrix = np.zeros((len(parameters), len_uncompressed_DV))

        for count, parameter in enumerate(parameters):
            LOGGER.debug(f"Building compression for parameter {parameter}")
            LOGGER.debug(f"Using fiducial value {p0_dict[parameter]} "
                         f"and increment {d_p0_dict[parameter]}")
            p1_dict = copy.copy(p0_dict)
            # initialise some stuff.
            ddh = np.zeros((len_uncompressed_DV, 4))
            der = np.zeros(len_uncompressed_DV)
            # now I am doing the 5-stencil derivative wrt to one parameter
            # at a time.
            # define a new dictionary with only ONE parameter slightly varied.
            p1_dict[parameter] = p0_dict[parameter] - 2 * d_p0_dict[parameter]
            u = self._compute_theory(p1_dict)
            ddh[:, 0] = u

            p1_dict[parameter] = p0_dict[parameter] - d_p0_dict[parameter]
            u = self._compute_theory(p1_dict)
            ddh[:, 1] = u
            p1_dict[parameter] = p0_dict[parameter] + d_p0_dict[parameter]
            u = self._compute_theory(p1_dict)
            ddh[:, 2] = u

            p1_dict[parameter] = p0_dict[parameter] + 2 * d_p0_dict[parameter]
            u = self._compute_theory(p1_dict)
            ddh[:, 3] = u

            der = -(- ddh[:, 0] + 8 * ddh[:, 1] - 8 * ddh[:, 2]
                    + ddh[:, 3]) / (12 * d_p0_dict[parameter])
            der = der.reshape(-1, 1)
            # the inv_cov is the approximate uncompressed inverse covariance.
            bc = np.matmul(inv_cov, der)
            norm = np.matmul(der.T, np.matmul(inv_cov, der))
            if count > 0:
                for q in range(count):
                    w = np.matmul(
                        der.T, transf_matrix[q, :].reshape(-1, 1))
                    w = w[0][0] * transf_matrix[q, :].reshape(-1, 1)
                    bc = bc - w
                    norm = norm - np.matmul(der.T, transf_matrix[q, :])**2.
            norm = np.abs(norm)
            norm = np.sqrt(norm)
            transf_matrix[count, :] = bc.T / norm[0][0]
        return transf_matrix

    def _compute_theory(self, p0_dict):
        list = self._convert_dict_list(p0_dict, 'list')
        mean = self._get_interp_data_vector(list)
        return mean.reshape(-1)

    def _transform_datavector(self, vec_in):
        """
        Applies all the available modifications to a raw data vector,
        meaning normalization, filtering, PCA and MOPED compression
        in this exact order.
        :param vec_in: A raw data vector that should be tranformed.
        :return: The transformed data vector
        """

        vec = vec_in[:].reshape(1, -1)
        if self.output_normalizer is not None:
            vec = self.output_normalizer(vec)
            LOGGER.debug("Applied output normalization")
        vec = vec[:, self.filter]
        if hasattr(self, 'pca'):
            if len(list(self.pca.keys())) > 1:
                # partial pca
                stats = self.ctx['statistic'].split('-')
                new_vec = np.zeros(0)
                counter = 0
                for stat in stats:
                    vec_partial = vec[
                        :, counter:counter+self.datavectorlengths[stat]]
                    new_vec = np.append(
                        new_vec,
                        self.pca[stat].transform(
                            vec_partial.reshape(1, -1)).flatten())
                    counter += self.datavectorlengths[stat]
                vec = new_vec
            else:
                vec = self.pca[self.ctx['statistic']].transform(vec)
            LOGGER.debug("Applied PCA")
        if hasattr(self, 'MOPED_matrix'):
            vec = np.matmul(self.MOPED_matrix, vec.reshape(-1, 1))
            LOGGER.debug("Applied MOPED compression")
        return vec.reshape(1, -1)

    def _set_meta(self, meta, parameters=None, nuisances=None,
                  normalize_input=False, normalize_ouput=False):
        """
        Set meta data table

        :param meta: Meta table to set
        """

        if parameters is None:
            parameters = copy.copy(self.ctx['parameters'])
        if nuisances is None:
            nuisances = copy.copy(self.ctx['nuisances'])

        if (self.input_normalizer is None) \
                & (normalize_input | normalize_ouput):
            # build meta normalizer using all realisations used for emulator

            if normalize_input:
                # only use those with fiducial nuisance
                idx_norm = np.ones(meta.shape[0], dtype=bool)
                for nuis, fid in zip(
                        self.ctx['nuisances'], self.ctx['nuisance_fiducials']):
                    idx_norm = np.logical_and(
                        idx_norm, np.isclose(meta[nuis], fid))
                meta_norm = meta[idx_norm]
                meta_norm = pd.DataFrame(meta_norm)
                meta_norm = meta_norm.drop(columns=['tomo', 'NREALS'])
                for nuis in self.ctx['nuisances']:
                    meta_norm = meta_norm.drop(columns=[nuis])
                self.input_normalizer = Normalizer()
                self.input_normalizer.adapt(np.array(meta_norm))
                LOGGER.debug("Built input normalizer")
        else:
            idx_norm = None

        # allow to only use a subspace of the original parameters/nuisances

        # parameters
        rejects = {}
        positions = []
        self.original_parameter_fiducials = np.asarray(
            self.ctx['parameter_fiducials'][:]).flatten()
        self.original_parameters = np.asarray(
            self.ctx['parameters'][:]).flatten()
        LOGGER.info(
            f"Using parameters {parameters} "
            f"out of {self.original_parameters}")

        orig = np.asarray(copy.copy(self.ctx['parameters']))
        self.ctx['parameters'] = []
        self.ctx['parameter_fiducials'] = []
        for p in parameters:
            if p in orig:
                pos = np.where(orig == p)[0][0]
                positions.append(pos)
            else:
                raise ValueError(
                    f"Requested parameter {p} is not in parameters.")
            self.ctx['parameters'].append(p)
            self.ctx['parameter_fiducials'].append(
                self.original_parameter_fiducials[pos])
        reject_params = list(set(orig) - set(self.ctx['parameters']))
        for p in reject_params:
            rejects[p] = self.original_parameter_fiducials[
                np.where(orig == p)[0][0]]

        # store all valid parameter positions
        self.valid_parameter_positions = copy.deepcopy(
            np.asarray(positions, dtype=int).flatten())

        # nuisances
        self.original_nuisance_fiducials = np.asarray(
            self.ctx['nuisance_fiducials'][:]).flatten()
        self.original_nuisances = np.asarray(
            self.ctx['nuisances'][:]).flatten()
        LOGGER.info(
            f"Using nuisances {nuisances} "
            f"out of {self.original_nuisances}")

        orig_nuis = np.asarray(copy.copy(self.ctx['nuisances']))
        orig_bin = copy.copy(self.ctx['multi_bin'])
        self.ctx['nuisances'] = []
        self.ctx['nuisance_fiducials'] = []
        self.ctx['multi_bin'] = []
        counter = 0
        for p in nuisances:
            if p in orig_nuis:
                pos = np.where(orig_nuis == p)[0][0]
                if orig_bin[pos]:
                    positions += [
                        pos + len(orig) + x for x in range(
                            len(self.unique_bins))]
                    counter += len(self.unique_bins)
                else:
                    positions.append(counter + len(orig))
                    counter += 1
            else:
                raise ValueError(
                    f"Requested nuisance {p} is not in nuisances.")
            self.ctx['nuisances'].append(p)
            self.ctx['nuisance_fiducials'].append(
                self.original_nuisance_fiducials[pos])
            self.ctx['multi_bin'].append(orig_bin[pos])
        reject_params = list(set(orig_nuis) - set(self.ctx['nuisances']))
        for p in reject_params:
            rejects[p] = self.original_nuisance_fiducials[
                np.where(orig_nuis == p)[0][0]]

        # adjust prior
        orig_prior = copy.deepcopy(self.ctx['prior_configuration'])
        self.ctx['prior_configuration'] = []
        for pos in positions:
            self.ctx['prior_configuration'].append(orig_prior[pos])
        LOGGER.info(
            f"Set prior configuration to {self.ctx['prior_configuration']}")

        new_dtype = np.dtype({'names': tuple(['tomo', 'NREALS']),
                              'formats': tuple(['i4', 'i4'])})

        # add all parameters and nuisances specified in config
        for ii, param in enumerate(self.ctx['parameters']):
            new_dtype = np.dtype(new_dtype.descr + [(param, 'f8')])
        for ii, nuis in enumerate(self.ctx['nuisances']):
            new_dtype = np.dtype(new_dtype.descr + [(nuis, 'f8')])

        # create new meta data with only specified parameters
        new_meta = np.zeros(meta.shape, dtype=new_dtype)
        for par in ['tomo', 'NREALS']:
            new_meta[par] = meta[par]
        for ii, par in enumerate(self.ctx['parameters']):
            try:
                new_meta[par] = meta[par]
            except ValueError:
                new_meta[nuis] = [self.ctx['parameter_fiducials'][ii]] \
                    * meta.shape[0]
        for ii, nuis in enumerate(self.ctx['nuisances']):
            try:
                new_meta[nuis] = meta[nuis]
            except ValueError:
                new_meta[nuis] = [self.ctx['nuisance_fiducials'][ii]] \
                    * meta.shape[0]

        # reject simulations where rejected parameters
        # are not set to fiducial values
        select = np.ones(meta.shape[0], dtype=bool)
        for r in rejects.items():
            select = np.logical_and(select, np.isclose(meta[r[0]], r[1]))

        self.META = new_meta[select]
        self.N_mean = np.mean(self.META['NREALS'])
        return select, idx_norm

    def _set_means(self, MEANS, select, means_is_path):
        """
        Set mean data vectors

        :param MEANS: Means to set
        """

        if means_is_path:
            if select is not None:
                MEANS = MEANS[select, :]
            else:
                MEANS = MEANS[:, :]
        else:
            MEANS = MEANS[:, :]

        self.MEANS = MEANS
        if self.MEANS.shape[0] != self.META.shape[0]:
            raise Exception(
                f"meta data and mean data vectors do not match! "
                f"Received {self.META.shape[0]} meta data entries "
                f"and {self.MEANS.shape[0]} data vectors")

    def _get_prior(self, params, prior_mode='emcee'):
        """
        Evaluates the prior.
        :param params: List of parameters
        (order should be same as in parameters and nuisances)
        :param prior_mode: Either emcee or polychord
        (polychord requires a different kind of prior)
        """
        if prior_mode == 'polychord':
            if not poly_enable:
                raise Exception(
                    "Cannot use prior_mode=polychord "
                    "without polychord installation!")
            prior = []
            for ii in range(len(params)):
                prior_config = self.ctx['prior_configuration'][ii]
                if prior_config[0] == 'flat':
                    prior.append(
                        UniformPrior(
                            prior_config[1],
                            prior_config[2])(params[ii]))
                elif prior_config[0] == 'normal':
                    prior.append(
                        GaussianPrior(
                            prior_config[1],
                            prior_config[2])(params[ii]))
        elif prior_mode == 'emcee':
            prior = 0.0
            for ii in range(0, len(params)):
                prior_config = self.ctx['prior_configuration'][ii]
                if prior_config[0] == 'flat':
                    if params[ii] < prior_config[1]:
                        prior = np.nan
                        break
                    if params[ii] > prior_config[2]:
                        prior = np.nan
                        break
                elif prior_config[0] == 'normal':
                    prior += (
                        (params[ii] - prior_config[1]) / prior_config[2])**2.
        else:
            raise ValueError(f"Option {prior_mode} for prior mode not valid")
        LOGGER.debug(f"Evaluated prior to {prior}")
        return prior

    def build_precision_matrix(self, check_inversion=True,
                               neglect_correlation=True):
        """
        Uses the fiducial data vector realisations to build the precision
        matrix.
        :param check_inversion: If True performs some stability checks for
        the inversion.
        :param neglect_correlation: If True all off-diagonal elements in
        the cov matrix are set to 0.
        """

        if not hasattr(self, 'FIDUCIAL_DATA'):
            raise Exception(
                "Cannot build precision matrix without fiducial data vectors!")
        fiducials = self.transform_datavectors(self.FIDUCIAL_DATA)

        cov = np.cov(fiducials, rowvar=False)

        # only setting a single central covariance matrix
        self.precision_matrix = cov.reshape(1, cov.shape[0], cov.shape[1])
        self._invert_cov_matrices(check_inversion=check_inversion,
                                  neglect_correlation=neglect_correlation)
        self.N_cov = self.FIDUCIAL_DATA.shape[0]


# @nb.jit(nopython=True)
def _get_param_array(params, p_index, degree, fiducial_keys_pos):
    ps = []
    for ii in fiducial_keys_pos:
        p_ = p_index[ii]
        ps_ = []
        for s in range(len(p_)):
            p = (params[p_[s, 0]]
                 + params[p_[s, 1]]) / 2.
            ps_.append(p)
        ps.append(ps_)

    # for polynomial precalculate all the terms
    p_terms = []
    for ii in range(len(fiducial_keys_pos)):
        ps_ = ps[ii]
        terms_ = []
        for s in range(len(ps_)):
            p = ps_[s]
            terms = np.array(
                [p**xx for xx in range(1, degree + 1)])
            terms_.append(terms)
        p_terms.append(terms_)
    return ps, p_terms


# @nb.jit(nopython=True)
def _get_scale(length, p_terms, emulators, p_inv):
    # loop over each data bin
    scale = np.zeros(length)
    for s in range(length):
        terms = p_terms[p_inv[s]]
        to_add = np.dot(emulators[s], terms)
        scale[s] += to_add
    return scale


def _get_scaling(scale, params, fiducial_keys_pos, nuisances,
                 emulators, degree, p_index, p_inv):
    ps, p_terms = _get_param_array(
        np.array(params), p_index, degree, fiducial_keys_pos)
    for ii, param in enumerate(nuisances):
        scale += _get_scale(
            scale.size, np.array(p_terms[ii]),
            emulators['fiducial'][param], p_inv[ii])
    return scale


class Normalizer:
    # selfmade whitener
    def __init__(self):
        self.variance = []
        self.mean = []
        self.is_adapted = False

    def adapt(self, input):
        # assert 2d array
        assert len(input.shape) == 2
        self.variance = np.var(input, axis=0)
        self.variance[np.isinf(1./self.variance)] = 1.0
        self.mean = np.mean(input, axis=0)
        self.is_adapted = True

    def __call__(self, input):
        if (input.shape) == 1:
            input = input.reshape(1, -1)
        assert len(input.shape) == 2
        assert input.shape[1] == self.variance.size
        return np.divide(input - self.mean, np.sqrt(self.variance))
