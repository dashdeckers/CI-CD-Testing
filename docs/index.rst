The CI/CD Testground
====================

.. toctree::
    :hidden:
    :maxdepth: 1

    license
    reference


This is a testing ground for
trying out and practicing
linting, documentation generation,
testing, type checking,
CI/CD workflows,
best practices,
project management,
and anything else along those lines.


Installation
------------

This project is currently not deployed to PyPI.
So, you will need to clone the GitHub repo by
running this command in your terminal:

.. code-block:: console

   $ git clone https://github.com/dashdeckers/CI-CD-Testing


Usage
-----

You can create a gif showing how
the plot of a logistic map:
:math:`x_{n+1} = r * x_n * (1 - x_n)`
changes for varying values of r. 
Currently they range between 0 and 4.5,
but command line arguments
will be implemented shortly.
To run the code,
execute the following in your terminal
(make sure you use python3.x):

.. code-block:: console

   $ python src/chaos/main.py

You can then view the file src/logistic_map.gif


Logging
-------

You can view the detailed log-tree by running

.. code-block:: console

    $ eliot-tree logfile.log

