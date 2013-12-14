from unittest import TestCase

from versions.packages import Package, InvalidPackageExpression, \
    InvalidPackageInfo
from versions.requirements import Requirement


class TestPackage(TestCase):

    def test_hash(self):
        package = Package('foo', 1)
        self.assertEqual(hash(package),
                         hash(package.name) ^ hash(package.version))

    def test_parse(self):
        p1 = Package.parse(' foo - 1.2 ')
        self.assertEqual(p1.name, 'foo')
        self.assertEqual(p1.version, '1.2.0')
        p2 = Package.parse(' foo - 1.2 ; depends bar >2,<3,>2.5; depends baz')
        self.assertTrue(Requirement.parse('bar >2,<3,>2.5') in p2.dependencies)
        self.assertTrue(Requirement.parse('baz') in p2.dependencies)
        self.assertEqual(len(p2.dependencies), 2)

    def test_parse_raises(self):
        self.assertRaises(InvalidPackageExpression, Package.parse, '#$!@')
        self.assertRaises(InvalidPackageInfo, Package.parse, 'foo-1;#$!@')
