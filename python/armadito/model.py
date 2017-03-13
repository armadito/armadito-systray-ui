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

def notify_before(f):
    @wraps(f)
    def decorator(self, *args, **kwargs):
        self.notify(self, f.__name__, *args, *kwargs)
        retval = f(self, *args, **kwargs)
        return retval
    return decorator

def notify_after(f):
    @wraps(f)
    def decorator(self, *args, **kwargs):
        retval = f(self, *args, **kwargs)
        self.notify(self, f.__name__, retval)
        return retval
    return decorator

class Notifier(object):
    def __init__(self):
        self._listener = None

    def listener(self, l):
        self._listener = l

    def notify(self, method_name, *args, **kwargs):
        if self._listener is not None:
            self._listener(method_name, *args, **kwargs)

class AVModel(Notifier):
    def __init__(self):
        super().__init__()

    @notify_after
    def status(self, info):
        passs


if __name__ == '__main__':
    class TestModel(Notifier):
        def __init__(self):
            super().__init__()
            self._count = 0

        @notify_after
        def inc(self):
            self._count += 1
            return self._count

        @notify_before
        def dec(self, x):
            self._count -= x

        @property
        def count(self):
            return self._count

    a1 = TestModel()
    a1.listener(lambda obj, method_name, *args, **kwargs: print(obj, method_name, *args, **kwargs))
    a1.inc()
    a1.inc()
    a1.dec(10)

    def foo(obj, method_name, *args, **kwargs):
        if method_name == 'inc':
            print('increment, result is', args[0])
        else:
            print('decrement by', args[0])

    a2 = TestModel()
    a2.listener(foo)
    a2.inc()
    a2.inc()
    a2.dec(10)
