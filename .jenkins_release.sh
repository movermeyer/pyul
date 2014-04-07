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

python setup.py sdist bdist_wheel upload -r mmfpypi
# Confirm that it worked
if (( $? )); then
    #Try register and then upload
    python setup.py sdist bdist_wheel register upload -r mmfpypi
    if (( $? )); then
        echo "Unable to distribute your release!" >&2
        exit 1
    fi
fi