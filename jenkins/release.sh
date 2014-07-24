if [[ -z "${RELEASE_TYPE}" ]]
then 
  RELEASE_TYPE=patch
fi

python setup.py tag --${RELEASE_TYPE} register -r rocktaviouspypi sdist bdist_wheel upload -r rocktaviouspypi