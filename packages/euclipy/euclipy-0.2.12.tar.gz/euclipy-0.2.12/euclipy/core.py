from collections import defaultdict
import pprint
import warnings
import sympy

class Registry:
    '''Singleton registry of:
        - Geometry instances (GeometricObjects and GeometricMeasures)
        - Theorems
    '''
    def __new__(cls):
        '''objects and measures are dictionaries with:
            - keys: registry key
            - values: dictionaries mapping labels to registered objects/measures
        '''
        if not hasattr(cls, 'instance'):
            cls.instance = super(Registry, cls).__new__(cls)
            cls.instance.objects = defaultdict(dict)
            cls.instance.measures = defaultdict(dict)
            cls.instance.theorems = defaultdict(list)
            cls.instance.auto_label_counter = defaultdict(int)
        return cls.instance
   
    def add_object(self, geometric_object):
        self.objects[geometric_object._registry_key][geometric_object.label] = geometric_object

    def add_measure(self, measure):
        self.measures[measure._registry_key][measure.label] = measure
    
    def remove_measure(self, measure):
        self.measures[measure._registry_key].pop(measure.label, None)

    def add_theorem(self, theorem, applies_to):
        self.theorems[applies_to].append(theorem)
            
    def get_auto_label(self, geometry):
        self.auto_label_counter[geometry._registry_key] += 1
        return f'{geometry._label_prefix}{self.auto_label_counter[geometry._registry_key]}'

    def find_object(self, registry_key, label):
        try:
            return self.objects[registry_key][label]
        except KeyError:
            return None

    def search_measure_by_class_and_value(self, measure_cls, value):
        try:
            return [m for m in self.measures[measure_cls._registry_key].values() if m.value == value][0]
        except IndexError:
            return None

    def search_measure_by_label(self, label):
        try:
            return[m for key in self.measures for m in self.measures[key].values() if m.label == label][0]
        except IndexError:
            return None

    def search_polygon(self, registry_key, points: list):
        '''Find polygon that shares points, regardless of point order
        '''
        try:
            matches = [p for p in iter(self.objects[registry_key].values()) if set(p.points) == set(points)]
            return matches[0] if matches else None
        except KeyError:
            return None

    def print_registry(self):
        pprint.pprint(self.objects)
        pprint.pprint(self.measures)
        pprint.pprint(self.theorems)

class Geometry:
    @classmethod
    @property
    def _registry_key(cls):
        return cls.__name__

class Expressions:
    '''
    Zero-valued expressions derived from theorems
    '''
    def __new__(cls):
        '''expressions is a list containing zero-valued expressions derived from theorems.
        The expressions are constructed in sympy. Symbols representing measures use the label of the corresponding measures.:
        '''
        if not hasattr(cls, 'instance'):
            cls.instance = super(Expressions, cls).__new__(cls)
            cls.instance.expressions = list()
        return cls.instance

    @staticmethod
    def measure_symbol(measure):
        return sympy.Symbol(measure.label)

    def add_expression(self, expression):
        original_expression = expression
        for s in expression.free_symbols:
            m = Registry().search_measure_by_label(s.name)
            if m.value:
                expression = expression.subs(s, m.value)
        if expression == 0:
            warnings.warn(f'{original_expression} contained no unknowns', stacklevel=3)
        else:
            self.expressions.append(expression)

    def substitute(self, var, sol):
        for i, e in enumerate(self.expressions):
            self.expressions[i] = e.subs(var, sol)
    
    def solve(self):
        # Find systems with numbers of equations equal to the number of free variables and solve them, using sympy
        solution = sympy.solve(self.expressions)
        # For all solutions with no free symbols, substitute the answer into the measure
        for var, sol in solution.items():
            if not sol.free_symbols:
                # Find the measure that corresponds to the variable
                var_measure = Registry().search_measure_by_label(var.name)
                # Set the measure value to the solution
                var_measure.value = sol
                self.substitute(var, sol)
        self.expressions = [e for e in self.expressions if e != 0]