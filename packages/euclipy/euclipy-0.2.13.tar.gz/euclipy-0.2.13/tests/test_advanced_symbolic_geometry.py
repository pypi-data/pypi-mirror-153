import sys
sys.path.append('../')
import pytest

from euclipy.core import *
from euclipy.measure import *
from euclipy.polygon import *
from euclipy.tools import *
from euclipy.theorems import *

def test_sum_theorem():
    try:
        del Registry.instance
    except AttributeError:
        pass
    T1 = Triangle([Point("A"), Point("B"), Point("C")])
    T1.angles[0].measure.value = 30
    T1.angles[1].measure.value = 60
    triangle_sum_theorem(T1)
    Expressions().solve()
    assert T1.angles[2].measure.value == 90

def test_isosceles_triangle_theorem():
    try:
        del Registry.instance
    except AttributeError:
        pass
    T1 = Triangle([Point("A"), Point("B"), Point("C")])
    T1.angles[0].measure.value = 45
    T1.angles[1].measure.value = 45
    T1.edges[2].measure.value = 1
    isosceles_triangle_theorem(T1)
    Expressions().solve()
    assert T1.edges[0].measure is T1.edges[2].measure

def test_pythagorean_theorem():
    try:
        del Registry.instance
    except AttributeError:
        pass
    T1 = Triangle([Point("A"), Point("B"), Point("C")])
    T1.angles[2].measure.value = 90
    T1.edges[0].measure.value = 3
    T1.edges[1].measure.value = 5
    pythagorean_theorem(T1)
    Expressions().solve()
    assert T1.edges[2].measure.value == 4
    
test_sum_theorem()
test_isosceles_triangle_theorem()
test_pythagorean_theorem()
