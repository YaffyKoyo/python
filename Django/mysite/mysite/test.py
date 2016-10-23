
import time

_values = {}
_time_stamps = {}

class MCClone():
    def __init__(self, name, params):
        self._value = _values.setdefault(name,{})
        self._time_stamp = _time_stamps.setdefault(name,{})
    
    def set(self,key,value,DefaultTimeOut = 10):
        self._value[key] = value
        self._time_stamp[key] = time.time()+DefaultTimeOut
    
    def get(self,key):
        if self.key_active(key):
            try:
                return self._value[key]
            except ValueError:
                return None
    
    def _get_time(self,key):
        '''
        this one is just for debug
        will not be used for real project
        '''
        try:
            return self._time_stamp[key]
        except ValueError:
            return default

    def key_active(self, key):
        if not self._has_expired(key):
            return True
        
        try:
            del self._value[key]
            del self._time_stamp[key]
        except KeyError:
            pass
        return False

    def _has_expired(self, key):
        exp = self._time_stamp.get(key,-1)
        if exp is None or exp > time.time():
            return False
        return True

    def __contains__(self, key):
        """
        contains make sure it will expired automatically.
        need to investigate more on this part.
        """
        return self.key_active(key)