import os
import virtualenv

def get_venv_home():
    return os.environ.get('VENV_HOME') or os.path.join(os.path.expanduser('~'),'.virtualenvs')

def make_venv_home():
    venv_home = get_venv_home()
    os.makedirs(venv_home)
    
def get_env_home(name=None):
    return os.path.join(get_venv_home(), name)
    
def get_paths(name):
    _, lib_dir, inc_dir, bin_dir = virtualenv.path_locations(name)
    
    venv_home = get_venv_home()
    home_dir = get_env_home(name)
    lib_dir = os.path.join(venv_home, lib_dir)
    pkg_dir = os.path.join(lib_dir, 'site-packages')
    inc_dir = os.path.join(venv_home, inc_dir)
    bin_dir = os.path.join(venv_home, bin_dir)        
    
    return home_dir, lib_dir, pkg_dir, inc_dir, bin_dir

def get_activate_script(name):
    home_dir, lib_dir, pkg_dir, inc_dir, bin_dir = get_paths(name)
    return os.path.join(bin_dir, 'activate_this.py')

def exists( name, raise_error=False):
    home_dir = get_env_home(name)
    if not os.path.exists(home_dir):
        if raise_error:
            raise Exception('Unable to find virtualenv {0}'.format(home_dir))
        return False
    return True 
