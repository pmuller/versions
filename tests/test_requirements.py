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
