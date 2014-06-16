#!/bin/bash
python setup.py register -r mmfpypi sdist bdist_wheel upload -r mmfpypi
python setup.py register -r rocktavious_pypi sdist upload -r rocktavious_pypi