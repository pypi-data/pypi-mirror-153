# Copyright (C) 2019 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import numpy as np
import healpy as hp
import scipy
from scipy import stats

from ekit import context
from estats import utils
from ekit import logger

LOGGER = logger.init_logger(__name__)


class catalog:
    """
    The catalog module handles a galaxy catalog consisting out of
    coordinates, ellipticities, weights and tomographic bins for each galaxy.
    Main functionalities: Can rotate the catalog on the sky, output
    survey mask, weight maps, shear and convergence maps.
    The convergence maps are calculated from the
    shear maps using spherical Kaiser-Squires.
    Also allows generation of shape noise catalogs
    or shape noise maps using random
    rotation of the galaxies in place.
    Can also pass additional scalar and obtain maps for these.

    The most important functionalities are:

    - rotate_catalog:

        Allows to rotate the survey on the sky by given angles.
        The spin-2 ellipticity field can also be
        rotated by the appropriate angle.

    - get_mask:

        Returns the survey mask as a binary Healpix
        (`Gorski et al. 2005
        <https://iopscience.iop.org/article/10.1086/427976>`_)
        map.

    - get_map:

        Can return Healpix
        shear maps, convergence maps or a weight map
        (number of galaxies per pixel). The convergence map is calculated from
        the ellipticities of the galaxies using the spherical Kaiser-Squires
        routine (`Wallis et al. 2017 <https://arxiv.org/pdf/1703.09233.pdf>`_).
        The shear and convergence maps are weighted by the galaxy weights.

    - generate_shape_noise_map:

        Generates a shape noise Healpix shear map by random rotation of the
        galaxies ellipticities in place. The weights are considered in the
        generation of the noise.

    The accepted keywords are:

    - NSIDE:

        default: 1024

        choices: an integer being a power of 2

        The Healpix resolution that is used to produce the map products.

    - degree:

        default: True

        choices: True, False

        If True the coordinates are assumed to be given in degrees otherwise
        in radians.

    - colat:

        default: False

        choices: True, False

        If True the second coordinate is assumed to be a co-latitude otherwise
        a normal latitude is assumed.

    - prec:

        default: 32

        choices: 64, 32, 16

        Size of the float values in the Healpix maps in bits. For less then 32
        hp.UNSEEN is mapped to -inf -> No RAM optimization anymore
    """

    def __init__(self, alphas=[], deltas=[], e1s=[], e2s=[],
                 redshift_bins=[], weights=[], pixels=[], context_in={},
                 store_pix=False,
                 verbosity=3, **kwargs):
        """
        Initialization function for catalog class.
        At least the position of the objects on the
        sky is required (alphas, deltas).
        Also accepts galaxy ellipticity components (e1s, e2s).
        The ellipticities can be converted to a convergence signal.
        Further accepts galaxy weights and redshift bins.
        Instead of alphas, deltas can also pass HEALPIX pixel locations.
        Can pass additional fields by name.
        They will be treated as scalar galaxy properties.
        The fields are identified if the string
        'field' is contained in the name.

        :param alphas: List of first coordinates, either in radians or degrees
        :param deltas: List of second coordinates, either in radians or degrees
        :param e1s: List of first ellipticity components
        :param e2s: List of second ellipticity components
        :param redshift_bins: List of integers indicating the redshift bin the
                              objects belong to (should start from 1)
        :param weights: List of object weights.
                        If not passed weights are set to 1 for each object.
        :param context_in: A dictionary containing parameters.
        :param store_pix: If true only pixel location of objects is stored
        :param verbosity: Verbosity level (0-4)
        """

        logger.set_logger_level(LOGGER, verbosity)

        LOGGER.debug("Initializing catalog object")

        # setup context
        allowed = ['NSIDE', 'degree', 'colat', 'prec']
        types = ['int', 'bool', 'bool', 'int']
        defaults = [1024, True, False, 32]

        # separate kwargs into additional fields and context variables
        extra_variables = {}
        self.extra_fields = []
        for item in kwargs:
            if 'field' in item:
                LOGGER.debug(f"Found additional field {item}")
                setattr(self, item, kwargs[item][:])
                self.extra_fields.append(item)
            else:
                LOGGER.debug(f"Found additional context variable {item}")
                extra_variables[item] = kwargs[item]

        self.ctx = context.setup_context(
            {**context_in, **extra_variables}, allowed, types, defaults,
            verbosity=verbosity)

        self.ctx['prec'] = 'float{}'.format(self.ctx['prec'])

        # assign objects
        self.pixels = {}
        self.set_coordinates(alphas, deltas, pixels)
        self.set_ellipticities(e1s, e2s)
        self.set_weights(weights)
        self.set_redhift_bins(redshift_bins)
        if store_pix:
            LOGGER.debug("Only storing pixels instead of ra,dec")
            self.pixels[0] = self._pixelize(alphas, deltas)
            self.alpha = []
            self.delta = []
            self.store_pix = True
        else:
            self.store_pix = False

        self._assert_lengths()

    ##################
    # ACCESING OBJECTS
    ##################

    def get_coordinates(self, bin=0):
        """
        Returns the coordinates of the catalog objects

        :param bin: Indicate the redshift bin of the objects which should be
                    returned. If 0 all bins are used.
        """
        idx = self._get_redshift_bool(bin)
        if len(self.alpha) > 0:
            return self.alpha[idx], self.delta[idx]
        else:
            LOGGER.info(
                "Found only pixel coordinates. "
                "Converting to angular coordinates.")
            delta, alpha = hp.pixelfunc.pix2ang(self.ctx['NSIDE'],
                                                self.pixels[0][idx])
            if self.ctx['degree']:
                LOGGER.debug("Returning coordinates in degrees")
                alpha = np.degrees(alpha)
                delta = np.degrees(delta)
                if not self.ctx['colat']:
                    delta = 90. - delta
                else:
                    LOGGER.debug("Returning coordinates in co-latitude")
            else:
                if not self.ctx['colat']:
                    delta = np.pi / 2. - delta
                else:
                    LOGGER.debug("Returning coordinates in co-latitude")
            return alpha, delta

    def get_ellipticities(self, bin=0):
        """
        Returns the ellipticities of the catalog objects

        :param bin: Indicate the redshift bin of the objects which should be
                    returned. If 0 all bins are used.
        """
        idx = self._get_redshift_bool(bin)
        return self.e1s[idx], self.e2s[idx]

    def get_redshift_bins(self, bin=0):
        """
        Returns the redshift bins of the catalog objects

        :param bin: Indicate the redshift bin of the objects which should be
                    returned. If 0 all bins are used.
        """
        bin = int(bin)
        idx = self._get_redshift_bool(bin)
        return self.redshift_bin[idx]

    def get_weights(self, bin=0):
        """
        Returns the weights of the catalog objects

        :param bin: Indicate the redshift bin of the objects which should be
                    returned. If 0 all bins are used.
        """
        bin = int(bin)
        idx = self._get_redshift_bool(bin)
        return self.weights[idx]

    def get_pixels(self, pix_key=0, bin=0):
        """
        Returns the shears of the catalog objects

        :param pix_key: If multiple rotated versions of the original catalog
                        are stored can access them with the pix_key index.
                        Only works if store_pix was set to True.
        :param bin: Indicate the redshift bin of the objects which should be
                    returned. If 0 all bins are used.
        """
        idx = self._get_redshift_bool(bin)
        # if pixels not set
        if (len(self.pixels.keys()) == 0) & (pix_key == 0):
            LOGGER.debug("Converting coordinates to pixels")
            pixs = self._pixelize(self.alpha, self.delta, bin=bin)
            return pixs
        else:
            if pix_key in self.pixels.keys():
                return self.pixels[pix_key][idx]
            else:
                raise KeyError(
                    f"No pixels with key number {pix_key} found. "
                    "Rotate catalog first")

    # SETTING OBJECTS
    def set_coordinates(self, alphas, deltas, pixels=[]):
        """
        Sets coordinate arrays
        :param alphas: First coordinates
        :param deltas: Second coordinates
        :param pixels: Alternatively can pass list of
        pixels instead of angular coordinates
        """
        if len(pixels) > 0:
            LOGGER.debug("Go list of pixels. Ignoring passed ra,decs.")
            delta, alpha = hp.pixelfunc.pix2ang(self.ctx['NSIDE'], pixels)

            # converting coordinates
            if self.ctx['degree']:
                LOGGER.debug("Setting coordinates in degrees")
                alpha = np.degrees(alpha)
                delta = np.degrees(delta)
                if not self.ctx['colat']:
                    delta = 90. - delta
                else:
                    LOGGER.debug("Setting coordinates in co-latitude")
            else:
                if not self.ctx['colat']:
                    delta = np.pi / 2. - delta
                else:
                    LOGGER.debug("Setting coordinates in co-latitude")

            self.alpha = alpha
            self.delta = delta
        else:
            self.alpha = alphas[:]
            self.delta = deltas[:]

    def set_ellipticities(self, e1s, e2s):
        """
        Sets elliticity arrays

        :param e1s: First  ellipticity component
        :param e2s: Second ellipticity component
        """
        if (len(e1s) == 0):
            LOGGER.warning(
                "Passed empty list for first ellipicities. Setting all to 0")
            self.e1s = np.zeros_like(self.alpha)
        if (len(e2s) == 0):
            LOGGER.warning(
                "Passed empty list for second ellipicities. Setting all to 0")
            self.e2s = np.zeros_like(self.alpha)
        else:
            self.e1s = e1s[:]
            self.e2s = e2s[:]

    def set_redhift_bins(self, redshift_bins):
        """
        Sets redshift bin array

        :param redshift_bins: Redshift bins for the stored objects.
                              If empty set to 0
        """
        if len(redshift_bins) == 0:
            LOGGER.warning("Passed empty list for redshifts. Setting all to 0")
            self.redshift_bin = np.zeros_like(self.alpha, dtype=int)
        else:
            self.redshift_bin = redshift_bins[:]

    def set_weights(self, weights):
        """
        Sets weight array

        :param weights: weights for the stored objects. If empty set to 1.
        """
        if len(weights) == 0:
            LOGGER.warning("Passed empty list for weights. Setting all to 1")
            self.weights = np.ones_like(self.alpha, dtype=int)
        else:
            self.weights = weights[:]

    # METHODS
    def clip_ellipticities(self, clip_value):
        """
        Clips ellipticities at a provided value.
        All objects exceeding sqrt(e1^2+e2^2) > clip_value are removed.

        :param clip_value: The maximum absolute values
                           of the ellipticities that is allowed
        """

        if len(self.e1s) == 0:
            raise Exception("Cannot clip ellipticities because none are set.")

        # clipping
        clip_value = float(clip_value)
        gamma_mag = np.sqrt(self.e1s**2. + self.e2s**2.)
        flagged = np.where(gamma_mag > clip_value)[0]

        LOGGER.info(
            f"Clipped ellipticity to {clip_value} -> "
            f"Removed {len(flagged)/len(self.e1s) * 100.}% of objects.")

        # remove flagged elements
        self.e1s = np.delete(self.e1s, flagged)
        self.e2s = np.delete(self.e2s, flagged)
        if len(self.alpha) > 0:
            self.alpha = np.delete(self.alpha, flagged)
            self.delta = np.delete(self.delta, flagged)
        for k in self.pixels.keys():
            self.pixels[k] = np.delete(self.pixels[k], flagged)
        self.redshift_bin = np.delete(self.redshift_bin, flagged)
        self.weights = np.delete(self.weights, flagged)
        for field in self.extra_fields:
            foo = np.delete(getattr(self, field), flagged)
            setattr(self, field, foo)

    def rotate_catalog(self, alpha_rot, delta_rot, store_pixels=False,
                       mirror=False, rotate_ellipticities=False):
        """
        Rotates the galaxy coordinates on the sky. Can overwrite coordinates
        or just store the pixel coordinates of the rotated survey.

        :param alpha_rot: The angle along the first coordinates
                          to rotate (in radians)
        :param delta_rot: The angle along the second coordinates
                          to rotate (in radians)
        :param store_pixels: If False the old coordinates are overwritten.
                             If True old coordinates are conserved and only the
                             pixel numbers of the rotated objects are stored in
                             self.pixels. Allows holding many rotated catalogs
                             without requiring too much memory.
        :param mirror: If True mirrors all coordinates on the equator
        :param rotate_ellipticities: If True rotates the ellipticities as well.
                                     Only supported for store_pixels=False
                                     and mirror=False.
        """

        alpha, delta = self._rotate_coordinates(
            alpha_rot, delta_rot, mirror)

        if store_pixels:
            pixs = self._pixelize(alpha, delta, bin=0, full_output=False)
            key = len(self.pixels.keys())
            self.pixels[key] = pixs
            LOGGER.info(
                "The pixel locations of the rotated catalog have been "
                "stored but the coordinates were rotated back")
        else:
            self.alpha, self.delta = alpha, delta
            if rotate_ellipticities:
                if store_pixels:
                    raise Exception(
                        "store_pixel is not supported "
                        "if rotate_ellipticities is used.")
            if len(self.e1s) > 0:
                self.e1s, self.e2s = self._rotate_ellipticities(
                    alpha_rot, delta_rot, mirror)

    def get_object_pixels(self, bin=0, alpha_rot=0.0, delta_rot=0.0, pix=-1,
                          mirror=False):
        """
        Returns the pixel of each object, all unique pixels where the
        objects are located and the object indices in each
        pixel. Can optionally rotate the catalog before returning products.

        :param bin: Redshift bin to use (0=full sample)
        :param alpha_rot: The angle along the first coordinates to rotate
        :param delta_rot: The angle along the second coordinates to rotate
        :param pix: Alternative operation mode. Uses the stored pixel catalogs
                    instead of the actual coordinates (-1 not used, greater or
                    equal than 0 indicates the map to use)
        :param mirror: If True mirrors coordinates on equator
        :return: Three lists containing the different pixelization information
        """

        # pixelize the coordinates
        if pix < -0.5:
            if len(self.alpha) == 0:
                raise Exception(
                    "No coordinates are set. "
                    "Cannot convert to pixel locations.")

            # rotate catalog if appicable
            if (not np.isclose(alpha_rot, 0.0)) | \
               (not np.isclose(delta_rot, 0.0)) | \
               (mirror):
                alpha, delta = self._rotate_coordinates(
                    alpha_rot, delta_rot, mirror)
            else:
                alpha = self.alpha
                delta = self.delta
            unis, indices, pixs = self._pixelize(
                alpha, delta, bin, full_output=True)
        else:
            pixs = self.pixels[pix]
            unis, indices = np.unique(
                pixs, return_inverse=True)

        return (pixs, unis, indices)

    def get_map(self, type, bin=0, alpha_rot=0.0, delta_rot=0.0,
                pix=-1, trimming=True, mirror=False, normalize=True,
                method='KS'):
        """
        Creates number count, weight, shear and convergence maps
        or custom field map from the catalog.
        Can optionally rotate the catalog before map creation.
        :param type: Can be counts, weights, ellipticities, convergence,
        a custom field or a list of them.
        Indicates types of the maps that are returned.
        The object weights are applied in the creation
        of all the maps except for the counts and weights map.
        Note that ellipticities and convergence return
        two maps each (e1, e2) and (E, B) respectively.
        :param bin: Redshift bin to use (0=full sample)
        :param alpha_rot: The angle along the first coordinates to rotate
        :param delta_rot: The angle along the second coordinates to rotate
        :param pix: Alternative operation mode. Uses the stored pixel catalogs
        instead of the actual coordinates (-1 not used, greater or
        equal than 0 indicates the instance to use)
        :param trimming: If True applies stricter masking to convergence map
        (some values on edges of survey mask can be
        very off due to spherical harmonics transformation).
        :param mirror: If True mirrors coordinates on equator
        :param normalize: If True all maps except for the counts and weights
        maps are normalized by the sum of all object weights per pixel.
        :param method: Mass mapping method for convergence maps.
        At the moment can only be KS (Kaiser-Squires).
        :return: The desired maps in a list (map1, map2, ...)
        """

        pixs, unis, indices = self.get_object_pixels(
            bin, alpha_rot, delta_rot, pix, mirror)

        # Do not touch!
        sign_flip = True

        if not isinstance(type, list):
            type = [type]

        # check if all desired fields are present
        output_type = "Returning maps in order: "
        for field in type:
            if (field != 'convergence') & (field != 'ellipticities') \
                    & (field != 'weights') \
                    & (field != 'counts'):
                try:
                    getattr(self, field)
                    output_type += f"{field}, "
                except AttributeError:
                    type.remove(field)
                    LOGGER.warning(
                        "Did not find field {}. Skipping...".format(field))
            else:
                output_type += f"{field}, "
        output_type = output_type[:-2]

        output = []

        idx = self._get_redshift_bool(bin)

        # calculate the weights map
        weights = np.zeros(hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                           dtype=float)
        weights[unis] += np.bincount(indices, weights=self.weights[idx])

        if 'counts' in type:
            # calculate the count map
            LOGGER.debug("Calculating object count map")
            count_weights = np.zeros(pixs.size)
            count_weights[idx] = 1.0
            counts = np.zeros(hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                              dtype=float)
            counts[unis] += np.bincount(indices, weights=count_weights)
            output.append(counts)

        if 'weights' in type:
            LOGGER.debug("Calculating weight map")
            output.append(weights)

        if 'ellipticities' in type:
            LOGGER.debug("Calculating ellipticity maps")
            # calculate the shear maps
            ellipticity_map_1 = np.zeros(
                hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                dtype=self.ctx['prec'])
            ellipticity_map_1[unis] += np.bincount(
                indices, weights=self.weights[idx] * self.e1s[idx])
            ellipticity_map_2 = np.zeros(
                hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                dtype=self.ctx['prec'])
            ellipticity_map_2[unis] += np.bincount(
                indices, weights=self.weights[idx] * self.e2s[idx])

            mask = np.logical_not(weights > 0.0)

            if normalize:
                widx = np.logical_not(mask)
                ellipticity_map_1[widx] = \
                    ellipticity_map_1[widx] / weights[widx]
                ellipticity_map_2[widx] = \
                    ellipticity_map_2[widx] / weights[widx]

            # masking
            ellipticity_map_1[mask] = hp.pixelfunc.UNSEEN
            ellipticity_map_2[mask] = hp.pixelfunc.UNSEEN

            output.append(ellipticity_map_1)
            output.append(ellipticity_map_2)

        if 'convergence' in type:
            LOGGER.debug("Calculating convergence maps")
            if 'ellipticities' not in type:
                # calculate the shear maps
                ellipticity_map_1 = np.zeros(
                    hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                    dtype=self.ctx['prec'])
                ellipticity_map_1[unis] += np.bincount(
                    indices, weights=self.weights[idx] * self.e1s[idx])
                ellipticity_map_2 = np.zeros(
                    hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                    dtype=self.ctx['prec'])
                ellipticity_map_2[unis] += np.bincount(
                    indices, weights=self.weights[idx] * self.e2s[idx])

                mask = np.logical_not(weights > 0.0)

                if normalize:
                    widx = np.logical_not(mask)
                    ellipticity_map_1[widx] = \
                        ellipticity_map_1[widx] / weights[widx]
                    ellipticity_map_2[widx] = \
                        ellipticity_map_2[widx] / weights[widx]

                # masking
                ellipticity_map_1[mask] = hp.pixelfunc.UNSEEN
                ellipticity_map_2[mask] = hp.pixelfunc.UNSEEN
            # calculate convergence maps
            m_kappa_E, m_kappa_B = self._calc_convergence_map(
                ellipticity_map_1, ellipticity_map_2, weights, bin,
                trimming, sign_flip, method,
                unis, indices, idx, normalize)

            output.append(m_kappa_E)
            output.append(m_kappa_B)

        for field in type:
            if (field != 'convergence') & (field != 'ellipticities') \
                    & (field != 'weights') \
                    & (field != 'counts'):
                LOGGER.debug(f"Calculating {field} map")
                map_1 = np.zeros(hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                                 dtype=self.ctx['prec'])
                map_1[unis] += np.bincount(
                    indices,
                    weights=self.weights[idx] * getattr(self, field)[idx])

                mask = np.logical_not(weights > 0.0)
                if normalize:
                    widx = np.logical_not(mask)
                    map_1[widx] = map_1[widx] / weights[widx]

                # masking
                map_1[mask] = hp.pixelfunc.UNSEEN
                output.append(map_1)

        LOGGER.debug(output_type)
        return output

    def get_mask(self, bin=0, alpha_rot=0.0, delta_rot=0.0, mirror=False):
        """
        Returns binary survey mask. Can optionally rotate catalog on sky.

        :param bin: Redshift bin to use (0=full sample)
        :param alpha_rot: The angle along the first coordinates to rotate
        :param delta_rot: The angle along the second coordinates to rotate
        :param mirror: If True mirrors coordinates on equator
        :return: A Healpix mask (0 outside and 1 inside of mask)
        """

        weights = self.get_map('weights', bin, alpha_rot,
                               delta_rot, mirror=mirror)[0]
        mask = weights > 0.0

        return mask

    def get_trimmed_mask(self, bin=0, alpha_rot=0.0, delta_rot=0.0,
                         mirror=False, accepted_error=0.05, smoothing=21.1):
        """
        Given a Healpix mask creates a trimmed mask, meaning it removes some
        pixels which are distored by edge
        effects in shear->convergence procedure.
        Optionally allows rotation of catalog.

        :param bin: Redshift bin to use (0=full sample)
        :param alpha_rot: The angle along the first coordinates to rotate
        :param delta_rot: The angle along the second coordinates to rotate
        :param mirror: If True mirrors coordinates on equator
        :param accepted_error: Maximum fractional error of pixels after
                               smoothing for trimming
        :param smoothing: FWHM of Gaussian kernel for smoothing in arcmin.
        :return: The trimmed Healpix mask
        """
        mask = self.get_mask(bin=bin, alpha_rot=alpha_rot,
                             delta_rot=delta_rot, mirror=mirror)
        mask = self._trimming(mask, accepted_error=accepted_error,
                              smoothing=smoothing)

        return mask

    def generate_shape_noise(self, seed=None, bin=0, fields=None,
                             input_fields=None):
        """
        Generates shape noise which resembles the noise in the original
        catalog by randomly rotating the ellipticities in place.

        :param seed: Seeding for the random generation of the rotation.
        :param bin: Redshift bin to use (0=full sample)
        :param fields: Can also provide a list of fields to randomize.
                      If two field names are given as a list they are
                      intrepreted as the two components of a spin-2
                      field and rotated like the ellipticities,
                      otherwise a scalar field is assumed and
                      the noise is drawn from its global distribution.
        :param input_fields: Provide list of fields directly instead of using
                            internal fields.
        :return: The new randomized fields
        """

        # Seeding
        if seed is not None:
            np.random.seed(int(seed))
            LOGGER.debug(f"Seeded random generater with seed {seed}")

        if input_fields is not None:
            LOGGER.debug("Not using internal fields but input_fields!")
            field_1 = input_fields[0]
            idx = np.ones(len(field_1), dtype=bool)
            try:
                field_2 = input_fields[1]
            except KeyError:
                pass
        else:
            idx = self._get_redshift_bool(bin)
            if (not isinstance(fields, list)) & (fields is not None):
                fields = [fields]

            if fields is None:
                LOGGER.debug("Using ellipticities")
                field_1 = self.e1s
                field_2 = self.e2s
            elif isinstance(fields, list):
                if isinstance(fields[0], str):
                    field_1 = getattr(self, fields[0])
                else:
                    raise Exception(
                        "First field must be of type string, "
                        "but received {}".format(type(fields[0])))
                try:
                    if isinstance(fields[1], str):
                        field_2 = getattr(self, fields[1])
                    else:
                        raise Exception(
                            "Second field must be of type string, "
                            "but received {}".format(type(fields[1])))
                except IndexError:
                    field_2 = None
            else:
                raise Exception(
                    "Fields argument must be of type string or "
                    "list of strings, but received {}".format(type(fields)))

        if field_2 is not None:
            LOGGER.debug("Assuming spin2 field")
            # Draw random phase
            ell = len(field_1[idx])

            # Generate random phase
            rad, ang = self._from_rec_to_polar(
                field_1[idx] + field_2[idx] * 1j)
            ang += np.pi
            ang = (ang + np.random.uniform(0.0, 2.0 * np.pi, ell)
                   ) % (2.0 * np.pi) - np.pi

            noise_shear = self._from_polar_to_rec(rad, ang)

            noise_shear_1 = np.real(noise_shear)
            noise_shear_2 = np.imag(noise_shear)
            return noise_shear_1, noise_shear_2
        else:
            LOGGER.debug("Assuming scalar field")
            # If only one field passed, draw from global distribution of pixels
            interp_steps = 10000
            min = np.min(field_1)
            max = np.min(field_1)

            pdf = stats.binned_statistic(
                field_1[idx],
                np.ones_like(field_1[idx]),
                statistic=sum, bins=interp_steps, range=(min, max))[0]

            # normalize
            pdf /= np.sum(pdf)
            # get cumulative function
            pdf = np.cumsum(pdf)

            # create interplator for inverted function
            steps = np.linspace(min, max, interp_steps)

            pdf_inv = scipy.interpolate.interp1d(pdf, steps)

            noise = pdf_inv(np.random.random(len(field_1[idx])))
            return [noise]

    def generate_shape_noise_map(self, seed=None, pix=-1, bin=0,
                                 normalize=True, fields=None):
        """
        Generates shape noise maps.
        :param seed: Seeding for the random generation of the rotation
        :param pix: Alternative operation mode. Uses the stored pixel catalogs
        instead of the actual coordinates(-1 not used, greater or
        equal than 0 indicates the map to use)
        :param bin: Redshift bin to use (0=full sample)
        :param normalize: If True the maps
        are normalized by the sum of all object weights per pixel.
        :param fields: Can also provide a list of fields to randomize.
        If two field names are given as a list they are
        intrepreted as the two components of a spin-2
        field and rotated like the ellipticities,
        otherwise a scalar field is assumed and
        the noise is drawn from its global distribution.
        :return: Two shape noise maps.
        """

        out = self.generate_shape_noise(seed, bin, fields=fields)

        pixs, unis, indices = self.get_object_pixels(
            bin, alpha_rot=0.0, delta_rot=0.0, pix=pix, mirror=False)

        idx = self._get_redshift_bool(bin)

        # calulate weights maps
        weights = np.zeros(hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                           dtype=float)
        weights[unis] += np.bincount(indices, weights=self.weights[idx])
        mask = np.logical_not(weights > 0.0)

        output = []
        for field in out:
            noise_field_map = np.zeros(
                hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                dtype=self.ctx['prec'])

            noise_field_map[unis] += np.bincount(
                indices, weights=self.weights[idx] * field)

            if normalize:
                widx = np.logical_not(mask)
                noise_field_map[widx] = noise_field_map[widx] / weights[widx]

            # masking
            noise_field_map[mask] = hp.pixelfunc.UNSEEN

            output.append(noise_field_map)

        return output

    ##################################
    # HELPER FUNCTIONS
    ##################################
    def _pixelize(self, alpha, delta, bin=0, full_output=False):
        """
        Converts angular coordinates into HEalpix map
        """

        # Handling for 1 sized arrays
        if isinstance(alpha, float):
            alpha = [alpha]
        if isinstance(delta, float):
            delta = [delta]

        idx = self._get_redshift_bool(bin)

        # converting coordinates to HealPix convention
        if self.ctx['degree']:
            alpha = np.radians(alpha)
            delta = np.radians(delta)
        if not self.ctx['colat']:
            delta = np.pi / 2. - delta
        pix = hp.pixelfunc.ang2pix(self.ctx['NSIDE'], delta[idx], alpha[idx])
        pix = pix.astype(int)

        # converting coordinates back
        if self.ctx['degree']:
            alpha = np.degrees(alpha)
            delta = np.degrees(delta)
        if not self.ctx['colat']:
            delta = 90. - delta

        if full_output:
            unis, indices = np.unique(
                pix, return_inverse=True)
            return unis, indices, pix
        else:
            return pix

    def _trimming(self, mask, accepted_error=0.05, smoothing=21.1):
        """
        Applys smoothing to a mask and removes pixels that are too far off.
        """
        mask = mask.astype(float)

        # Apply smoothing
        mask = hp.smoothing(mask, fwhm=np.radians(smoothing / 60.))

        # Only keep pixels with values in tolerance
        idx = np.abs(mask - 1.0) > accepted_error

        mask[idx] = 0.0
        mask[np.logical_not(idx)] = 1.0
        mask = mask.astype(bool)
        return mask

    def _calc_convergence_map(self, ellipticity_map_1, ellipticity_map_2,
                              weights, bin=0,
                              trimming=True, sign_flip=True, method='KS',
                              unis=[], indices=[], idx=[], normalize=True):
        """
        calculate the convergence maps from ellipticity maps
        """
        if sign_flip & (len(ellipticity_map_1) > 0):
            LOGGER.debug("Applying sign flip")
            ellipticity_map_1[ellipticity_map_1 > hp.UNSEEN] *= -1.

        if method == 'N0oB':
            # NOT SUPPORTED
            # make ellipticity error maps
            ellipticity_map_1_std = np.zeros(
                hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                dtype=self.ctx['prec'])
            ellipticity_map_1_std[unis] += np.bincount(
                indices,
                weights=self.weights[idx]
                * (self.e1s[idx] - ellipticity_map_1[unis][indices])**2.)
            ellipticity_map_2_std = np.zeros(
                hp.pixelfunc.nside2npix(self.ctx['NSIDE']),
                dtype=self.ctx['prec'])
            ellipticity_map_2_std[unis] += np.bincount(
                indices,
                weights=self.weights[idx]
                * (self.e2s[idx] - ellipticity_map_2[unis][indices])**2.)

            mask = np.logical_not(weights > 0.0)

            if normalize:
                widx = np.logical_not(mask)
                ellipticity_map_1_std[widx] = \
                    ellipticity_map_1_std[widx] / weights[widx]
                ellipticity_map_2_std[widx] = \
                    ellipticity_map_2_std[widx] / weights[widx]

            # masking
            ellipticity_map_1_std[mask] = hp.pixelfunc.UNSEEN
            ellipticity_map_2_std[mask] = hp.pixelfunc.UNSEEN
        else:
            ellipticity_map_1_std = []
            ellipticity_map_2_std = []
        alm_E, alm_B = utils._calc_alms(
            ellipticity_map_1, ellipticity_map_2,
            method=method,
            shear_1_err=ellipticity_map_1_std,
            shear_2_err=ellipticity_map_2_std)
        if sign_flip & (len(ellipticity_map_1) > 0):
            ellipticity_map_1[ellipticity_map_1 > hp.UNSEEN] *= -1.

        m_kappa_B = np.asarray(hp.alm2map(alm_B, nside=self.ctx['NSIDE']),
                               dtype=self.ctx['prec'])
        m_kappa_E = np.asarray(hp.alm2map(alm_E, nside=self.ctx['NSIDE']),
                               dtype=self.ctx['prec'])

        # masking
        if not trimming:
            LOGGER.debug(
                "Note: Conversion to convergence can introduce artefacts "
                "To be sure apply more conservative cut using trimmed mask.")
            m_kappa_E[np.logical_not(weights > 0.0)] = hp.pixelfunc.UNSEEN
            m_kappa_B[np.logical_not(weights > 0.0)] = hp.pixelfunc.UNSEEN
        else:
            mask = self._trimming(weights > 0.0)
            mask = np.logical_not(mask)
            m_kappa_E[mask] = hp.pixelfunc.UNSEEN
            m_kappa_B[mask] = hp.pixelfunc.UNSEEN

        return m_kappa_E, m_kappa_B

    def _from_rec_to_polar(self, x):
        """
        Takes a standard comlex number or sequence of
        complex numbers and return the polar coordinates.
        """
        return abs(x), np.angle(x)

    def _from_polar_to_rec(self, radii, angles):
        """
        Takes polar coordinates of a complex number or
        a sequence and returns a standard complex number.
        """
        return radii * np.exp(1j * angles)

    def _get_redshift_bool(self, bin=0):
        """
        Get the indices of the objects in a certain redshift bin.
        """
        bin = int(bin)
        if len(self.redshift_bin) == 0:
            raise Exception("Redshift bins not set. Cannot select objects")
        if bin == 0:
            idx = np.ones_like(self.redshift_bin)
        else:
            idx = np.isclose(self.redshift_bin, bin)

        if len(idx) == 0:
            raise Exception(f"No objects found for bin {bin}")
        idx = idx.astype(bool)
        return idx

    def _rotate_coordinates(self, alpha_rot, delta_rot, mirror):
        """
        rotate the coordinates
        """
        if len(self.alpha) > 0:
            alpha = self.alpha
            delta = self.delta
            # converting coordinates to HealPix convention
            if self.ctx['degree']:
                alpha = np.radians(alpha)
                delta = np.radians(delta)
            if not self.ctx['colat']:
                delta = np.pi / 2. - delta
        else:
            try:
                pix = self.pixels[0]
            except KeyError:
                raise Exception(
                    "Cannot access the pixel object and coordinates not set")
            delta, alpha = hp.pixelfunc.pix2ang(self.ctx['NSIDE'], pix)

        if mirror:
            delta = np.pi - delta

        # Healpix rotator
        rot = hp.rotator.Rotator(rot=[alpha_rot, delta_rot], deg=False)

        rot_delta, rot_alpha = rot(delta, alpha)

        if len(self.alpha) > 0:
            # converting coordinates back
            if self.ctx['degree']:
                alpha = np.degrees(alpha)
                delta = np.degrees(delta)
            if not self.ctx['colat']:
                delta = 90. - delta

        # converting rotated coordinates back
        if self.ctx['degree']:
            rot_alpha = np.degrees(rot_alpha)
            rot_delta = np.degrees(rot_delta)
        if not self.ctx['colat']:
            rot_delta = 90. - rot_delta

        return rot_alpha, rot_delta

    def _rotate_ellipticities(self, alpha_rot, delta_rot, mirror):
        """
        rotate the coordinates
        """

        # converting coordinates to HealPix convention
        if self.ctx['degree']:
            alpha = np.radians(self.alpha)
            delta = np.radians(self.delta)
        if not self.ctx['colat']:
            delta = np.pi / 2. - delta

        if mirror:
            raise Exception(
                "Rotation of ellipticities not supported if mirror is True.")

        # Healpix rotator
        rot = hp.rotator.Rotator(rot=[alpha_rot, delta_rot], deg=False)

        theta_pix_center_back, phi_pix_center_back = rot.I(alpha, delta)

        ref_angle = rot.angle_ref(theta_pix_center_back, phi_pix_center_back)

        rad, ang = self._from_rec_to_polar(self.e1s + self.e2s * 1j)
        ang += 2. * ref_angle
        x = self._from_polar_to_rec(rad, ang)

        return np.real(x), np.imag(x)

    def _assert_lengths(self):
        """
        checks that the lengths of the objects are consistent
        """
        if self.store_pix:
            length = len(self.pixels[0])
        else:
            length = len(self.alpha)

        try:
            assert len(self.e2s) == length
            assert len(self.e1s) == length
            assert len(self.redshift_bin) == length
            assert len(self.weights) == length
            if not self.store_pix:
                assert len(self.delta) == length
            for k in self.pixels.keys():
                assert len(self.pixels[k]) == length
        except AssertionError:
            raise Exception(
                "Lengths of the objects passed to estats.catalog do not match")
