from __future__ import annotations
import datetime as dt

from numpy import average

class timeseries:
    
    name:   str
    _data:  dict[dt.date, float]

    def __init__(
        self, 
        name:   str, 
        _data:   dict[dt.date, float] = None,
        ):
        self.name = name
        self._data = {}
        if not _data is None:
            self._data = _data.copy()

    @property
    def size(self):
        return len(self._data)

    def add(self, date: dt.date, value: float):
        self._data[date] = value
    
    def copy(self, new_name = None) -> timeseries:
        if new_name is None:
            new_name = self.name
        return timeseries(new_name, self._data)

    def keys(self):
        res = list(self._data.keys())
        res.sort()
        return res
    
    def values(self):
        return [self.get(d) for d in self.keys()]

    def first(self):
        first_date = self.keys()[0]
        return first_date, self._data[first_date] 
    
    def first_date(self)-> dt.date:
        return self.first[0]

    def first_value(self)-> float:
        return self.first[1]
    
    def _last(self):
        last_date = self.keys()[-1]
        return last_date, self._data[last_date] 
    
    def get_last_date(self)-> dt.date:
        return self._last()[0]

    def get_last_value(self)-> float:
        return self._last()[1]

    def get(self, date: dt.date):
        return self._data.get(date, None)

    def get_closest(self, date: dt.date, is_before: bool = True):
        res = self.get(date)
        if not res is None:
            return res
        if is_before:
            return [self._data[k] for k in self._data.keys() if k < date][-1]
        else:
            return [self._data[k] for k in self._data.keys() if k > date][0]

    def _to_list(self) -> list:
        return [v for (k,v) in self._data.items()]

    def sum(self) -> float:
        return sum(self._to_list())

    def average(self):
        if self.size == 0:
            return 0
        return average(self._to_list())

    def copy_paste(self, ts: timeseries) -> None:
        for k in ts._data.keys():
            if k in self._data.keys():
                raise ValueError("key already used") 
            self.add(k, ts._data[k])
        return
    
    def __str__(self) -> str:
        res = self.name + ": "
        for x in self.keys():
            res += f"\n {x} -> {self._data[x]}"
        return res

def adjust_timeseries_by_coverage(
    ts: timeseries,
    override_name: str = None
    ) -> timeseries:
    
    new_name = ts.name + ""
    if not override_name is None:
        new_name = override_name
    
    new_ts = {}
    if ts.size > 0:
        keys = ts.keys()
        if ts.size == 1:
            new_ts[ts.get_last_date()] = ts.get_last_value() * 4.0
        else:
            last_coverage = 0
            for i in range(0, len(keys) - 1):
                last_coverage = (keys[i+1]-keys[i]).days / 365.0
                new_ts[keys[i]] = ts.get(keys[i]) / last_coverage
            new_ts[ts.get_last_date()] = ts.get_last_value() / last_coverage
    
    return timeseries(new_name, new_ts)

