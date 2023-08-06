import sys
sys.path.append('../')
import pytest

from euclipy.core import *
from euclipy.measure import *
from euclipy.polygon import *
from euclipy.theorems import *
from euclipy.tools import *

def test_point_identity():
    assert Point("A") is Point("A")

def test_point_inquality():
    assert Point("A") is not Point("B")

def test_segment_identity():
    assert Segment([Point("A"), Point("B")]) is Segment([Point("A"), Point("B")])

def test_segment_inequality():
    assert Segment([Point("A"), Point("B")]) is not Segment([Point("B"), Point("C")])

def test_segment_measure_identity():
    assert SegmentMeasure(1) is SegmentMeasure(1)

def test_segment_measure_inequality():
    assert SegmentMeasure(1) is not SegmentMeasure(2)

def test_undefined_segment_measure():
    assert SegmentMeasure().value == None

def test_angle_measure_identity():
    assert AngleMeasure(60) is AngleMeasure(60)

def test_angle_measure_inequality():
    assert AngleMeasure(60) is not AngleMeasure(90)

def test_undefined_angle_measure():
    assert AngleMeasure().value == None

def test_dummy():
    assert True