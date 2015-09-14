#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# As 2015-09-14 get the exec is OK, running it fails, no clue


from distutils.core import setup
import py2exe

#setup(console=['aggregator.py'])

setup( options = {"py2exe": {"compressed": 1, "optimize": 0, "bundle_files": 1, } }, zipfile = None, console=['aggregator.py'] )
