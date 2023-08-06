# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher Oct 2019

import os
import yaml
from pydoc import locate
from ekit import logger as log

LOGGER = log.init_logger(__name__)


def setup_context(ctx_in=None, allowed=[], types=[],
                  defaults=[], remove_unknowns=False,
                  verbosity=3, verbose=None, logger=None):
    """
    Sets up a context in the form a dictionary.

    :param ctx_in: If it is a directory containing keys corresponding to
                   parameter names defined in allowed they will be used.
                   If it is a valid path the file is assumed to be in YAML
                   format and the parameters are read from it.
    :param allowed: A list of the parameter names that are allowed
                    in the context.
    :param types: A list of the data types required for the parameters.
    :param defaults: A list of the default values of the parameters
                     (used if no other values found).
    :param remove_unknowns: If True then parameters that are in ctx_in but not
                            in allowed are not in the returned context.
    :param verbosity: Verbosity level (0 - 4).
    :param verbose: Only for backwards compatibility. Not used.
    :param logger: Only for backwards compatibility. Not used.
    :return: A directory containing all the parameter names
             and their assigned values.
    """

    log.set_logger_level(LOGGER, verbosity)

    ctx = {}

    # first set all parameters to their defaults
    for ii, parameter in enumerate(allowed):
        LOGGER.debug(
            f"Setting parameter {parameter} to default {defaults[ii]}")
        ctx[parameter] = defaults[ii]

    # check if config file path is given
    if isinstance(ctx_in, str):
        if os.path.isfile(ctx_in):
            LOGGER.info(f"Setting context using configuration file {ctx_in}.")
            with open(ctx_in, 'r') as f:
                CONF = yaml.load(f, yaml.FullLoader)
            for key in CONF.keys():
                if key in allowed:
                    if isinstance(CONF[key],
                                  locate(str(types[allowed.index(key)]))):
                        ctx[key] = CONF[key]
                        LOGGER.debug(f"Setting parameter {key} -> {CONF[key]}")
                    else:
                        raise ValueError(
                            f"Parameter {key} is not "
                            f"instance of type "
                            f"{locate(str(types[allowed.index(key)]))}")
                else:
                    if remove_unknowns:
                        LOGGER.warning(
                            f"Parameter {key} is not kown. Ignoring")
                    else:
                        LOGGER.debug(
                            f"Including parameter {key} although unknown.")
                        ctx[key] = CONF[key]
        else:
            raise FileNotFoundError("Path {} is not valid".format(ctx_in))

    # if parameters given directly as arguments overwrite
    elif ctx_in is not None:
        for key in ctx_in.keys():
            if key in allowed:
                if isinstance(ctx_in[key],
                              locate(str(types[allowed.index(key)]))):
                    LOGGER.debug(f"Setting parameter {key} -> {ctx_in[key]}")
                    ctx[key] = ctx_in[key]
                else:
                    raise ValueError(
                        f"Parameter {key} is not "
                        f"instance of type "
                        f"{locate(str(types[allowed.index(key)]))}")
            else:
                if remove_unknowns:
                    LOGGER.warning(f"Parameter {key} is not kown. Ignoring")
                else:
                    LOGGER.debug(
                        f"Including parameter {key} although unknown.")
                    ctx[key] = ctx_in[key]

    LOGGER.debug("Set context to:")
    LOGGER.debug('######################################')
    for parameter in allowed:
        LOGGER.debug(f"{parameter} : {ctx[parameter]}")
    LOGGER.debug('###################################### \n')

    return ctx
