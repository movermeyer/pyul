__all__ = ['DotifyDict']

#------------------------------------------------------------
#------------------------------------------------------------
class DotifyDict(dict):
    def __init__(self, data):
        for k, v in data.items():
            k = str(k)
            try:
                setattr(self, k, DotifyDict(v))
            except:
                setattr(self, k, v)
    
    def __repr__(self):
        return super(DotifyDict, self).__repr__()
    
    def __setitem__(self, key, value):
        if '.' in key:
            myKey, restOfKey = key.split('.', 1)
            target = self.set_default(myKey, DotifyDict())
            if not isinstance(target, DotifyDict):
                raise KeyError, 'cannot set "{0}" in "{1}" ({2})'.format(restOfKey, myKey, repr(target))
            target[restOfKey] = value
        else:
            if isinstance(value, dict) and not isinstance(value, DotifyDict):
                value = DotifyDict(value)
            super(DotifyDict, self).__setitem__(key, value)
    
    def __getitem__(self, key):
        if '.' not in key:
            return super(DotifyDict, self).__getitem__(key)
        myKey, restOfKey = key.split('.', 1)
        target = super(DotifyDict, self).__getitem__(myKey)
        if not isinstance(target, DotifyDict):
            raise KeyError, 'cannot get "{0}" in "{1}" ({2})'.format(restOfKey, myKey, repr(target))
        return target[restOfKey]
    
    def __contains__(self, key):
        if '.' not in key:
            return super(DotifyDict, self).__contains__(key)
        myKey, restOfKey = key.split('.', 1)
        target = super(DotifyDict, self).__getitem__(myKey)
        if not isinstance(target, DotifyDict):
            return False
        return restOfKey in target
    
    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default
    
    def set_default(self, key, default):
        if key not in self:
            self[key] = default
        return self[key]
    
    __setattr__ = __setitem__
    __getattr__ = __getitem__