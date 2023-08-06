import sympy
import sys
sys.path.append("./")

from euclipy.core import Registry, Expressions
from euclipy.polygon import Triangle
from euclipy.tools import pairs_in_iterable


def triangle_sum_theorem(triangle:Triangle) -> bool:
    Expressions().add_expression(sum([a.measure.symbol for a in triangle.angles]) - 180)
    return True

Registry().add_theorem(triangle_sum_theorem, 'Triangle')

def pythagorean_theorem(triangle:Triangle) -> bool:
    is_right_triangle = Triangle.is_right_triangle(triangle)
    if is_right_triangle is not False:
        print(is_right_triangle)
        Expressions().add_expression(is_right_triangle[0].measure.symbol**2 + is_right_triangle[1].measure.symbol**2 - is_right_triangle[2].measure.symbol**2)
        return True

Registry().add_theorem(pythagorean_theorem, 'Triangle')

def isosceles_triangle_theorem(triangle: Triangle) -> bool:
    theorem_applied = False
    congruent_sides = triangle.congruent_sides()
    if congruent_sides:
        for side_pairs in pairs_in_iterable(congruent_sides):
            vertex = side_pairs[0].common_point_with(side_pairs[1])
            angles = [a for a in triangle.angles if a.vertex() != vertex]
            angles[0].measure.set_equal_to(angles[1].measure)
        theorem_applied = True
    congruent_angles = triangle.congruent_angles()
    if congruent_angles:
        for angle_pairs in pairs_in_iterable(congruent_angles):
            sides = [side for angle in angle_pairs for side in triangle.edges if angle.vertex() not in side.endpoints]
            sides[0].measure.set_equal_to(sides[1].measure)
        theorem_applied = True
    return theorem_applied

Registry().add_theorem(isosceles_triangle_theorem, 'Triangle')
