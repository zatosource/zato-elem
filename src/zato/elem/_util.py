# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>
Licensed under LGPLv3, see LICENSE.txt for terms and conditions.

Part of Zato - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python
https://zato.io
"""

# Bunch
from bunch import Bunch

# six
from six import iteritems

def bunchify(x): # pragma: no cover
    """ Python 2 and 3-safe bunchify version of bunch.bunchify.
    """
    if isinstance(x, dict):
        return Bunch((k, bunchify(v)) for k, v in iteritems(x))
    elif isinstance(x, (list, tuple)):
        return type(x)(bunchify(v) for v in x)
    else:
        return x
