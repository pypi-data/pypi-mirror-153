#!/usr/bin/env python3
# Copyright © 2022 Mark Summerfield. All rights reserved.
# License: GPLv3

'''
This module provides the editabletuple() function for creating classes
with a fixed sequence of fields, similar to a namedtuple, except editable.

Each instance of a class created by the editabletuple function's fields can
be accessed by index et[i] or by fieldname et.name.

Example #1: no defaults; no validator

>>> Options = editabletuple('Options', 'maxcolors shape zoom restore')
>>> options = Options(5, 'square', 0.9, True)
>>> options
Options(maxcolors=5, shape='square', zoom=0.9, restore=True)
>>> options.maxcolors = 7
>>> options[-1] = False
>>> options[2] -= 0.1
>>> options
Options(maxcolors=7, shape='square', zoom=0.8, restore=False)

Example #2: with defaults but no validator

>>> Rgb = editabletuple('Rgb', 'red green blue', defaults=(0, 0, 0))
>>> black = Rgb()
>>> black
Rgb(red=0, green=0, blue=0)
>>> navy = Rgb(blue=128)
>>> navy
Rgb(red=0, green=0, blue=128)
>>> violet = Rgb(238, 130, 238)
>>> violet
Rgb(red=238, green=130, blue=238)

Example #3: with defaults and a validator

>>> def validate_rgba(self, index, value):
...     if index == 3: # alpha channel
...         if not (0.0 <= value <= 1.0):
...             self[index] = 1.0 # silently default to opaque
...     elif not (0 <= value <= 255):
...         raise ValueError(f'color value must be 0-255, got {value}')
>>>
>>> Rgba = editabletuple('Rgba', 'red', 'green', 'blue', 'alpha',
...                      defaults=(0, 0, 0, 1.0), validator=validate_rgba)
>>> black = Rgba()
>>> black
Rgba(red=0, green=0, blue=0, alpha=1.0)
>>> seminavy = Rgba(blue=128, alpha=0.5)
>>> seminavy
Rgba(red=0, green=0, blue=128, alpha=0.5)
>>> violet = Rgba(238, 130, 238, alpha=2.5) # alpha too big
>>> violet
Rgba(red=238, green=130, blue=238, alpha=1.0)
>>>
>>> color = Rgba(green=99)
>>> color
Rgba(red=0, green=99, blue=0, alpha=1.0)
>>> assert color.green == 99
>>> color.red = 128
>>> assert color[2] == 0
>>> color[2] = 240
>>> assert color[2] == 240
>>> color[-1] = 0.5
>>> color
Rgba(red=128, green=99, blue=240, alpha=0.5)
>>> color[1] = 299
Traceback (most recent call last):
    ...
ValueError: color value must be 0-255, got 299
>>> color.blue = -65
Traceback (most recent call last):
    ...
ValueError: color value must be 0-255, got -65
>>> color = Rgba(green=99, blue=256)
Traceback (most recent call last):
    ...
ValueError: color value must be 0-255, got 256
>>> color = Rgba(100, 200, 300)
Traceback (most recent call last):
    ...
ValueError: color value must be 0-255, got 300

Curiously, on Python 3.8.10 and 3.10.4 on 64-bit Linux I get these results:

    import sys
    from collections import namedtuple
    from editabletuple import editabletuple

    t = (1, 2, 3)
    N = namedtuple('N', 'x y z')
    n = N(1, 2, 3)
    E = editabletuple('E', 'x', 'y', 'z')
    e = E(1, 2, 3)

    for x in (t, n, e):
        print(sys.getsizeof(x), x, type(x))
    # output:
    #   64 (1, 2, 3) <class 'tuple'>
    #   64 N(x=1, y=2, z=3) <class '__main__.N'>
    #   56 E(x=1, y=2, z=3) <class 'editabletuple.E'>

Note that dataclasses aren't indexable or iterable, so aren't comparable
with tuples, namedtuples, or editabletuples.
'''

__version__ = '1.0.1'


def editabletuple(classname, *fieldnames, defaults=None, validator=None):
    '''Returns a Class with the given classname and fieldnames whose
    attributes can be accessed by index or fieldname.

    classname is the name of the class to create: this should also be the
    name the returned class is bound to, e.g.,
    Point = editabletuple('Point', 'x y').

    fieldnames may be one or more fieldnames, e.g., 'x', 'y', 'z', or a
    single str of space-separated fieldnames, e.g., 'x y z'.

    defaults is an optional sequence of default values; if not given or if
    fewer than the number of fields, None is used as the default.

    validator is an optional function that is passed the editabletuple, an
    attribute index and an attribute value. whenever an attempt is made to
    set a value, e.g., by et[i] = value or et.fieldname = value. It should
    check the value and either leave it if valid, or change it to an
    acceptable alternative, or raise a ValueError.

    See the module docstring for examples.
    '''

    def init(self, *args, **kwargs):
        fields = self.__class__.__slots__
        if len(args) + len(kwargs) > len(fields):
            raise TypeError(f'{self.__class__.__name__} accepts up to '
                            f'{len(fields)} args; got {len(args)}')
        for index, name in enumerate(fields):
            default = (self._defaults[index] if self._defaults is not None
                       and index < len(self._defaults) else None)
            value = args[index] if index < len(args) else default
            setattr(self, name, value)
        names = set(fields)
        for name, value in kwargs.items():
            if name not in names:
                raise TypeError(f'{self.__class__.__name__} does not have '
                                f' a {name} field')
            setattr(self, name, value)
        if self._validator is not None: # must be done after all fields set
            for index in range(len(fields)):
                self._validator(index, getattr(self, fields[index]))

    def repr(self):
        pairs = []
        for name in self.__class__.__slots__:
            pairs.append((name, getattr(self, name)))
        kwargs = ', '.join(f'{name}={value!r}' for name, value in pairs)
        return f'{self.__class__.__name__}({kwargs})'

    def getitem(self, index):
        index = self._sanitize_index(index)
        return getattr(self, self.__class__.__slots__[index])

    def setitem(self, index, value):
        index = self._sanitize_index(index)
        if self._validator is not None:
            self._validator(index, value) # might raise ValueError
        setattr(self, self.__class__.__slots__[index], value)

    def setattr(self, name, value):
        if self._validator is not None:
            index = self.__class__.__slots__.index(name)
            self._validator(index, value) # might raise ValueError
        object.__setattr__(self, name, value)

    def _sanitize_index(self, index):
        if isinstance(index, slice):
            if index.stop is not None or index.step is not None:
                raise IndexError(f'{self.__class__.__name__}: cannot '
                                 f'use slices {index}')
            index = index.start
        length = len(self.__class__.__slots__)
        if index < 0:
            index += length
        if index >= length:
            raise IndexError(f'{self.__class__.__name__}: index {index} '
                             'out of range')
        return index

    def asdict(self):
        return {name: value for name, value in zip(self.__slots__, self)}

    def length(self):
        return len(self.__class__.__slots__)

    def iter(self): # implicitly supports tuple(obj) and list(obj)
        fields = self.__class__.__slots__
        for i in range(len(fields)):
            yield getattr(self, fields[i])

    def eq(self, other):
        if self.__class__.__name__ != other.__class__.__name__:
            return False
        return tuple(self) == tuple(other)

    def lt(self, other):
        if self.__class__.__name__ != other.__class__.__name__:
            return False
        return tuple(self) < tuple(other)

    if len(fieldnames) == 1 and isinstance(fieldnames[0], str):
        fieldnames = fieldnames[0].split()
    return type(classname, (), dict(__init__=init, __repr__=repr,
                _sanitize_index=_sanitize_index, __getitem__=getitem,
                __setitem__=setitem, __setattr__=setattr,
                asdict=property(asdict), _defaults=defaults,
                _validator=validator, __len__=length, __iter__=iter,
                __eq__=eq, __lt__=lt, __slots__=fieldnames))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
