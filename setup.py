#-*- coding: utf-8 -*-

"""
    dungeons
    ~~~~~~~~

    Setup
    `````

    $ pip install -e .
"""

from distutils.core import setup

setup(
    name='dungeons',
    version='0.0.2',
    url='http://github.com/mekarpeles/dungeons',
    author='mek',
    author_email='michael.karpeles@gmail.com',
    packages=[
        'dungeon',
        'test',
        ],
    platforms='any',
    license='LICENSE',
    install_requires=[
        'twisted >= 11.1.0',
        'telnetlib',
    ],
    description="Dungeons MUD.",
    long_description=open('README.md').read(),
)
