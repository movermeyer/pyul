import sys
from setuptools import setup
from subprocess import call
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop

class install(_install):
    def run(self):
        call(['pip install -r requirements.txt --find-links "./"'], shell=True)
        _install.run(self)
        
class develop(_develop):
    def run(self):
        call(['pip install -r dev-requirements.txt --find-links "./"'], shell=True)
        _develop.run(self)

kw = {}
if sys.version_info >= (3,):
    kw['use_2to3'] = True

setup(cmdclass={'install': install,
                'develop': develop},
      setup_requires=['pbr==0.11.0.dev19.gb0cedad'],
      pbr=True,
      **kw)