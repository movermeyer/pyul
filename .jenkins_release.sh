#!/bin/bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv shell
pyenv virtualenv pyul_release#${BUILD_NUMBER}-${PYENV_VERSION} -f
pyenv activate "pyul_release#${BUILD_NUMBER}-${PYENV_VERSION}"

pip install --index-url http://pypi.mapmyfitness.com/mmf/stable/+simple/ setuptools==0.9.8
pip install --index-url http://pypi.mapmyfitness.com/mmf/stable/+simple/ pip==1.5.2
pip install wheel

# I cannot find anything wrong with calling register for each upload
python setup.py register sdist bdist_wheel upload -r mmfpypi