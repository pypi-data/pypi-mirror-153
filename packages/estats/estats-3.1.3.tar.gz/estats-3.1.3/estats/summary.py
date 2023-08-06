# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
from tqdm import tqdm
import copy
import matplotlib.pyplot as plt
from estats import utils

from ekit import paths as paths
from ekit import context
from ekit import logger

LOGGER = logger.init_logger(__name__)


class summary:
    """
    The summary module is meant to postprocess summary statistics measurements.

    The main functionality of the summary module is to calculate mean
    data-vectors, standard deviations and covariance or precision matrices
    for the summary statistics at different parameter configurations,
    based on a set of realizations of the summary statistic at each
    configuration.

    The meta data (e.g. cosmology setting, precision settings, tomographic
    bin and so on) for each set of realizations (read-in from a file or an
    array directly) can be
    given to the module on read-in directly or parsed from the filename.
    Directly after read-in a first postprocessing can be done using the process
    function defined in the statistic plugin.
    The read-in data-vectors are stored appended to a data table for each
    statistic and the meta data is added to an internal meta data table.
    The realizations are ordered according to their meta data entry. There
    are two special entries for the meta data (tomo: label for the tomographic
    bin of the data-vectors, NREALS: the number of data-vectors associated to
    each entry (is inferred automatically)).
    All other entries can be defined by the user.

    The summary module allows to downbin the potentially very long data-vectors
    into larger bins using a binning scheme.
    The decide_binning_scheme function in the statistic plugin is used to
    decide on
    that scheme, which defines the edges of the large bins based on the bins
    of the original data-vectors. For plotting purposes the binning scheme
    can also define the values of each data bin (for example its
    signal-to-noise ratio).
    The slice function in the statistic plugin then defines how exactly
    the binning scheme is used to downbin each data-vector.
    See the :ref:`own_stat` Section for more details.

    The summary module allows to combine summary statistics calculated for
    different tomographic bins
    to perform a tomographic analysis. The tomo entry in the meta data table
    defines the label of the tomographic bin for each set of data-vector
    realizations. One can define the order of the labels when combined into
    a joint data-vector using the cross_ordering keyword.

    The summary module also allows to combine different summary
    statistics into a joint data-vector.

    The most important functionalities are:

    - generate_binning_scheme:

        Uses the decide_binning_scheme function from the statistic plugin to
        create a binning scheme. The scheme can be created for different
        tomographic bins and scales.
        See the Section :ref:`own_stat` for more details.

    - readin_stat_files:

        Reads in data-vector realizations from a file. The process function
        from the statistics plugin is used to perform a first processing of
        the data. The meta data for each file can either be given directly or
        can be parsed from the file name by giving a
        list of parameters indicating the fields to be parsed (using ekit).

    - downbin_data:

        Uses the created binning scheme to bin the data-vector entries into
        larger bins.
        Uses the slice function from the statistics plugin to do so.

    - join_redshift_bins:

        Joins all data-vector realizations of a specific statistic at the same
        configuration. The tomo entry in the meta data table
        defines the label of the tomographic bin for each set of data-vector
        realizations. One can define the order of the labels when combined into
        a joint data-vector
        using the cross_ordering keyword. If for a specific parameter
        configuration different number of realizations are found for different
        tomographic bins, only the minimum number of realizations is used to
        calculate the combined data-vectors.

    - join_statistics:

        Creates a new statistic entry including the data table and the meta
        data table, by concatenating the data-vectors of a set of statistics.
        The new statistic has the name statistic1-statistic2-...
        If for a specific parameter configuration
        different number of realizations are found for different statistics,
        only the minimum number of realizations is used to calculate the
        combined data-vectors.

    - get_means:

        Returns the mean data vectors of a statistic for the different
        parameter configurations.

    - get_meta:

        Returns the full meta data table for a statistic.

    - get_errors:

        Returns the standard deviation of the data vectors of a statistic
        for the different configurations.

    - get_covariance_matrices:

        Returns the covariance matrices estimated from the realizations at
        each configuration. Can also invert the covariance matrices directly
        to obtain the precision matrices.

    The accepted keywords are:

    - cross_ordering:

        default: []

        choices: a list of labels

        Indicates the order of the tomographic bin labels that is used by
        join_redshift_bins
        to combine data-vectors from different tomographic bins.

        The labels could be bin1xbin2 for example, and the corresponding
        cross_ordering could be [1x1, 1x2, 2x2, 2x3, 3x3].
    """

    def __init__(self, context_in={}, verbosity=3, **kwargs):
        """
        Initialization function.

        :param context_in: Context instance
        :param verbosity: Verbosity level (0-4)
        """

        logger.set_logger_level(LOGGER, verbosity)

        LOGGER.debug("Initialized summary object with no data so far.")

        allowed = ['cross_ordering']
        defaults = [[]]
        types = ['list']

        allowed, types, defaults = utils._get_plugin_contexts(
            allowed, types, defaults)
        self.ctx = context.setup_context(
            {**context_in, **kwargs}, allowed, types, defaults,
            verbosity=verbosity)

        self.meta = {}
        self.data = {}
        self.bin_centers = {}
        self.bin_edges = {}

    # ACCESING OBJECTS
    def get_data(self, statistic='Peaks', params=None):
        """
        Get full data array for a certain statistic
        :param statistic: Statistic for which to return data array
        :param params: Can provide dictionary of parameter values.
        Returns only realisations with those parameters.
        :return: All data vector realisations for the statistic
        """

        if statistic == 'all':
            return self.data
        else:
            if params is not None:
                check = [True] * self.meta[statistic].shape[0]
                for item in params.items():
                    if item[0] not in self.parameters:
                        continue
                    item_row = np.where(
                        np.asarray(self.parameters) == item[0])[0]
                    check &= np.isclose(
                        self.meta[statistic][:, item_row].astype(
                            type(item[1])).reshape(-1), item[1])
                ids = np.where(check)[0]
                out = np.zeros((0, self.data[statistic].shape[1]))
                for id in ids:
                    if id == 0:
                        start = 0
                    else:
                        start = int(
                            np.sum(self.meta[statistic][:id, 1].astype(float)))
                    end = start + int(
                        np.asarray(self.meta[statistic][id, 1]).astype(float))
                    out = np.vstack((out, self.data[statistic][start:end]))
            else:
                out = self.data[statistic]
            return out

    def get_meta(self, statistic='Peaks'):
        """
        Get full meta table for a certain statistic
        :param statistic: Statistic for which to return meta data
        :return: Full meta table for the statistic
        """
        dtype = []
        if statistic not in self.meta.keys():
            raise Exception(
                "Meta data table not set for statistic {}".format(statistic))
        if len(self.meta[statistic]) == 0:
            LOGGER.error(
                f"Meta data for statistic {statistic} is empty.")
            return []
        for ii in self.meta[statistic][0, :]:
            try:
                float(ii)
                dtype.append('f8')
                continue
            except ValueError:
                pass
            try:
                int(ii)
                dtype.append('i4')
                continue
            except ValueError:
                pass
            dtype.append('<U50')
        fields = []
        for line in self.meta[statistic]:
            fields.append(tuple(line))
        dtype = np.dtype({'names': tuple(self.parameters),
                          'formats': tuple(dtype)})
        to_return = np.core.records.fromrecords(fields, dtype=dtype)
        return to_return

    def get_binning_scheme(self, statistic='Peaks', bin=0):
        """
        Get binning scheme for a certain statistic and tomographic bin
        :param statistic: Statistic for which to return the binning scheme
        :param bin: Tomographic bin for which to return the binning scheme
        :return: bin edges and bin centers
        """
        return (self.bin_edges[bin][statistic][:],
                self.bin_centers[bin][statistic][:])

    def get_means(self, statistic='Peaks'):
        """
        Returns the mean datavectors for all different parameter
        configurations for a given statistic.
        :param statistic: Statistic for which to return means
        :return: An array containing the mean data vectors as
        (number of parameter configurations, data vector length)
        """
        pointer = 0
        means = np.zeros(
            (self.meta[statistic].shape[0], self.data[statistic].shape[1]))
        for ii, entry in enumerate(self.meta[statistic]):
            means[ii, :] = np.nanmean(
                self.data[statistic][pointer:pointer + int(float(entry[1])),
                                     :],
                axis=0)
            pointer += int(float(entry[1]))
        return means

    def get_errors(self, statistic='Peaks'):
        """
        Returns the error datavectors for all different parameter
        configurations for a given statistic.

        :param statistic: Statistic for which to return errors
        :return: An array containing the error data vectors as
                (number of parameter configurations, data vector length)
        """
        pointer = 0
        errors = np.zeros(
            (self.meta[statistic].shape[0], self.data[statistic].shape[1]))
        for ii, entry in enumerate(self.meta[statistic]):
            errors[ii, :] = np.nanstd(
                self.data[statistic][pointer:pointer + int(float(entry[1])),
                                     :],
                axis=0)
            pointer += int(float(entry[1]))
        return errors

    def get_covariance_matrices(self, statistic='Peaks', invert=False,
                                set_to_id_if_failed=False,
                                plot_fiducial_correlation=False,
                                plot_fiducial_incov=False,
                                Fiducials=[], store_fiducial_cov=False):
        """
        Returns the covariance matrices for all different parameter
        configurations for a given statistic.
        :param statistic: Statistic for which to return errors
        :param invert: If True attempts to invert the covariance matrices.
        If numerically unstable raises Error
        :param set_to_id_if_failed: If True sets matrices to identity matrix
        if the inversion fails.
        :param plot_fiducial_correlation: If True plots the correlation matrix
        and covariance matrix for the fiducial parameter setting
        indicated by Fiducials
        :param plot_fiducial_incov: If True plots the inverted covariance
        matrix for the fiducial parameter setting
        indicated by Fiducials
        :param Fiducials: The fiducial parameter values for which to plot
        :param store_fiducial_cov: If True stores fiducial covariance matrix
        separately (less RAM in MCMC)
        :return: An array containing the (inverted) covariance matrices as
        (number of parameter configurations, data vector length,
        data vector length)
        """
        covs = self._calc_cov_matrices(
            statistic, invert, set_to_id_if_failed,
            plot_fiducial_correlation,
            plot_fiducial_incov,
            Fiducials, store_fiducial_cov=store_fiducial_cov)
        return covs

    def get_full_summary(self, statistic='Peaks', invert=False,
                         set_to_id_if_failed=False,
                         plot_fiducial_correlation=False,
                         plot_fiducial_incov=False,
                         Fiducials=[],
                         label='',
                         check_stability=False, calc_covs=True,
                         calc_fiducial_cov=False, store_fiducial_cov=False):
        """
        Returns the mean datavectors, errors and (inverted) covariance matrices
        for all different parameter configurations for a given statistic.

        :param statistic: Statistic for which to return errors
        :param invert: If True attempts to invert the covariance matrices.
                       If numerically unstable raises Error
        :param set_to_id_if_failed: If True sets matrices to identity matrix
                                    if the inversion fails.
        :param plot_fiducial_correlation: If True plots the correlation matrix
                                          and covariance matrix
                                          for the fiducial parameter setting
                                          indicated by Fiducials
        :param plot_fiducial_incov: If True plots the inverted covariance
                                    matrix for the fiducial parameter setting
                                    indicated by Fiducials
        :param Fiducials: The fiducial parameter values for which to plot
        :param label: Label used to create path for cov and corr matrix plots
        :param check_stability: If True performs numerical stability checks
                                wheFn inverting covariance matrices
        :param calc_covs: Can turn off the calculation of covariance matrices.
                          For example when SVD should be used.
        :param calc_fiducial_cov: If True and calc_covs is False it only
                                  computes the fiducial matrix
        :param store_fiducial_cov: If True stores fiducial covariance matrix
                                   separately (less RAM in MCMC)
        :return: 3 objects. Means, errors and (inverted) covariance matrices
        """

        errors = self.get_errors(statistic)
        means = self.get_means(statistic)

        if calc_covs | calc_fiducial_cov:
            covs = self._calc_cov_matrices(
                statistic, invert, set_to_id_if_failed,
                plot_fiducial_correlation,
                plot_fiducial_incov,
                Fiducials, label, check_stability,
                store_fiducial_cov=store_fiducial_cov)
        else:
            covs = []
        return (means, errors, covs)

    # SETTING OBJECTS
    def set_data(self, data, statistic='Peaks'):
        """
        Set full data array

        :param data: Data array to set
        :param statistic: The statistic for which to set the data
        """
        self.data[statistic] = data[:]

    def set_meta(self, meta, statistic='Peaks', parameters=[]):
        """
        Set meta array

        :param meta: Meta array to set
        :param statistic: The statistic for which to set the meta data
        :param parameters: A list indicating the parameter labels in the meta
                           data table
        """
        self.meta[statistic] = meta[:]
        self.parameters = parameters[:]

    def set_binning_scheme(self, bin_centers, bin_edges,
                           statistic='Peaks', bin=0):
        """
        Set binning scheme

        :param bin_centers: Centers of the bins to set (only used for plotting)
        :param bin_edges: Edges of the bins to set
        :param statistic: The statistic for which to set the binning scheme
        :param bin: The tomographic bin for which to set the binning scheme
        """
        try:
            self.bin_centers[bin][statistic] = bin_centers[:]
            self.bin_edges[bin][statistic] = bin_edges[:]
        except KeyError:
            self.bin_centers[bin] = {}
            self.bin_edges[bin] = {}
            self.bin_centers[bin][statistic] = bin_centers[:]
            self.bin_edges[bin][statistic] = bin_edges[:]

    def readin_stat_files(self, files, statistic='Peaks', meta_list=[],
                          parse_meta=False, parameters=[]):
        """
        Reads in data from files and does a first processesing.

        :param files: A list of filepaths containing the realisations for
                      different parameter configurations
        :param statistic: The name of the statistic to which the files belong
        :param meta_list: Can provide a list for the meta data of the shape
                          (num_of files, num_of_parameters)
        :param parse_meta: If set to True will try to get meta
                           parameters from file names (names need to be in
                           ekit format)
        :param parameters: List of strings indicating the parameter names that
                           should be extracted from the file names
        """
        if type(files) is str:
            files = [files]
        if len(files) == 0:
            return

        plugin = utils.import_executable(
            statistic, 'process')

        for ii, file in tqdm(enumerate(files)):
            data = np.load(file)
            self.readin_stat_data(data, plugin, statistic=statistic,
                                  meta_list=meta_list,
                                  parse_meta_from_file_names=parse_meta,
                                  parameters=parameters, file=file,
                                  sort_data=False)
        LOGGER.info("Completed readin of {} files for statistic {}".format(
            len(files), statistic))
        self._sort_data(statistic, copy.copy(parameters))

    def rescale_data(self, statistic='Peaks'):
        """
        Devides each databin by the median of the samples.
        Useful when performing SVD for example.

        :param statistic: The name of the statistic to which the files belong
        """
        self.data[statistic] /= np.median(self.data[statistic], axis=0)

    def readin_stat_data(self, data, plugin=None, statistic='Peaks',
                         meta_list=[],
                         parse_meta_from_file_names=False, parameters=[],
                         file='', sort_data=True):
        """
        Processesing of a chunk of realisations belonging to the same parameter
        configuration.

        :param data: An array containing the realisations as
                     (n_reals, length of datavectors)
        :param statistic: The name of the statistic to which the realisations
                          belong
        :param meta_list: Can provide a list for the meta data of the shape
                          (1, num_of_parameters)
        :param parse_meta_from_file_names: If set to True will try to get meta
                                           parameters from file name passed by
                                           file (name need to be in ekit
                                           format)
        :param parameters: List of strings indicating the parameter names that
                           should be extracted from the file name
        :param file: A path from which the meta data can be parsed
        :param sort_data: If True performs lexsort of full data array
        """

        if plugin is None:
            plugin = utils.import_executable(
                statistic, 'process')

        meta = self._get_meta(
            data, meta_list, parse_meta_from_file_names,
            parameters, file_name=file)
        data = self._process_data(
            plugin, data, statistic, meta[0, 0])

        # update NREALS
        NREALS = int(np.asarray([data.shape[0]]))
        meta[0, 1] = NREALS

        # stacking
        try:
            self.meta[statistic] = np.vstack((self.meta[statistic], meta))
        except KeyError:
            self.meta[statistic] = meta

        try:
            self.data[statistic] = np.vstack((self.data[statistic], data[:]))
        except KeyError:
            self.data[statistic] = data

        if sort_data:
            self._sort_data(statistic, copy.copy(parameters))

    # METHODS

    def generate_binning_scheme(self, statistics=['Peaks', 'Voids', 'CLs',
                                                  'Minkowski', '2PCF', '2VCF'],
                                bin=0):
        """
        Generates a binning scheme for different statistics for a given
        tomographic bin.

        :param statistics: A list of statistics for which to compute the
                           binning scheme
        :param bin: The tomographic bin for which to calculate the binning
                    scheme
        """
        if isinstance(statistics, str):
            statistics = [statistics]

        for stat in statistics:
            if ('-' in stat):
                LOGGER.warning(
                    'Cannot make binning scheme '
                    'for joined statistics. Skipping...')
                continue

            bin_centers, bin_edges = self._decide_on_bins(
                stat, bin)

            try:
                self.bin_centers[bin][stat] = bin_centers
                self.bin_edges[bin][stat] = bin_edges
            except KeyError:
                self.bin_centers[bin] = {}
                self.bin_edges[bin] = {}
                self.bin_centers[bin][stat] = bin_centers
                self.bin_edges[bin][stat] = bin_edges

    def downbin_data(self, statistics=['Peaks', 'Voids', 'CLs',
                                       'Minkowski']):
        """
        Use binning scheme to downbin data vectors into larger bins.

        :param statistics: The statistics for which to perform the binning
        """
        if isinstance(statistics, str):
            statistics = [statistics]
        for stat in statistics:
            self._slice_data(errors=[], stat=stat)

    def join_statistics(self, statistics=['Peaks', 'CLs']):
        """
        Join datavectors for different statistics. Creates a new instance for
        meta and data objects with the key as the single statistics
        concatinated by '-'s.

        :param statistics: The statistics which should be combined.
        """

        # check that there is meta and data for all stats
        for s in statistics:
            if s not in self.meta:
                raise Exception(f"Did not find meta data for statistic {s}")
            if s not in self.data:
                raise Exception(f"Did not find data for statistic {s}")

        # get entries present in all statistics
        total_entries = np.zeros(
            (0, self.meta[statistics[0]].shape[1]), dtype=float)
        for s in statistics:
            total_entries = np.vstack((total_entries, self.meta[s]))
        # remove tomo and NREALS
        total_tomos = total_entries[:, 0]
        total_entries = total_entries[:, 2:]
        unique_entries = np.unique(total_entries.astype(float), axis=0)
        unique_tomos = np.unique(total_tomos.astype(float), axis=0)
        if len(unique_tomos) > 1:
            raise Exception("Not all entries have same tomographic bin")
        if len(unique_entries) == 0:
            raise Exception("Found no entries to combine")

        data_vector_length = 0
        for s in statistics:
            data_vector_length += self.data[s].shape[1]
        new_meta = np.zeros(
            (0, self.meta[statistics[0]].shape[1]), dtype=object)
        new_data = np.zeros((0, data_vector_length))

        # combine each entry
        for entry in unique_entries:
            skip = False
            idxs = []
            for s in statistics:
                idx = np.array([True] * self.meta[s].shape[0])
                for ii in range(unique_entries.shape[1]):
                    to_check = self.meta[s][:, ii + 2].astype(float)
                    idx = np.logical_and(
                        idx, np.isclose(to_check, entry[ii]))
                # check that idx has only one entry
                if int(np.sum(idx)) != 1:
                    LOGGER.warning(
                        f"For some reason found {int(np.sum(idx))} "
                        f"corresponding entries for statitic {s}. "
                        f"Skipping entry {entry}")
                    skip = True
                    break
                idxs.append(np.where(idx)[0][0])
            if skip:
                continue
            block_lengths = [self.meta[statistics[xx]][idxs[xx], 1]
                             for xx in range(len(statistics))]
            block_length = int(np.min(np.asarray(block_lengths, dtype=float)))
            new_meta_ = copy.copy(self.meta[statistics[0]][idxs[0]])
            new_meta_[1] = block_length
            new_meta = np.vstack((new_meta, new_meta_))

            new_data_ = np.zeros((block_length, 0))
            for ids, s in enumerate(statistics):
                lower = int(np.sum(self.meta[s][:idxs[ids], 1].astype(float)))
                new_data_temp = self.data[s][lower:lower + block_length, :]
                new_data_ = np.hstack((new_data_, new_data_temp))
            new_data = np.vstack((new_data, new_data_))

        # set the new meta array
        self.meta['-'.join(statistics)] = new_meta
        self.data['-'.join(statistics)] = new_data

        LOGGER.info("Constructed joined statistic {}".format(
            '-'.join(statistics)))

    def join_redshift_bins(self):
        """
        Concatenates datavector realisations for the different tomographic
        bins. The old single bin entries get deleted and the new entries have
        tomographic bin set to -1.
        """
        for statistic in self.data.keys():
            # get all tomographic bins in data
            bins = np.unique(self.get_meta(statistic)['tomo'])
            # if only one bin do nothing but set tomo to -1 to indicate
            if len(bins) == 1:
                LOGGER.warning(
                    "Cannot join tomographic bins since all samples have "
                    "same tomographic bin. Skipping")
                self.meta[statistic][:, 0] = -1
                continue
            if len(self.ctx['cross_ordering']) > 0:
                bins_ = self.ctx['cross_ordering']
                new_bins = []
                for bin in bins_:
                    if bin in bins:
                        new_bins.append(bin)
                bins = new_bins
            else:
                LOGGER.warning(
                    "Did not find cross_ordering entry. "
                    "Trying to guess the order of the tomographic bins.")

            # get all configurations in data
            meta = self.get_meta(statistic)
            new_meta = np.zeros((meta.shape[0], 0))
            fields = meta.dtype.fields.keys()
            parameters = []
            for field in fields:
                if (field != 'tomo') & (field != 'NREALS'):
                    new_meta = np.hstack((new_meta,
                                          meta[field].reshape(-1, 1)))
                    parameters.append(field)
            unique_meta = np.unique(new_meta, axis=0)

            # loop over the unique entries
            temp_data = np.zeros((0,
                                  self.data[statistic].shape[1] * len(bins)))
            temp_meta = np.zeros((0, self.meta[statistic].shape[1]),
                                 dtype=self.meta[statistic].dtype)
            for entry in tqdm(unique_meta):
                check = np.ones(self.meta[statistic].shape[0], dtype=bool)
                for ii, field in enumerate(parameters):
                    for jj in range(check.size):
                        check[jj] &= (str(meta[field][jj]) == str(entry[ii]))

                if np.sum(check) != len(bins):
                    LOGGER.warning(
                        "For entry with parameters {} there are some "
                        "bins missing. Skipping".format(entry))
                    continue

                # get starting and stopping points
                starts = []
                stops = []
                for e in np.where(check)[0]:
                    starts.append(np.sum(
                        meta['NREALS'][:e]))
                    stops.append(
                        np.sum(meta['NREALS'][:e + 1]))
                starts = np.array(starts, dtype=int)
                stops = np.array(stops, dtype=int)

                # decide on maximum number of realisations
                diffs = stops - starts
                max = np.min(diffs)
                diffs = diffs - max
                stops = stops - diffs

                # append combined data
                meta_ = meta[check]
                temp_ = np.zeros((max, 0))
                for bin in bins:
                    idx = np.where(meta_['tomo'] == bin)[0][0]
                    temp_ = np.hstack((
                        temp_, self.data[statistic][starts[idx]:stops[idx]]))
                temp_data = np.vstack((temp_data, temp_))

                # append combined meta
                meta_ = meta_[0]
                meta_['NREALS'] = max
                meta_['tomo'] = -1
                meta_ = np.asarray(list(meta_))
                temp_meta = np.vstack((temp_meta, meta_.reshape(1, -1)))

            # update class object
            self.data[statistic] = temp_data
            self.meta[statistic] = temp_meta

            LOGGER.info(
                "Joined data from tomographic bins for statistic {}. "
                "The order is {}".format(statistic, bins))

    ##################################
    # HELPER FUNCTIONS
    ##################################

    def _calc_cov_matrices(self, statistic, invert=False,
                           set_to_id_if_failed=False,
                           plot_fiducial_correlation=False,
                           plot_fiducial_incov=False,
                           Fiducials=[],
                           label='',
                           check_stability=False, calc_fiducial_cov=False,
                           store_fiducial_cov=False):
        """
        Calculation and inversion of covariance matrices
        """
        pointer = 0
        covs = np.zeros(
            (self.meta[statistic].shape[0], self.data[statistic].shape[1],
             self.data[statistic].shape[1]))
        for ii, entry in enumerate(self.meta[statistic]):
            if plot_fiducial_correlation | calc_fiducial_cov:
                check = True
                for xx, par in enumerate(entry[2:]):
                    check_ = np.isclose(float(par), Fiducials[xx])
                    check &= check_
                if (calc_fiducial_cov) & (not check):
                    continue
            mx = self.data[statistic][pointer:pointer + int(float(entry[1]))]
            c = np.cov(mx, rowvar=False)

            if store_fiducial_cov:
                if check:
                    np.save(
                        'fid_cov_mat_{}_{}.npy'.format(statistic, label), c)
            if plot_fiducial_correlation:
                if check:
                    plt.figure(figsize=(12, 8))
                    plt.imshow(np.ma.corrcoef(mx, rowvar=False,
                                              allow_masked=True))
                    plt.xticks(fontsize=20)
                    plt.yticks(fontsize=20)
                    cbar = plt.colorbar()
                    cbar.ax.tick_params(labelsize=20)
                    plt.savefig('corr_mat_{}_{}.pdf'.format(statistic, label))
                    plt.clf()

                    plt.figure(figsize=(12, 8))
                    plt.imshow(c)
                    plt.xticks(fontsize=20)
                    plt.yticks(fontsize=20)
                    cbar = plt.colorbar()
                    cbar.ax.tick_params(labelsize=20)
                    plt.savefig('cov_mat_{}_{}.pdf'.format(statistic, label))
                    plt.clf()

            if invert:
                try:
                    incov = np.linalg.solve(c, np.eye(c.shape[0]))
                except np.linalg.LinAlgError:
                    # Fallback to tricks if inversion not possible
                    if (np.isclose(np.linalg.det(c), 0.0)):
                        LOGGER.warning(
                            "Determinant close to 0. Trying Inversion tricks")
                        c *= 10e20
                        if (np.isclose(np.linalg.det(c), 0.0)):
                            if set_to_id_if_failed:
                                LOGGER.error(
                                    "Inversion of covariance failed. "
                                    "SETTING PRECISON MATRIX TO IDENTITY")
                                incov = np.identity(c.shape[0])
                            else:
                                raise Exception(
                                    "Error: Fiducial Covariance Matrix \
                                     not invertible!!!")
                        else:
                            incov = np.linalg.pinv(c)
                        incov *= 10e20

                    else:
                        incov = np.linalg.pinv(c)

                # check numerical stability of inversion
                if check_stability:
                    id_check = np.dot(c, incov)
                    id = np.eye(id_check.shape[0])
                    id_check -= id
                    if not np.all(np.isclose(id_check, 0.0, atol=1e10,
                                             rtol=0.0)):
                        raise Exception(
                            "Inversion of Fiducial Covariance matrix "
                            "did not pass numerical stability test")
                    else:
                        LOGGER.info("Successfully inverted Fiducial "
                                    "Covariance matrix")

                covs[ii] = incov

                if plot_fiducial_incov:
                    check = True
                    for xx, par in enumerate(entry[2:]):
                        check_ = np.isclose(par, Fiducials[xx])
                        check &= check_
                    if check:
                        plt.figure(figsize=(12, 8))
                        plt.imshow(incov)
                        plt.xticks(fontsize=20)
                        plt.yticks(fontsize=20)
                        cbar = plt.colorbar()
                        cbar.ax.tick_params(labelsize=20)
                        plt.savefig(
                            'incov_mat_{}_{}.pdf'.format(statistic, label))
                        plt.clf()
            else:
                covs[ii] = c
            if (calc_fiducial_cov):
                if not check:
                    covs = [covs[ii]]
                    break
            pointer += int(float(entry[1]))
        return covs

    def _get_meta_from_file_name(self, parameters, file):
        """
        Parse meta data from file names
        """
        defined = paths.get_parameters_from_path(file)[0]

        meta = np.zeros(0, dtype=object)
        for param in parameters:
            meta = np.append(meta, defined[param][0])
        return meta

    def _process_data(self, plugin, raw_data, stat, tomo_bin,
                      trimmed_mask_dict={}):
        """
        Load a STATS file in the correct format
        """

        self.ctx['tomo_bin'] = tomo_bin
        return plugin(raw_data, self.ctx, False)

    def _stack_data(self, raw_data, num_of_scales):
        """
        Stacks data arrays
        """
        data = np.zeros(
            (int(raw_data.shape[0] / num_of_scales), raw_data.shape[1]
             * num_of_scales))
        for jj in range(int(raw_data.shape[0] / num_of_scales)):
            data[jj, :] = raw_data[jj * num_of_scales:
                                   (jj + 1) * num_of_scales, :].ravel()
        return data

    def _get_meta(self, data, meta_list=[], parse_meta_from_file_names=False,
                  parameters=[],
                  file_name=''):
        """
        Helper function to get meta data
        """
        # Setting meta data
        NREALS = int(np.asarray([data.shape[0]]))
        if (len(meta_list) == 0) & (not parse_meta_from_file_names):
            meta = NREALS
        elif not parse_meta_from_file_names:
            meta = np.array([NREALS] + meta_list, dtype=object)
        elif parse_meta_from_file_names:
            to_app = self._get_meta_from_file_name(parameters, file_name)
            meta = np.append(NREALS, to_app)

        # put tomographic bin to the beginning
        if 'tomo' in parameters:
            idx = np.asarray(parameters) == 'tomo'
            idx = np.append([False], idx)
            meta[idx] = meta[idx]
            idx = np.where(idx)[0]
            tomo_column = meta[idx]
            meta = np.delete(meta, idx)
            meta = np.append(tomo_column, meta)
        else:
            meta = np.append(np.zeros(1), meta)
        return meta.reshape(1, -1)

    def _get_sort_idx(self, parameters, statistic):
        """
        Performs sorting of meta data
        """
        # lexsort
        idx = np.delete(np.arange(self.meta[statistic].shape[1]), 1)
        sort_idx = np.lexsort(
            np.flip(self.meta[statistic][:, idx], axis=1).transpose())

        return sort_idx

    def _slice_data(self, errors=[], stat='Peaks'):
        """
        Given some datavectors and a list of edge indices for the new bins
        as created using decide_on_bins() down-samples the datavectors
        """

        plugin = utils.import_executable(stat, 'slice')

        slicer_config = plugin(self.ctx)
        num_of_scales, n_bins_sliced, operation, mult = slicer_config[:4]
        if len(slicer_config) > 4:
            range_mode_bool = slicer_config[4]
        else:
            range_mode_bool = False

        n_bins_original = self.data[stat].shape[1] // (mult * num_of_scales)
        new_data_total = np.zeros(
            (self.data[stat].shape[0], mult * n_bins_sliced * num_of_scales))

        bins = np.unique(self.meta[stat][:, 0])

        for bin in bins:
            # get meta entries for right bin
            bin_idx = np.where(self.meta[stat][:, 0] == bin)[0]

            # select data in the right bin
            idx = np.zeros(self.data[stat].shape[0])
            for ii in bin_idx:
                start = int(np.sum(self.meta[stat][:, 1][:ii].astype(int)))
                end = start + int(self.meta[stat][:, 1][ii])
                idx[start:end] = 1
            idx = idx.astype(bool)

            if operation != 'none':
                new_data = _slicer(
                    data=self.data[stat][idx],
                    num_of_samples=self.data[stat][idx].shape[0],
                    n_bins_original=n_bins_original,
                    n_bins_sliced=n_bins_sliced,
                    bin_edges=self.bin_edges[bin][stat],
                    num_of_scales=num_of_scales,
                    mult=mult, operation=operation,
                    range_mode_bool=range_mode_bool)
            else:
                new_data = self.data[stat][idx]

            new_data_total[idx, :] = new_data

        self.data[stat] = new_data_total

        LOGGER.info(
            "Down sampled data vectors for statistic {} from {} "
            "bins to {} bins".format(
                stat, n_bins_original, n_bins_sliced))

    def _decide_on_bins(self, stat, bin=0):
        """
        Given some realisations of a datavector decides how to arange
        a fixed number of bins
        """

        plugin = utils.import_executable(
            stat, 'decide_binning_scheme')
        try:
            data = self.data[stat]
            meta = self.meta[stat]
        except KeyError:
            data = []
            meta = []
        bin_edge_indices, bin_centers = \
            plugin(data, meta, bin, self.ctx)

        LOGGER.debug("Decided on binning scheme for statistic {}".format(
            stat))

        return bin_centers, bin_edge_indices

    def _sort_data(self, statistic, parameters):
        """
        Sort data array according to parameters
        """
        idx_sort = self._get_sort_idx(parameters, statistic)

        # sort the blocks in the data
        temp_data = np.zeros_like(self.data[statistic])
        pointer = 0
        for ii in range(self.meta[statistic].shape[0]):
            block_length = int(self.meta[statistic][:, 1][idx_sort[ii]])
            start = int(np.sum(
                self.meta[statistic][:, 1][:idx_sort[ii]].astype(int)))
            end = start + int(block_length)
            to_paste = self.data[statistic][start:end, :]
            temp_data[pointer:pointer + int(block_length), :] = to_paste
            pointer += int(block_length)

        # set the objects
        self.data[statistic] = temp_data
        self.meta[statistic] = self.meta[statistic][idx_sort, :]
        self.parameters = ['tomo', 'NREALS']
        parameters.remove('tomo')
        self.parameters += parameters


def _slicer(data, num_of_samples, n_bins_original, n_bins_sliced, bin_edges,
            num_of_scales=1, mult=1, operation='mean', get_std=False,
            range_mode_bool=False):
    """
    Slices data arrays into subbins
    """
    new_data = np.zeros((num_of_samples, mult * n_bins_sliced * num_of_scales))

    for jj in range(num_of_scales):
        # loop over Minkowski functions
        for ii in range(mult):
            if range_mode_bool:
                data_act = data[:, int(n_bins_original * (mult * jj + ii)):int(
                    n_bins_original * (mult * jj + ii + 1))]
                minima = data_act[:, 0]
                maxima = data_act[:, -1]
                original_bins = np.linspace(
                    minima.reshape(-1), maxima.reshape(-1),
                    num=n_bins_original - 1).T
                original_values = original_bins[:, :-1] + 0.5 * \
                    (original_bins[:, 1:] - original_bins[:, :-1])
                original_weights = data_act[:, 1:-1]

                new_bin_edges = bin_edges[jj]
                digi = np.digitize(original_values, bins=new_bin_edges) - 1
                # unfortunately this is slow but cannot think of a better
                # way at the moment
                for xx in range(n_bins_sliced):
                    for index in range(original_weights.shape[0]):
                        if operation == 'mean':
                            new_data[index,
                                     n_bins_sliced * (ii + mult * jj) + xx] = \
                                np.nanmean(
                                original_weights[index, digi[index] == xx])
                        elif operation == 'sum':
                            new_data[index,
                                     n_bins_sliced * (ii + mult * jj) + xx] = \
                                np.nansum(
                                original_weights[index, digi[index] == xx])
            else:
                # loop over bins
                for xx in range(n_bins_sliced):
                    # Slice out correct scale
                    to_combine = data[:, int(n_bins_original * (mult * jj + ii)
                                             + bin_edges[jj][xx]):int(
                        n_bins_original * (mult * jj + ii)
                        + bin_edges[jj][xx + 1])]

                    if get_std:
                        num = bin_edges[0, xx + 1] - bin_edges[0, xx]
                        fac = 1. / np.sqrt(num)
                    else:
                        fac = 1.

                    if operation == 'mean':
                        new_data[:, n_bins_sliced
                                 * (ii + mult * jj) + xx] = fac \
                            * np.nanmean(to_combine, axis=1)
                    elif operation == 'sum':
                        new_data[:, n_bins_sliced
                                 * (ii + mult * jj) + xx] = fac \
                            * np.nansum(to_combine, axis=1)
    return new_data
