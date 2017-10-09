from . import PI
from .simple import multiply


def circumference(radius):
    return multiply(2, multiply(PI, radius))