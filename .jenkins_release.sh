#!/bin/bash
# pip install the versions of setuptools pip and wheel we need to release the package
pip install --index-url http://pypi.mapmyfitness.com/mmf/stable/+simple/ setuptools==0.9.8
pip install --index-url http://pypi.mapmyfitness.com/mmf/stable/+simple/ pip==1.5.2
pip install wheel

# I cannot find anything wrong with calling register for each upload
python setup.py register -r mmfpypi sdist bdist_wheel upload -r mmfpypi