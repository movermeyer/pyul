#!/bin/bash
venv_name=.virtualenv
virtualenv_activate=./${venv_name}/bin/activate

# Validate the virtualenv and activate it
if [[ ! -e $virtualenv_activate ]]
then
  virtualenv $venv_name
fi
. ${virtualenv_activate}

pip install pbr==0.11.0.dev19.gb0cedad --find-links "./"
pip install -r dev-requirements.txt --find-links "./"
if [[ -e "./setup.py" ]]
then
    python setup.py develop
fi
