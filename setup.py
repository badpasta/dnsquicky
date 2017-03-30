#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

import sys
import os
import setuptools
from version import __VERSION__


def _setup():
    setuptools.setup(
        name='dnsquicky',
        version=__VERSION__,
        description='It is a simple dns script.',
        author='Jingyu Wang',
        author_email='badpasta@gmail.com',
        url='',
        install_requires=['tornado', 'momoko', 'dnspython', 'PyYaml'],
        packages=setuptools.find_packages("src"),
        package_dir={'': 'src'},
        include_package_data = True,
        entry_points={
            'console_scripts': [
                'dnsquicky-api=dnsquicky.application.cmd:start_api_server',
                'dnsquciky-web=dnsquicky.application.cmd:start_web_server',
                ]
            },
        classifiers=[
            'Development Status :: 4 - Beta Development Status',
            'Environment :: Console',
            'Topic :: Utilities',
        ],
    )

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'publish':
            os.system('make publish')
            sys.exit()
        elif sys.argv[1] == 'release':
            if len(sys.argv) < 3:
                type_ = 'patch'
            else:
                type_ = sys.argv[2]
            assert type_ in ('major', 'minor', 'patch')

            os.system('bumpversion --current-version {} {}'
                      .format(__VERSION__, type_))
            sys.exit()

    _setup()


if __name__ == '__main__':
    main()

