#!/bin/bash
venv_name=.virtualenv
virtualenv_activate=./${venv_name}/bin/activate

# Check to see if pip and virtualenv is installed
command -v pip >/dev/null 2>&1 || { echo >&2 "Unable to find pip.  Aborting."; exit 1; }
command -v virtualenv >/dev/null 2>&1 || { echo >&2 "Unable to find virtualenv.  Aborting."; exit 1; }

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
