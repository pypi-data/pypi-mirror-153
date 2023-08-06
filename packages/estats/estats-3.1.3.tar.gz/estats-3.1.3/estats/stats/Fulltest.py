import numpy as np
import healpy as hp


def context():
    """
    Defines the parameters used by the plugin
    """
    stat_type = "multi"

    required = ["NSIDE"]
    defaults = [1024]
    types = ["int"]
    return required, defaults, types, stat_type


def Fulltest(maps, weights, ctx):
    map = np.zeros(hp.pixelfunc.nside2npix(ctx['NSIDE']))
    for key in maps.keys():
        map = maps[key] * weights[key]
    return np.asarray([[np.mean(map), np.std(map)]])
