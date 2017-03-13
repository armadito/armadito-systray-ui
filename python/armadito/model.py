# Copyright (C) 2016-2017 Teclib'

# This file is part of Armadito indicator.

# Armadito indicator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Armadito indicator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Armadito indicator.  If not, see <http://www.gnu.org/licenses/>.

from functools import wraps

def notify(f):
    @wraps(f)
    def decorator(self, *args, **kwargs):
        retval = f(self, *args, **kwargs)
        self.notify(f)
        return retval
    return decorator

class Notifier(object):
    def __init__(self):
        self._listeners = {}

    def on(self, mth, fun):
        self._listeners[mth.__name__] = fun

    def notify(self, mth):
        try:
            fun = self._listeners[mth.__name__]
        except KeyError:
            pass
        fun()

class AVModel(Notifier):
    def __init__(self):
        super().__init__(self)

    @notify
    def info(self, x):
        self._a += x
        return self._a


if __name__ == '__main__':
    class TestModel(Notifier):
        def __init__(self):
            super().__init__()
            self._count = 0

        @notify
        def inc(self, x):
            self._count += x

        @property
        def count(self):
            return self._count

    a1 = TestModel()
    a1.on(a1.inc, lambda : print('lambda', a1.count))
    a1.inc(2)
    a1.inc(3)

