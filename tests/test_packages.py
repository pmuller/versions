from unittest import TestCase

from versions.packages import Package


class TestPackage(TestCase):

    def test_hash(self):
        package = Package('foo', 1)
        self.assertEqual(hash(package),
                         hash(package.name) ^ hash(package.version))
