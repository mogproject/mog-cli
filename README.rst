=======
mog-cli
=======

Command Line Interface for Playing Shogi Games

.. image:: https://travis-ci.org/mogproject/mog-cli.svg?branch=master
   :target: https://travis-ci.org/mogproject/mog-cli
   :alt: Build Status

.. image:: https://coveralls.io/repos/mogproject/mog-cli/badge.png?branch=master
   :target: https://coveralls.io/r/mogproject/mog-cli?branch=master
   :alt: Coverage Status

.. image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
   :target: http://choosealicense.com/licenses/apache-2.0/
   :alt: License

.. image:: https://badge.waffle.io/mogproject/mog-cli.svg?label=ready&title=Ready
   :target: https://waffle.io/mogproject/mog-cli
   :alt: 'Stories in Ready'

------------
Dependencies
------------

* Python == 3.5
* Boost C++ Library >= 1.57.0
* clang >= 3.5
* libstdc++ >= 4.9

------------
Installation
------------

TBD


------------------
Running on Jupyter
------------------

::

    pip3 install jupyter
    jupyter notebook

-----------
Development
-----------

::

    make clean save_attack_tables
    
    # The file "src/cmogcore/attack/data/preset_data.hpp" will be created.
    # This process shortens compile time while development.
    
    make clean test_quick

