from unittest import TestCase

from versions.constraints import Constraints, merge, ExclusiveConstraints
from versions.constraint import Constraint


class TestConstraints(TestCase):

    def test_match(self):
        self.assertTrue(Constraints.parse('>1,<2').match('1.5'))

    def test_match_in(self):
        self.assertTrue('1.5' in Constraints.parse('>1,<2'))

    def test_parse(self):
        constraints = Constraints.parse('>1,<2')

    def test_add(self):
        self.assertEqual(Constraints() + '>1', Constraints.parse('>1'))

    def test_iadd(self):
        constraints = Constraints()
        constraints += '>1'
        self.assertEqual(constraints, Constraints.parse('>1'))

    def test_str(self):
        self.assertEqual(str(Constraints([Constraint.parse('>1'),
                                          Constraint.parse('<2')])),
                         '>1.0.0,<2.0.0')

    def test_repr(self):
        self.assertEqual(repr(Constraints()), "Constraints()")
        self.assertEqual(repr(Constraints.parse('==1')),
                         "Constraints.parse('==1.0.0')")


class TestMerge(TestCase):

    def test_empty_constraints(self):
        constraint_str = '==1'
        constraint = Constraint.parse(constraint_str)
        self.assertEqual(merge([], constraint_str), [constraint])

    def test_raises_ExclusiveConstraints(self):
        self.assertRaises(ExclusiveConstraints, merge,
                          [Constraint.parse('==1')], '==2')
        self.assertRaises(ExclusiveConstraints, merge,
                          [Constraint.parse('>2')], '<1')
        self.assertRaises(ExclusiveConstraints, merge,
                          [Constraint.parse('>2')], '<2')
        self.assertRaises(ExclusiveConstraints, merge,
                          [Constraint.parse('>2')], '<=2')

    def test(self):
        self.assertEqual(merge([Constraint.parse('>1')], '<2'),
                         [Constraint.parse('>1.0.0'),
                          Constraint.parse('<2.0.0')])
        self.assertEqual(merge([Constraint.parse('<2')], '<3'),
                         [Constraint.parse('<2.0.0')])
        self.assertEqual(merge([Constraint.parse('<2')], '>=1'),
                         [Constraint.parse('>=1.0.0'),
                          Constraint.parse('<2.0.0')])
        self.assertEqual(merge([Constraint.parse('>=2')], '>2'),
                         [Constraint.parse('>2.0.0')])
        self.assertEqual(merge([Constraint.parse('>1')], '>=2'),
                         [Constraint.parse('>=2.0.0')])
        self.assertEqual(merge([Constraint.parse('<2')], '<=1'),
                         [Constraint.parse('<=1.0.0')])
        self.assertEqual(merge([Constraint.parse('<=2')], '<1'),
                         [Constraint.parse('<1.0.0')])
        self.assertEqual(merge([Constraint.parse('<=2')], '>=2'),
                         [Constraint.parse('==2.0.0')])
