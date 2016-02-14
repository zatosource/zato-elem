# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Part of Zato - Open-source ESB, SOA, REST, APIs and Cloud Integrations in Python
# https://zato.io

# stdlib
from uuid import uuid4

def rand_string(count=1):
    if count == 1:
        return 'a' + uuid4().hex
    else:
        return ['a' + uuid4().hex for x in range(count)]
