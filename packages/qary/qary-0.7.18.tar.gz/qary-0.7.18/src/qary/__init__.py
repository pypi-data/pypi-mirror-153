# -*- coding: utf-8 -*-
__version__ = 'unknown'

try:
    from pkg_resources import get_distribution, DistributionNotFound
except ImportError as e:
    print(e)

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound as e:
    print(e)
finally:
    del get_distribution, DistributionNotFound


# from qary.init import maybe_download  # noqa
