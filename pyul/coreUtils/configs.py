import yaml
import json
import pprint
from pyul import coreUtils, xmlUtils
from pyul.support import Path

__all__ = ['Config','YAMLConfig','JSONConfig','XMLConfig']   

class Config(coreUtils.ComparableMixin, coreUtils.DotifyDict):
    """
    A utility class for representing a format as a dictionary of nested data.
    """

    def __init__(self, filepath):
        filepath = Path(filepath)
        if filepath.is_dir():
            filepath = coreUtils.getUserTempDir().joinpath('temp.dat')
        coreUtils.synthesize(self, 'filepath', filepath)
        self.read()
        
    def _cmpkey(self):
        return tuple(self._get_data().values())
        
    def _ignore_keys(self):
        return ['_filepath']
    
    def _get_data(self, data=None):
        if data is None:
            data = self
        output = {}
        ignore_keys = self._ignore_keys()
        for k, v in [(k,v) for k,v in data.items() if k not in ignore_keys]:
            if isinstance(v, coreUtils.DotifyDict):
                output[k] = self._get_data(v)
            else:
                output[k] = v
        return output
                
    def load(self, data):
        parsed_data = self.parse(data)
        for k, v in parsed_data.items():
            try:
                setattr(self, k, coreUtils.DotifyDict(v))
            except:
                setattr(self, k, v)
        
    def read(self):
        if not self._filepath.exists():
            return
        with open(str(self._filepath)) as fh:
            data = fh.read()
        self.load(data)
        
    def write(self):
        '''Writes the dict data to the file'''
        with open(str(self._filepath),'wb') as fh :
            fh.write(self.unparse(self._get_data()))
    
    def pprint(self):
        pprint.pprint(self._get_data())
    
    def parse(self, data):
        raise NotImplementedError
    
    def unparse(self, data):
        raise NotImplementedError
    


class YAMLConfig(Config):
    """
    Class for representing yaml data as a nested dictionary
    """
    def parse(self, data):
        return yaml.load(data)
    
    def unparse(self, data):
        return yaml.dump(data, default_flow_style=False)
    
class JSONConfig(Config):
    """
    Class for representing json data as a nested dictionary
    """
    def parse(self, data):
        return json.loads(data)
    
    def unparse(self, data):
        return json.dumps(data,
                          sort_keys=True,
                          indent=4)
    
class XMLConfig(Config):
    """
    Class for representing xml data as a nested dictionary
    """
    def parse(self, data):
        return xmlUtils.parseToDict(data)
    
    def unparse(self, data):
        return xmlUtils.unparseFromDict(data)
            


if __name__ == '__main__':    
    yaml_config = YAMLConfig('/Users/kyle.rockman/data.yaml')
    json_config = JSONConfig('/Users/kyle.rockman/data.json')
    xml_config = XMLConfig('/Users/kyle.rockman/data.xml')
    
    yaml_config.pprint()
    json_config.pprint()
    xml_config.pprint()
    
    
    yaml_config.write()
    json_config.write()
    xml_config.write()