#!/bin/bash

#Setup PYENV
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv shell
pyenv virtualenv pyul#${BUILD_NUMBER}-${PYENV_VERSION} -f
pyenv activate "pyul#${BUILD_NUMBER}-${PYENV_VERSION}"

#pip install to virtual env
pip install -r requirements.txt
pip install -r test_requirements.txt

#run tests with setup.cfg controlling options to nose
python setup.py nosetests