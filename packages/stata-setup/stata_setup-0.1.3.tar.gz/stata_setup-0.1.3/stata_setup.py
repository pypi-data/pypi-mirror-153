'''
*! version 0.1.3  11may2022

A module for configuring and initializing Stata within Python.

This code is under the 
`Apache License v2 <https://www.apache.org/licenses/LICENSE-2.0.txt>`_.
'''
from __future__ import absolute_import, print_function

__all__ = ["config"]
__version__ = '0.1.3'
__author__ = 'StataCorp LLC'

import os
import sys

def config(path, edition, splash=True):
    """
    Configure Stata within Python.

    Parameters
    ----------
    path : str
        Stata's installation path.
	
    edition : str
        The Stata edition to be used. It can be one of mp, se, or be.
        
    splash  : bool, optional 
        Suppress displaying the splash message after Stata is successfully 
        initialized. Default is True. When set to False, the splash will be 
        suppressed.

        *New in version 0.1.3*.
    """	
    if not os.path.isdir(path):
        raise OSError(path + ' is invalid')

    if not os.path.isdir(os.path.join(path, 'utilities')):
        raise OSError(path + " is not Stata's installation path")

    sys.path.append(os.path.join(path, 'utilities'))
    from pystata import config 
    config.init(edition, splash=splash)
