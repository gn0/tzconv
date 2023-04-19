#!/usr/bin/env python
# coding: utf8

from setuptools import setup

setup(
    name='tzconv',
    version='1.0',
    description=u'command-line tool to convert a date and time to several time zones at once',
    author=u'Gabor Nyeki',
    url='https://www.gabornyeki.com/',
    packages=['tzconv'],
    install_requires=['click'],
    provides=['tzconv (1.0)'],
    entry_points={
        'console_scripts': [
            'tzconv = tzconv:main',
        ],
    }
    )
