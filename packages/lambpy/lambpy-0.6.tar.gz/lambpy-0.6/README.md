lambpy
======

lambpy is a simple script to build lambda compatible zip file.

Features
========

lambpy is able to:

* create a zip file with python modules
* install using requirements.txt file
* the resulting zip archive is reproducible

Using lambpy
============

Installing
----------

lambpy is available via pypi:

    python3 -m pip install lambpy

Usage
-----

To create a new zip archive, list the modules to include and the requirements:

    lambpy -r requirements.txt -i mymodule/

To pass pipfile location:
    lambpy -p ./ -i mymodule/

The zip archive will be called `lambda.zip`
