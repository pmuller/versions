from unittest import TestCase

from versions.packages import Package, InvalidPackage


class TestPackage(TestCase):

    def test_parse(self):
        package = Package.parse('foo 1')
        self.assertEqual(package.name, 'foo')
        self.assertEqual(package.version, '1.0.0')
        self.assertRaises(InvalidPackage, Package.parse, 'foo')

    def test_hash(self):
        package = Package.parse('foo 1')
        self.assertEqual(hash(package),
                         hash(package.name) ^ hash(package.version))
