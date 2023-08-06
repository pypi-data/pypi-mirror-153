# coding: utf-8
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup

import sys
if sys.version_info < (3, 7):
    sys.exit('Python 3.7 or greater is required.')
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# 版本号，自己随便写
VERSION = "0.0.1"

LICENSE = "GPLv3"

setup(
    name='nonebot_plugin_tweetPusher',
    version=VERSION,
    keywords=["nonebot"],
    description=(
        'a tweet pusher plugin for nonebot2'
    ),
    author='Kizureina',
    author_email='houchangkun@gmail.com',
    maintainer='Kizureina',
    maintainer_email='houchangkun@gmail.com',
    license=LICENSE,
    platforms=["all"],
    url='https://github.com/Kizureina/nonebot_plugin_ytbLivePusher',
    python_requires=">=3.7",
    install_requires=["requests", "nonebot", "nonebot2", "jsonlines", "twint"],
    classifiers=[
            "Operating System :: OS Independent",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: Implementation :: CPython"
    ],
)
