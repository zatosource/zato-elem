# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Originally part of Zato - open-source ESB, SOA, REST, APIs and cloud integrations in Python
# https://zato.io

from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys
from setuptools import setup, find_packages

version = '1.0'

LONG_DESCRIPTION = ''

def parse_requirements(requirements):
    with open(requirements) as f:
        return [line.strip('\n') for line in f if line.strip('\n') and not line.startswith('#')]

package_dir = b'src' if sys.version_info.major == 2 else 'src'

setup(
      name = 'zato-elem',
      version = version,

      author = 'Dariusz Suchojad',
      author_email = 'dsuch at zato.io',
      url = 'https://zato.io/docs',
      description = 'The most convenient Python library for JSON, XML and CSV',
      long_description = LONG_DESCRIPTION,
      platforms = ['OS Independent'],
      license = 'GNU Lesser General Public License v3 (LGPLv3)',

      package_dir = {'':package_dir},
      packages = find_packages('src'),

      namespace_packages = ['zato'],
      install_requires = parse_requirements(
          os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')),

      zip_safe = False,

      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'Topic :: Education :: Testing',
        'Topic :: Internet',
        'Topic :: Internet :: Proxy Servers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: Utilities',
        ],
)
