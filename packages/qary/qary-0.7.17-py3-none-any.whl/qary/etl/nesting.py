# Recursive dictionary merge
# Copyright (C) 2016 Paul Durivage <pauldurivage+github@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import logging
import re

try:
    from collections.abc import Mapping
except ImportError:  # python <3.7
    from collections import Mapping
import copy


log = logging.getLogger(__name__)


def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.

    Inputs:
        dct (dict): dict into which the merge is executed
        merge_dct (dict): dict merged into dct
    Returns: None (only `dct` is updated in place)

    >>> old = dict(zip('abc', '123'))
    >>> new = dict(zip('cd', '34'))
    >>> dict_merge(old, new)
    >>> old == dict(zip('abcd', '1234'))
    True
    """
    for k, v in merge_dct.items():
        if (k in dct
                # TODO: test with dest `dict` replaced with `Mapping`
                and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def dict_diff(a, b):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.

    Inputs:
        a (dict): original dictionary
        b (dict): changed dictionary
    Returns:
        delta_a_to_b (dict): deepcopy of b with any unchanged k, v pairs deleted

    >>> old = {'a': '1', 'b': '2', 'c': '3'}
    >>> new = {                    'c': '3', 'd': 4}
    >>> dict_diff(old, new)
    {'d': 4, 'a': None, 'b': None}
    """
    abdiff = copy.deepcopy(b)
    keys_to_del = []
    for k, v in abdiff.items():
        if k in a:
            if isinstance(b[k], dict) and isinstance(a[k], Mapping):
                # TODO: test with dest `dict` replaced with `Mapping`
                abdiff[k] = dict_diff(a[k], b[k])
            elif abdiff[k] == a[k]:
                keys_to_del.append(k)
    for k, v in a.items():
        if k not in abdiff:
            abdiff[k] = None
    for k in keys_to_del:
        del abdiff[k]
    return abdiff


####################################################################
# duplicated in src/qary/etl/dialog.py

def default_normalizer(s, lower=True, underscores=True, strip=True):
    """ String normalizer: lower, strip whitespace, replace whitespace with underscores.

    >>> default_normalizer(' a a _')
    'a_a__'
    """
    if lower:
        s = str.lower(s)
    if strip:
        s = str.strip(s)
    if underscores:
        s = re.sub(r'[\s-]', '_', s)
    return s


def dict_key_normalize(unclean, normalizer=default_normalizer):
    """ Recursively lower, strip whitespace, replace whitespace with underscores.

    Inputs:
      unclean (dict): original dictionary
    Returns:
      clean (dict): deepcopy of clean with keys normalized

    >>> old = {' a a _': 1, '__b__': 2, 'c': {'  d  ': 3}}
    >>> dict_key_normalize(old)
    {'a_a__': 1, '__b__': 2, 'c': {'d': 3}}
    """
    clean = {}
    for k, v in unclean.items():
        if isinstance(unclean[k], Mapping):
            # TODO: test with dest `dict` replaced with `Mapping`
            clean[normalizer(k)] = dict_key_normalize(v, normalizer=normalizer)
        else:
            clean[normalizer(k)] = v
    return clean


def dict_replace(unclean, mapping, replace_values=True, replace_keys=False):
    """ Replace values in nested dicts according to the mapping provided

    >>> dict_replace(
    ...     {'W': {'a': 'True', 'b': True}, 'X': {'c': {False: {'d': True}}}},
    ...     mapping={False: 'n', True: 'y'})
    {'W': {'a': 'True', 'b': 'y'}, 'X': {'c': {False: {'d': 'y'}}}}
    """
    if replace_keys:
        raise NotImplementedError
    elif not replace_values:
        log.error('dict_replace() not doing anything!!!')
        return unclean
    clean = {}
    for k, v in unclean.items():
        if isinstance(unclean[k], Mapping):
            # TODO: test with dest `dict` replaced with `Mapping`
            clean[k] = dict_replace(v, mapping=mapping, replace_values=replace_values, replace_keys=replace_keys)
        else:
            clean[k] = mapping.get(v, v)
    return clean


def lod_replace(unclean, mapping, replace_values=True, replace_keys=False,
                list_types=(list, tuple), dict_types=(Mapping,)):
    """ Replace values in list of dicts according to mapping provided

    >>> lod_replace(
    ...     [{'a': 'True', 'b': True}, {'c': [False, {'d': True}]}],
    ...     mapping={False: 'n', True: 'y'})
    [{'a': 'True', 'b': 'y'}, {'c': ['n', {'d': 'y'}]}]
    """
    nonscalar_types = tuple(list(dict_types) + list(list_types))
    if not isinstance(mapping, Mapping):
        mapping = dict(mapping)
    if replace_keys:
        raise NotImplementedError
    elif not replace_values:
        log.error('dict_replace() not doing anything!!!')
        return unclean
    is_dict = isinstance(unclean, dict_types)
    is_list = isinstance(unclean, list_types)
    clean = {} if isinstance(unclean, dict_types) else []
    if is_list:
        item_generator = enumerate(unclean)
    elif is_dict:
        item_generator = unclean.items()
    else:
        return copy.copy(unclean)
    for k, v in item_generator:
        if isinstance(v, nonscalar_types):
            replaced_value = lod_replace(
                v, mapping=mapping,
                replace_values=replace_values, replace_keys=replace_keys)
        else:
            replaced_value = mapping.get(v, v)
        if is_list:
            clean.append(replaced_value)
        else:
            clean[k] = replaced_value
    return clean

# duplicated in src/qary/etl/dialog.py
####################################################################
