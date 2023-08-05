.. _installation:

Installation
############

Debian
======
A `Debian package <https://packages.debian.org/unstable/lavacli>`_ is available
for Debian unstable and could be installed with:

.. code-block:: shell

    apt install lavacli

PyPi
====

lavacli is also available on `Pypi <https://pypi.org/project/lavacli/>`_ and can be installed with:

.. code-block:: shell

    pip install lavacli

Development versions
=====================

It's also possible to use lavacli directly from the sources:

.. code-block:: shell

    git clone https://git.lavasoftware.org/lava/lavacli.git
    cd lavacli
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt
    python3 -m lavacli
