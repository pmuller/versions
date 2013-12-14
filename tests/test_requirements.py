from unittest import TestCase

from versions.requirements import Requirement, InvalidRequirement


class TestRequirement(TestCase):

    def test_parse(self):
        r = Requirement.parse('foo')
        self.assertEqual(r.name, 'foo')
        self.assertEqual(r.version_constraints, None)
        self.assertEqual(r.build_options, None)

        r2 = Requirement.parse('vim [python, ruby] >=7, <8')
        self.assertEqual(r2.name, 'vim')
        self.assertEqual(r2.version_constraints, '>=7,<8')
        self.assertEqual(r2.build_options, set(['python', 'ruby']))

    def test_invalid(self):
        self.assertRaises(InvalidRequirement, Requirement.parse, '@($%#$*)@')

    def test_hash(self):
        self.assertEqual(hash(Requirement.parse('foo')),
                         hash('foo') ^ hash(None) ^ hash(None))

    def test_eq(self):
        self.assertTrue(Requirement.parse('foo') == 'foo')
        self.assertFalse(Requirement.parse('foo') == 'bar')
        self.assertFalse(Requirement.parse('foo') == '#$@!')

    def test_str(self):
        self.assertEqual(str(Requirement.parse('foo')), 'foo')
        self.assertEqual(str(Requirement.parse('foo==1')), 'foo==1.0.0')
        self.assertEqual(str(Requirement.parse('foo [ bar ]')), 'foo[bar]')
        self.assertEqual(str(Requirement.parse('vim [python, perl] >7,<8')),
                         'vim[python,perl]>7.0.0,<8.0.0')

    def test_repr(self):
        self.assertEqual(repr(Requirement.parse('foo')),
                         "Requirement.parse('foo')")

    def test_add(self):
        Requirement.parse('foo==1.0') + 'foo'
        Requirement.parse('foo[bar]==1.0') + 'foo'
        Requirement.parse('foo[bar]>=1.0') + 'foo<2'
        r = Requirement('foo') + 'foo ==1.0'
        self.assertEqual(r.version_constraints, '==1.0')
        r2 = Requirement.parse('foo[bar]') + 'foo[baz]'
        self.assertEqual(r2.build_options, set(['bar', 'baz']))

    def test_add_raises(self):
        self.assertRaises(InvalidRequirement,
                          Requirement('foo').__add__, 'bar')
