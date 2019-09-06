.. _installing:

Installing
==========

Installing with pip
----------------------------------

The Brightway2-aggregated package is hosted `on Pypi <https://pypi.org/project/bw2agg/>`_ and can be installed using pip:

.. code-block:: console

    pip install presamples

Installing with conda
------------------------------------

The Brightway2-aggregated package is hosted on a conda channel and can be installed using conda:

.. code-block:: console

    conda install --channel pascallesage bw2agg

Install from github
-----------------------------------

The latest version of the Brightway2-aggregated package is hosted on `Github <https://github.com/PascalLesage/bw2agg/>`__ and can be installed
using pip:



.. code-block:: console


    https://github.com/PascalLesage/brightway2-aggregated/archive/master.zip
    git clone https://github.com/PascalLesage/brightway2-aggregated.git
    cd presamples
    python setup.py install

.. note::
    On some systems you may need to use ``sudo python setup.py install`` to
    install presamples system-wide.


Brightway2 dependency
----------------------------------------

Brightway2-aggregated is an extension to the `Brightway2 framework <https://brightwaylca.org/>`_, and is therefore
dependent on that framework.
