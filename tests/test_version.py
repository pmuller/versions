from unittest import TestCase

from versions.version import Version, InvalidVersion, \
    get_prerelease_type_precedence


class TestVersion(TestCase):

    def test_parse_semver2_v1(self):
        v1 = Version.parse('1.0.0')
        self.assertEqual(v1.major, 1)
        self.assertEqual(v1.minor, 0)
        self.assertEqual(v1.patch, 0)
        self.assertEqual(v1.prerelease, None)
        self.assertEqual(v1.build_metadata, None)

    def test_parse_semver2_v1_1(self):
        v1 = Version.parse('1.0.0-1')
        self.assertEqual(v1.major, 1)
        self.assertEqual(v1.minor, 0)
        self.assertEqual(v1.patch, 0)
        self.assertEqual(v1.prerelease, 1)
        self.assertEqual(v1.build_metadata, None)

    def test_parse_semver2_v1_dev(self):
        v1 = Version.parse('1.0.0-dev')
        self.assertEqual(v1.major, 1)
        self.assertEqual(v1.minor, 0)
        self.assertEqual(v1.patch, 0)
        self.assertEqual(v1.prerelease, 'dev')
        self.assertEqual(v1.build_metadata, None)

    def test_parse_semver2_v1_dev_foo_bar(self):
        v1 = Version.parse('1.0.0-dev+foo.bar')
        self.assertEqual(v1.major, 1)
        self.assertEqual(v1.minor, 0)
        self.assertEqual(v1.patch, 0)
        self.assertEqual(v1.prerelease, 'dev')
        self.assertEqual(v1.build_metadata, 'foo.bar')

    def test_parse_partial(self):
        v1 = Version.parse('1')
        self.assertEqual(v1.major, 1)
        self.assertEqual(v1.minor, 0)
        self.assertEqual(v1.patch, 0)
        self.assertEqual(v1.prerelease, None)
        self.assertEqual(v1.build_metadata, None)

    def test_parse_raise_InvalidVersion(self):
        self.assertRaises(InvalidVersion, Version.parse, 'a')
        self.assertRaises(InvalidVersion, Version.parse, '1.a')
        self.assertRaises(InvalidVersion, Version.parse, '1.a.b')

    def test_cmp_major_eq(self):
        self.assertEqual(Version(1).__cmp__('1'), 0)

    def test_cmp_major_gt(self):
        self.assertEqual(Version(2).__cmp__('1'), 1)

    def test_cmp_major_lt(self):
        self.assertEqual(Version(1).__cmp__('2'), -1)

    def test_cmp_minor_gt(self):
        self.assertEqual(Version(1, 1).__cmp__('1'), 1)

    def test_cmp_minor_lt(self):
        self.assertEqual(Version(1).__cmp__('1.1'), -1)

    def test_cmp_patch_gt(self):
        self.assertEqual(Version(1, 1, 1).__cmp__('1.1'), 1)

    def test_cmp_patch_lt(self):
        self.assertEqual(Version(1, 1, 0).__cmp__('1.1.1'), -1)

    def test_cmp_patch_eq(self):
        self.assertEqual(Version(1, 1, 0).__cmp__('1.1.0'), 0)

    def test_cmp_prerelease(self):
        self.assertEqual(Version(1, prerelease='foo').__cmp__(Version(1)), -1)
        self.assertEqual(Version(1, prerelease='foo').__cmp__('1-foo'), 0)
        self.assertEqual(Version(1, prerelease='foo').__cmp__('1-bar'), 1)
        self.assertEqual(Version(1, prerelease='bar').__cmp__('1-foo'), -1)
        self.assertEqual(Version(1, 1, 0, 'foo').__cmp__('1.1.0-1'), 1)
        self.assertEqual(Version(1, 1, 0, 1).__cmp__('1.1.0-foo'), -1)
        self.assertEqual(Version(1, 1, 0).__cmp__('1.1.0-foo'), 1)
        self.assertEqual(Version(1, 1, 0, 'foo').__cmp__('1.1.0'), -1)

    def test_cmp_raise_InvalidVersion(self):
        self.assertRaises(InvalidVersion, Version(1).__cmp__, None)

    def test_eq(self):
        self.assertTrue(Version(1) == Version(1))

    def test_ne(self):
        self.assertTrue(Version(1, 1) != Version(1))

    def test_gt(self):
        self.assertTrue(Version(2) > Version(1))

    def test_ge(self):
        self.assertTrue(Version(2) >= Version(1))
        self.assertTrue(Version(2) >= Version(2))

    def test_lt(self):
        self.assertTrue(Version(1) < Version(2))

    def test_le(self):
        self.assertTrue(Version(1) <= Version(1))
        self.assertTrue(Version(1) <= Version(2))

    def test_str(self):
        self.assertEqual(str(Version(1, 0, 0)), '1.0.0')
        self.assertEqual(str(Version(1, 0)), '1.0.0')
        self.assertEqual(str(Version(1)), '1.0.0')
        self.assertEqual(str(Version.parse('1')), '1.0.0')
        self.assertEqual(str(Version.parse('1-foo')), '1.0.0-foo')
        self.assertEqual(str(Version.parse('1+foo')), '1.0.0+foo')
        self.assertEqual(str(Version.parse('1-foo+bar.baz')),
                         '1.0.0-foo+bar.baz')

    def test_repr(self):
        self.assertEqual(repr(Version(1)), "Version.parse('1.0.0')")


class TestGetPrereleaseTypePrecedence(TestCase):

    def test(self):
        self.assertEqual(get_prerelease_type_precedence(None), 2)
        self.assertEqual(get_prerelease_type_precedence('foo'), 1)
        self.assertEqual(get_prerelease_type_precedence(1), 0)
        self.assertRaises(TypeError, get_prerelease_type_precedence, [])
