# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher Oct 2019

import numpy as np
import collections
from ekit import logger
from pathlib import Path

LOGGER = logger.init_logger(__name__)


def create_path(identity, out_folder=None, defined_parameters={},
                undefined_parameters=[], suffix='', verbosity=3):
    """
    Creates a standardised path for files. The meta data is encoded in the path
    and can be savely recovered using the get_parameters_from_path function.
    NOTE: Your variable names must not contain underscores or equal signs!

    :param identity: The prefix of the name.
    :param out_folder: The directory of the file.
    :param defined_parameters: A dictionary of key value pairs.
    :param undefined_parameters: A list of parameters that do not have a name
                                (be mindful about their order when
                                reading them from the name again!).
    :param suffix: What should go at the end of the name.
    :param verbosity: Verbosity level (0 - 4).
    :return: A string which is the created path.
    """

    logger.set_logger_level(LOGGER, verbosity)

    if out_folder is None:
        outstring = identity
    else:
        outstring = f"{out_folder}/{identity}"

    # order by keys to remove ambigous ordering
    defined_parameters = collections.OrderedDict(sorted(
                                                 defined_parameters.items()))

    # add the defined parameters
    for key in defined_parameters.keys():
        LOGGER.debug(
            f"Adding defined key {key} "
            f"with value {defined_parameters[key]}")
        add = '_{}={}'.format(key, defined_parameters[key])
        outstring = outstring + add

    # add the undefined parameters
    for param in undefined_parameters:
        LOGGER.debug(
            f"Adding undefined parameter with value {undefined_parameters}")
        add = '_{}'.format(param)
        outstring = outstring + add

    # add suffix
    outstring += suffix

    return outstring


def get_parameters_from_path(paths, suffix=True, fmt=None, verbosity=3):
    """
    Given a list of standardised paths, or a single path created with
    create_path() this function reads the parameters in the paths.

    :param paths: Either a single string or a list of strings. The strings
                  should be paths in the create_path() format.
    :param suffix: If True assumes that the given paths have suffixes
    :param fmt: Format string in format: %s_%i_%b etc. The order is the same
                as the attributes that should be read from the path.
                Accepts: %s = string, %i = integer, %f = float, %b = boolean
    :param verbosity: Verbosity level (0 - 4).
    :return: Returns a dictionary which contains the defined parameters and
             a list containing the undefined parameters.
    """

    logger.set_logger_level(LOGGER, verbosity)

    if fmt is not None:
        LOGGER.debug(f"Received format string: {fmt}")
        fmt = fmt.split("_")

    # convert to list if needed
    if not isinstance(paths, list):
        paths = [paths]

    LOGGER.debug(f"Found {len(paths)} path(s) to process.")

    # use first path to initialize the dictionary and list for output
    defined_names = []
    undefined_count = 0
    path = paths[0]
    path = _prepare_path(path, suffix=suffix)
    for c in path:
        if isinstance(c, list):
            c = c[0]
        if '=' in c:
            # named parameter
            b = c.split('=')
            defined_names.append(b[0])
        else:
            undefined_count += 1

    LOGGER.debug(
        f"Extracting {len(defined_names)} named parameters from path.")
    LOGGER.debug(
        f"Extracting {undefined_count} unnamed parameters from path.")

    # initialize output directory / list
    undefined = np.zeros((len(paths), undefined_count), dtype=object)
    defined = {}
    for d in defined_names:
        defined[d] = np.zeros(len(paths), dtype=object)

    # loop over files and get parameters
    for ii, path in enumerate(paths):
        path = _prepare_path(path, suffix=suffix)
        count = 0
        for idx_c, c in enumerate(path):
            if isinstance(c, list):
                c = c[0]
            if '=' in c:
                # named parameter
                b = c.split('=')
                to_add = _check_type(b[1], fmt, idx_c)
                defined[b[0]][ii] = to_add
            else:
                to_add = _check_type(c, fmt, idx_c)
                undefined[ii, count] = to_add
                count += 1
    LOGGER.debug(f"Extracted named parameters: {defined}")
    LOGGER.debug(f"Extracted unnamed parameters: {undefined}")
    return defined, undefined


def mkdir_on_demand(path, exist_ok=True, parents=True, verbosity=3):
    """
    Creates a directory if it does not exist.
    Just a wrapper around pathlib but kept for backwards compatibility.

    :param path: The path to the directory that should be created.
    :param exist_ok: If set to True ignores errors raised if
    directory already exists.
    :param parents: If True creates full directory tree.
    :param verbosity: Verbosity level (0 - 4).
    """

    logger.set_logger_level(LOGGER, verbosity)

    Path(path).mkdir(parents=parents, exist_ok=exist_ok)
    LOGGER.info(f"Created directory-tree for {path}")


def _check_type(in_, fmt, idx):
    if fmt is not None:
        try:
            format = fmt[idx]
        except IndexError:
            format = None
    else:
        format = None

    if format is not None:
        if format[1] == 'b':
            if in_ == 'True':
                to_add = True
            elif in_ == 'False':
                to_add = False
            else:
                raise ValueError(
                    f"String {in_} cannot be interpreted "
                    "as a boolean. Must be True or False.")
        elif format[1] == 'i':
            to_add = int(in_)
        elif format[1] == 'f':
            to_add = float(in_)
        elif format[1] == 's':
            to_add = str(in_)
        else:
            raise ValueError(f"Did not recognize format string {format}")
    else:
        # check if boolean
        if in_ == 'True':
            to_add = True
        elif in_ == 'False':
            to_add = False
        else:
            # check if integer
            try:
                to_add = int(in_)
            except ValueError:
                # check if float
                try:
                    to_add = float(in_)
                except ValueError:
                    # else use string
                    try:
                        to_add = str(in_)
                    except ValueError:
                        raise ValueError(
                            "Did not understand parameter: "
                            f"{in_}. Not a bool, integer, "
                            "float nor string")

    return to_add


def _prepare_path(path, suffix=True):
    path = path.split('/')[-1]
    path = path.split('_')

    # do not consider identifier
    path = path[1:]

    # do not consider suffix
    if suffix:
        path[-1] = path[-1].split('.')[:-1]
    else:
        path[-1] = path[-1].split('.')
    path[-1] = '.'.join(path[-1])
    return path
