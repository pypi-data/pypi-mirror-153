=========================
ekit - Version 0.2.% BETA
=========================

.. image:: https://cosmo-gitlab.phys.ethz.ch/cosmo_public/ekit/badges/master/coverage.svg
  		:target: https://cosmo-gitlab.phys.ethz.ch/cosmo_public/ekit

.. image:: https://cosmo-gitlab.phys.ethz.ch/cosmo_public/ekit/badges/master/pipeline.svg
        :target: https://cosmo-gitlab.phys.ethz.ch/cosmo_public/ekit

.. image:: http://img.shields.io/badge/arXiv-2006.12506-orange.svg?style=flat
        :target: https://arxiv.org/abs/2006.12506

.. image:: http://img.shields.io/badge/arXiv-2110.10135-orange.svg?style=flat
        :target: https://arxiv.org/abs/arXiv:2110.10135



ekit is a collection of small tools used by the Non-Gaussian Statistics Framework (`NGSF <https://cosmo-gitlab.phys.ethz.ch/cosmo_public/NGSF>`_).

If you use this package in your research please cite Zuercher et al. 2020 (`arXiv-2006.12506 <https://arxiv.org/abs/2006.12506>`_)
and Zuercher et al. 2021 (`arXiv-2110.10135 <https://arxiv.org/abs/2110.10135>`_).

`Source <https://cosmo-gitlab.phys.ethz.ch/cosmo_public/ekit>`_

`Documentation <http://cosmo-docs.phys.ethz.ch/ekit>`_

Introduction
============

It contains the following tools:

- paths:

    The paths module allows to pack meta data into paths and to retrieve it again from the paths.
    It diffferentiates between named (passed via a directory) and unnamed parameters (passed via a list).
    Note that your parameter names MUST NOT contain = or _ signs as these are used to parse the metadata from the path.

- context:

    The context module can be used to pass configuration parameters around. 
    You can specify which parameters are allowed and what data types they must have. 
    You can also specify default values for them.

- logger:

    The logger module allows to create convenient and nice looking logs for your python code. 

Getting Started
===============

The easiest and fastest way to learn about ekit is to have a look at the Tutorial section in the documentation.

Credits
=======

This package was created by Dominik Zuercher (PhD student at ETH Zurich in Alexandre Refregiers `Comsology Research Group <https://cosmology.ethz.ch/>`_)

The package is maintained by Dominik Zuercher dominik.zuercher@phys.ethz.ch.

Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.
