#!/bin/bash
venv_name=.virtualenv
virtualenv_activate=./${venv_name}/bin/activate

# Check to see if virtualenv is installed
if ! venv_cmd="$(type -p "virtualenv")" || [ -z "$venv_cmd" ]
then
  echo "Unable to find virtualenv command"
  exit
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
