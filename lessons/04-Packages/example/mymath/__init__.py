# For real life example, see how pandas organizes their imports:
# https://github.com/pandas-dev/pandas/blob/master/pandas/__init__.py

print('__init__.py called')
from .constants import pi
PI = pi
del pi

from . import geometry as geo # change namespace
del geometry

from .simple import * # import everything


