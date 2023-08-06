Installation
============

This guide describes how to install *midas* on :ref:`linux`,
:ref:`os-x`, and :ref:`windows`. 

.. _linux:

Linux
-----

This guide is based on *Arch Linux 5.13, 64bit*, but this should for work for
other distributions as well.

The *midas* package requires `Python`__ >= 3.8. We recommend to use a
`virtualenv`__ to avoid messing up your system environment. Use your
distributions' package manager to install pip and virtualenv. Make sure which
python version is linked to the `python` command (in some distros this is 
python2). To be sure, specify the python interpreter when creating the env:

.. code-block:: bash

    $ virtualenv -p /usr/bin/python3 ~/.virtualenvs/midas
    $ source ~/.virtualenv/midas/bin/activate

Now you can install *midas-mosaik* from the pypi package repository

.. code-block:: bash

    (midas) $ pip install midas-mosaik
    
or from the source code.

.. code-block:: bash

    (midas) $ pip install git+https://gitlab.com/midas-mosaik/midas.git

Finally, you can test your installation by typing:

.. code-block:: bash

    (midas) $ midasctl --help 

into the console, which should print information about the command line 
tool of *midas*.

__ https://www.python.org/
__ https://virtualenv.readthedocs.org

.. _os-x:

OS-X
----

10.15 Catalina
(Coming soon)

.. _windows:

Windows
-------

There are several ways to install MIDAS on Windows. If you're using conda or
pycharm, you probably know how to install packages into your system. For that
reason, this guide targets a system without Python installed (you can, of
course, join the guide at any point).

Install python
##############

First, you need to download and install Python on your System. Visit 
https://www.python.org/downloads/release/python-397/ to select and download
the latest version of python. Make sure to use the 64bit version (unless your
system is 32bit only).

Once the installer is downloaded, double-click to start the setup. During the
installation, make sure to mark the options "Add Python to PATH" and "Install
for all users". As soon as the installation finishes, it may be required to
log out and log in from your system or (to be safe) restart the whole system.
You can test your installation via Powershell (Win+S, then type "Powershell",
and execute as administrator). Once the Powershell opens, type:

.. code-block:: bash

    PS > python --version

If your installation was successful, the command prints out the installed
version of Python (e.g.: "Python 3.9.7")

To use virtualenvs inside of Powershell, you need to allow the execution of
scripts. This can be achieved by typing the following command into the 
Powershell (still requires an administrator shell).

.. code-block:: bash

    PS > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned

Afterwards, you should install virtualenv with

.. code-block:: bash

    PS > python -m pip install virtualenv

Afterwards, you should close your administrator Powershell and open a normal
Powershell. Create and activate the virtualenv (but it may be helpful to first
install the C++ compiler in the next step).

.. code-block:: bash
    
    PS > python -m virtualenv PATH\\TO\\.virtualenvs\\midas
    PS > PATH\\TO\\.virtualenvs\\midas\\Scripts\\activate.ps1

Install C++-Compiler
####################

Unfortunately, some packages need to be compiled from source and, since
Windows has no C++ compiler shipped per default, a compiler needs to be
installed. The easiest way to to so is to download and install the latest
Visual Studio Community edition from 
https://docs.microsoft.com/de-de/visualstudio/releases/2019/release-notes.

Alternatively, you can try to use pre-compiled binaries, which can be found
https://www.lfd.uci.edu/~gohlke/pythonlibs/. Make sure to select the
appropriate package version. Some packages you may need (Python 3.9, 64bit):

    * numpy‑1.20.3+mkl‑cp39‑cp39‑win_amd64.whl
    * numexpr‑2.7.3‑cp39‑cp39‑win_amd64.whl
    * llvmlite‑0.37.0‑cp39‑cp39‑win_amd64.whl
    * numba‑0.54.0‑cp39‑cp39‑win_amd64.whl
    * tables‑3.6.1‑cp39‑cp39‑win_amd64.whl

They can be install with pip, e.g.:

.. code-block:: bash

    (midas) PS > pip install numpy-1.20.3+mkl-cp39-cp39-win_amd64.whl

However, on my test machine, I had no luck using this method. 

Install the packages
####################

With the C++ compiler installed, you should be able to install *midas-mosaik*
directly from pypi:

.. code-block:: bash
    
    (midas) PS > pip install midas-mosaik

Finally, to test your installation, type

.. code-block:: bash

    (midas) PS > midasctl --help

You should see information about the *midasctl* command.
