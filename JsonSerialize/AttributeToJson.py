from collections import OrderedDict, namedtuple

__author__ = 'jurankirihara'
import numpy
import os.path
import simplejson as json
from collections import namedtuple, Iterable, OrderedDict
from past.builtins import long,basestring



class JsonSerialize:
    #filename is read only
    @property
    def _file_name(self):
        return self._file


    def __init__(self,filename,overwrite=False):
        #Never overwrite file unless overwrite option specified
        def rename(self,filename):
            ind=1
            temp=filename+'_'+str(ind)
            while os.path.isfile(temp):
                ind+=1
                temp=temp[-1:]+str(ind)
            filename=temp
        try:
            if os.path.isfile(filename) and not overwrite:
                rename(filename)
        except Exception as e:
            raise e
        self._file=filename+'.json'
    @staticmethod
    def isnamedtuple(obj):
            """Heuristic check if an object is a namedtuple."""
            return isinstance(obj, tuple) and hasattr(obj, "_fields") and hasattr(obj, "_asdict") and callable(obj._asdict)


    def serialize(self,data):

        if data is None or isinstance(data, (bool, int, long, float, basestring)):
            return data
        if isinstance(data, list):
            return [self.serialize(val) for val in data]
        if isinstance(data, OrderedDict):
            return {"py/collections.OrderedDict":
                    [[self.serialize(k), self.serialize(v)] for k, v in data.iteritems()]}
        if self.isnamedtuple(data):
            return {"py/collections.namedtuple": {
                "type":   type(data).__name__,
                "fields": list(data._fields),
                "values": [self.serialize(getattr(data, f)) for f in data._fields]}}
        if isinstance(data, dict):
            if all(isinstance(k, basestring) for k in data):
                return {k: self.serialize(v) for k, v in data.items()}
            return {"py/dict": [[self.serialize(k), self.serialize(v)] for k, v in data.iteritems()]}
        if isinstance(data, tuple):
            return {"py/tuple": [self.serialize(val) for val in data]}
        if isinstance(data, set):
            return {"py/set": [self.serialize(val) for val in data]}
        if isinstance(data, numpy.ndarray):
            return {"py/numpy.ndarray": {
                "values": data.tolist(),
                "dtype":  str(data.dtype)}}
        raise TypeError("Type %s not data-serializable" % type(data))

    def deserialize(self,dct):
        if not isinstance(dct,Iterable):
            return dct
        if "py/dict" in dct:
            return dict(dct["py/dict"])
        if "py/tuple" in dct:
            return tuple(dct["py/tuple"])
        if "py/set" in dct:
            return set(dct["py/set"])
        if "py/collections.namedtuple" in dct:
            data = dct["py/collections.namedtuple"]
            return namedtuple(data["type"], data["fields"])(*data["values"])
        if "py/numpy.ndarray" in dct:
            data = dct["py/numpy.ndarray"]
            return numpy.array(data["values"], dtype=data["dtype"])
        if "py/collections.OrderedDict" in dct:
            return OrderedDict(dct["py/collections.OrderedDict"])
        return dct

    def data_to_json(self,data):
        print('Serializing data to json'+self._file)
        d = data.__dict__
        for k, v in d.items():
            d[k] = self.serialize(v)
        d['className']=str(data.__class__)
        print(d['className'])
        with open(self._file,'w') as f:
            json.dump(d, f)
        print('Serialized file')
    def json_to_data(self,class_init):

        attr = json.load(open(self._file))

        for k, v in attr.items():
            if k == 'className':

                if not str(type(class_init)) == str(attr[k]):
                    print(str(type(class_init)), str(attr[k]))
                    raise AttributeError("Specified class name does not match the JSON class. Specified class name is "+str(type(class_init))+" JSON class name is "+attr[k])
            else:
                setattr(class_init, k, self.deserialize(v))
        return class_init

    '''
    def serialize(self,attr):
        #does not save in memory the trained model attributes
        if attr is None:
            raise Exception("Cannot save empty model data")
        if not type(attr) is dict:
            raise Exception("Expected input to be of type Dict")
        print('Parsing to Json...')
        try:
            for k, v in attr.items():
                if type(v) is numpy.ndarray and k[-1] == '_':
                    attr[k] = v.tolist()
        except Exception as e:
            raise e
        print('Parsing completed, file '+self._file+'.json'+' created')
        json.dump(attr, open('./'+self._file+'.json', 'w'))
    #returns a variable with specified class type

    def load(self,ret):
        print(type(ret))
        attr=json.load(open(self._file+'.json'))
        for k, v in attr.items():
            if isinstance(v, list):
                setattr(ret, k, numpy.array(v))
            else:
                setattr(ret, k, v)

    '''