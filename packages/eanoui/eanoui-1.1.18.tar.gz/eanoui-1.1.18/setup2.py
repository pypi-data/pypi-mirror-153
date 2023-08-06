# -*- coding: utf-8 -*-
import sys

from setuptools import setup
import eanoui

if sys.version_info < (3, 0):

    long_description = "\n".join([
        open('README.rst', 'r').read(),
    ])
else:
    long_description = "\n".join([
        open('README.rst', 'r', encoding='utf-8').read(),
    ])

setup(
    name='eanoui',
    version=eanoui.get_version(),
    packages=['eanoui'],
    zip_safe=False,
    include_package_data=True,
    url='https://www.eano.com',
    license='Apache License 2.0',
    author='Hongbin',
    long_description=long_description,
    author_email='hongbin@eano.com',
    description='django admin theme 后台模板 based on simpleui',
    install_requires=['django'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
