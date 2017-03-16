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

#
# Method interception ideas taken from:
# http://stackoverflow.com/questions/2704434/intercept-method-calls-in-python
# http://stackoverflow.com/questions/4723717/how-to-intercept-instance-method-calls
#

class NotifyError(Exception):
    """notification exception"""
    pass

def check_private(name):
    if name.startswith('_'):
        raise NotifyError('cannot notify on private properties')

class Notifier(object):
    def __init__(self):
        # calling __setattr__ of this class is too early as __setattr__ checks for _notify_property
        super().__setattr__('_notify_property', {})
        super().__setattr__('_notify_before', {})
        super().__setattr__('_notify_after', {})

    def notify_before(self, name, fun):
        check_private(name)
        if name in self._notify_after:
            raise NotifyError('cannot notify before and after')
        self._notify_before[name] = fun
    
    def notify_after(self, name, fun):
        check_private(name)
        if name in self._notify_before:
            raise NotifyError('cannot notify before and after')
        self._notify_after[name] = fun

    def notify_property(self, name, fun):
        check_private(name)
        self._notify_property[name] = fun

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if not callable(attr):
            return attr
        if name in self._notify_before:
            fun = self._notify_before[name]
            def notify_before_wrapper(*args, **kwargs):
                fun(*args, **kwargs)
                return attr(*args, **kwargs)
            return notify_before_wrapper
        if name in self._notify_after:
            fun = self._notify_after[name]
            def notify_after_wrapper(*args, **kwargs):
                retval = attr(*args, **kwargs)
                fun(retval)
                return retval
            return notify_after_wrapper
        return attr            

    def __setattr__(self, name, value):
        if not name in self._notify_property:
            super().__setattr__(name, value)
        try:
            old_value = super().__getattribute__(name)
        except:
            old_value = None
        super().__setattr__(name, value)
        if old_value != value:
            self._notify_property[name](old_value, value)

if __name__ == '__main__':
    class TestCounter(Notifier):
        def __init__(self):
            super().__init__()
            self._count = 0

        def inc(self):
            self._count += 1
            return self._count

        def dec(self, x):
            self._count -= x

        def fun(self):
            return 43

        @property
        def count(self):
            return self._count

        @count.setter
        def count(self, value):
            self._count = value


    a1 = TestCounter()
    a1.notify_before('dec', lambda *args, **kwargs: print("I'm the before 'dec' lambda", *args, **kwargs))
    a1.notify_after('inc', lambda retval: print("I'm the after 'inc' lambda", retval))
    a1.notify_before('fun', lambda *args, **kwargs: print("I'm the before 'fun' lambda", *args, **kwargs))
    a1.notify_property('count', lambda old_value, value: print("I'm the 'count' property lambda", 'old', old_value, 'new', value))
    a1.inc()
    a1.inc()
    a1.dec(10)
    a1.fun()
    c = a1.count 
    print('count is', c)
    a1.count = c + 1

    import traceback
    try:
        a1.notify_property('_count', lambda value: print("whoot?"))
    except:
        traceback.print_exc()
    try:
        a1.notify_after('fun', lambda retval: print("I'm the after 2 lambda", retval))
    except:
        traceback.print_exc()
