# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
import requests,warnings


import jdw.data.DataAPI.mg as MGAPI
import jdw.mfc.experimental.DataAPI.mg as ExperimentalAPI
try:
    import jdw.mfc.anode as AnodeAPI
except ImportError:
    warnings.warn("the environment cannot be traded")


from jdw.mfc.neutron.factory import Factory


from .version import __version__

try:
    unicode
except:
    unicode = str
    
session = requests.Session()


NeutronAPI = Factory()