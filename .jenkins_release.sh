#!/bin/bash
pip install setuptools==0.9.8
pip install pip==1.5.2
pip install wheel

python setup.py register sdist bdist_wheel upload