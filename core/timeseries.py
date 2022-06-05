from __future__ import annotations
import datetime as dt

from numpy import average

class timeseries:
    
    name:   str
    _data:  dict[dt.date, float] = {}

    def __init__(
        self, 
        name:   str, 
        data:   dict[dt.date, float] = None,
        ):
        self.name = name
        if not data is None:
            self._data = data

    def size(self):
        return len(self._data)

    def add(self, date: dt.date, value: float):
        self._data[date] = value
    
    def copy(self, new_name = None) -> timeseries:
        if new_name is None:
            new_name = self.name
        res = { k: v for (k,v) in self._data.items() }
        return timeseries(new_name, res)

    def keys(self):
        res = list(self._data.keys())
        res.sort()
        return res
    
    def first(self):
        first_date = self.keys()[0]
        return first_date, self._data[first_date] 
    
    def first_date(self)-> dt.date:
        return self.first[0]

    def first_value(self)-> float:
        return self.first[1]
    
    def last(self):
        last_date = self.keys()[-1]
        return last_date, self._data[last_date] 
    
    def last_date(self)-> dt.date:
        return self.last[0]

    def last_value(self)-> float:
        return self.last[1]

    def get(self, date: dt.date):
        return self._data.get(date, None)

    def sum(self):
        return sum([v for (k,v) in self._data.items()])

    def average(self):
        return average([v for (k,v) in self._data.items()])
    
    def __str__(self) -> str:
        res = self.name + ": "
        for x in self.keys():
            res += f"\n {x} -> {self._data[x]}"
        return res
