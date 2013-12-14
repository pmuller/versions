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
        self.assertEqual(Constraints() + Constraints.parse('>1'),
                         Constraints.parse('>1'))
        self.assertEqual(Constraints() + Constraint.parse('>1'),
                         Constraints.parse('>1'))
        self.assertRaises(TypeError, Constraints().__add__, 42)

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

    def test_eq_invalid_constraints_str(self):
        self.assertFalse(Constraints() == '#@$!')


class TestMerge(TestCase):

    def assertMerge(self, input, output):
        self.assertEqual(merge(input), output)

    def test_raises_ExclusiveConstraints(self):
        self.assertRaises(ExclusiveConstraints, merge,
                          [Constraint.parse('==1'), Constraint.parse('==2')])
        self.assertRaises(ExclusiveConstraints, merge,
                          [Constraint.parse('>2'), Constraint.parse('<1')])
        self.assertRaises(ExclusiveConstraints, merge,
                          [Constraint.parse('>2'), Constraint.parse('<2')])
        self.assertRaises(ExclusiveConstraints, merge,
                          [Constraint.parse('>2'), Constraint.parse('<=2')])
        # the first 2 constraints will be merge into ==2,
        # which conflicts with !=2
        self.assertRaises(ExclusiveConstraints, merge,
                          [Constraint.parse('<=2'), Constraint.parse('>=2'),
                           Constraint.parse('!=2')])

    def test(self):

        constraints = [Constraint.parse('>1'), Constraint.parse('<2')]
        self.assertMerge(constraints, constraints)

        self.assertMerge([Constraint.parse('<2'), Constraint.parse('<3')],
                         [Constraint.parse('<2.0.0')])

        self.assertMerge([Constraint.parse('<2'), Constraint.parse('>=1')],
                         [Constraint.parse('>=1.0.0'), Constraint.parse('<2.0.0')])

        self.assertMerge([Constraint.parse('>=2'), Constraint.parse('>2')],
                         [Constraint.parse('>2.0.0')])

        self.assertMerge([Constraint.parse('>1'), Constraint.parse('>=2')],
                         [Constraint.parse('>=2.0.0')])

        self.assertMerge([Constraint.parse('<2'), Constraint.parse('<=1')],
                         [Constraint.parse('<=1.0.0')])

        self.assertMerge([Constraint.parse('<=2'), Constraint.parse('<1')],
                         [Constraint.parse('<1.0.0')])

        self.assertMerge([Constraint.parse('<=2'), Constraint.parse('>=2')],
                         [Constraint.parse('==2.0.0')])

        # Negative constraints should not be omitted!
        self.assertMerge([Constraint.parse('!=2'), Constraint.parse('!=1')],
                         [Constraint.parse('!=1.0.0'), Constraint.parse('!=2.0.0')])
