from unittest import TestCase

from versions.constraint import Constraint, InvalidConstraint
from versions.constraints import Constraints
from versions.operators import eq
from versions.version import Version


class TestConstraint(TestCase):

    def test_parse(self):
        constraint = Constraint.parse('==1.0')
        self.assertEqual(constraint.operator, eq)
        self.assertEqual(constraint.version, Version(1))

    def test_match(self):
        self.assertTrue(Constraint.parse('==1.0').match(Version(1)))
        self.assertTrue('1' in Constraint.parse('==1.0'))
        self.assertTrue('2' in Constraint.parse('>1.0'))

    def test_eq(self):
        self.assertEqual(Constraint.parse('==1.0'), Constraint.parse('==1.0'))

    def test_parse_raises_InvalidConstraint(self):
        self.assertRaises(InvalidConstraint, Constraint.parse, '')

    def test_repr(self):
        self.assertEqual(repr(Constraint.parse('==1')),
                         "Constraint.parse('==1.0.0')")

    def test_add(self):
        self.assertEqual(Constraint.parse('>1') + '<2',
                         Constraints.parse('>1,<2'))
