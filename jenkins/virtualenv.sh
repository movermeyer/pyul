#!/bin/bash
venv_name=.virtualenv
virtualenv_activate=./${venv_name}/bin/activate

# Make sure we have the standard modules for working with packaging and virtualenvs
if ! venv_cmd="$(type -p "pip")" || [ -z "$venv_cmd" ]
then
  curl --silent --show-error --retry 5 https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python
fi

# Only try to install virtualenv if it isn't already installed
if ! venv_cmd="$(type -p "virtualenv")" || [ -z "$venv_cmd" ]
then
  pip install --upgrade virtualenv
fi

# Validate the virtualenv and activate it
if [[ ! -e $virtualenv_activate ]]
then
  virtualenv $venv_name
fi
. ${virtualenv_activate}

if [[ "$1" == "install" ]]
then
  pip install -r requirements.txt
  pip install --upgrade pyul
else
  pip install --upgrade -r dev-requirements.txt
  python setup.py develop
fi
