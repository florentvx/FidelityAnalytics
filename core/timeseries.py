from __future__ import annotations
import datetime as dt

from numpy import average

class timeseries:
    
    name:   str
    _data:  dict[dt.date, float] = {}

    def __init__(self, name):
        self.name = name

    @property
    def size(self):
        return len(self._data)

    def add(self, date: dt.date, value: float):
        self._data[date] = value
    
    def keys(self):
        res = list(self._data.keys())
        res.sort()
        return res
    
    @property
    def first(self):
        first_date = self.keys()[0]
        return first_date, self._data[first_date] 
    
    @property
    def first_date(self)-> dt.date:
        return self.first[0]

    @property
    def first_value(self)-> float:
        return self.first[1]

    @property
    def last(self):
        last_date = self.keys()[-1]
        return last_date, self._data[last_date] 
    
    @property
    def last_date(self)-> dt.date:
        return self.last[0]

    @property
    def last_value(self)-> float:
        return self.last[1]

    def get(self, date: dt.date):
        return self._data.get(date, None)

    def average(self):
        return average([v for (k,v) in self._data.items()])
    
