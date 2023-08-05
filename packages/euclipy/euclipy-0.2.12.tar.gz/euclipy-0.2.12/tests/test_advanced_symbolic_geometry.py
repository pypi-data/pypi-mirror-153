import sys
from tkinter import image_names
sys.path.append('../')
import pytest

from euclipy.core import *
from euclipy.measure import *
from euclipy.polygon import *
from euclipy.tools import *
from euclipy.theorems import *

def test_sum_theorem():
    T1 = Triangle([Point("A"), Point("B"), Point("C")])
    T1.angles[0].measure.value = 30
    T1.angles[1].measure.value = 60
    triangle_sum_theorem(T1)
    Expressions().solve()
    assert T1.angles[2].measure.value == 90
