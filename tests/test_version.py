from unittest import TestCase

from versions.version import Version, InvalidVersionExpression, \
    get_prerelease_type_precedence, get_postrelease_type_precedence, \
    InvalidVersion


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

    def test_parse_raise_InvalidVersionExpression(self):
        self.assertRaises(InvalidVersionExpression, Version.parse, 'a')
        self.assertRaises(InvalidVersionExpression, Version.parse, '1.a')
        self.assertRaises(InvalidVersionExpression, Version.parse, '1.a.b')
        # Can't have both pre- and post-release information !
        self.assertRaises(InvalidVersionExpression, Version.parse, '1.0.1l-dev')

    def test_parse_postrelease(self):
        v = Version.parse('1.0.1l')
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 1)
        self.assertEqual(v.postrelease, 'l')
        self.assertEqual(v.prerelease, None)
        self.assertEqual(v.build_metadata, None)

    def test_cmp_postrelease(self):
        v101 = Version.parse('1.0.1')
        v101a = Version.parse('1.0.1a')
        v101b = Version.parse('1.0.1b')
        self.assertEqual(v101.__cmp__(v101a), -1)
        self.assertEqual(v101.__cmp__(v101b), -1)
        self.assertEqual(v101a.__cmp__(v101), 1)
        self.assertEqual(v101a.__cmp__(v101a), 0)
        self.assertEqual(v101a.__cmp__(v101b), -1)
        self.assertEqual(v101b.__cmp__(v101), 1)
        self.assertEqual(v101b.__cmp__(v101a), 1)
        self.assertEqual(v101b.__cmp__(v101b), 0)

    def test_cmp_pre_and_postrelease(self):
        self.assertTrue(Version.parse('1.0.1a') > Version.parse('1.0.1-foo'))
        self.assertTrue(Version.parse('1.0.1-foo') < Version.parse('1.0.1f'))
        self.assertTrue(Version.parse('1.0.1f') == Version.parse('1.0.1f'))

    def test_parse_postrelease_digits(self):
        v = Version.parse('2.8.12.3')
        self.assertEqual(v.major, 2)
        self.assertEqual(v.minor, 8)
        self.assertEqual(v.patch, 12)
        self.assertEqual(v.postrelease, 3)
        self.assertEqual(v.prerelease, None)
        self.assertEqual(v.build_metadata, None)

        v12 = Version.parse('2.8.12')
        self.assertTrue(v > v12)
        self.assertTrue(v12 < v)

        v12_1 = Version.parse('2.8.12.1')
        self.assertTrue(v > v12_1)
        self.assertTrue(v12_1 < v)

        v12_5 = Version.parse('2.8.12.5')
        self.assertTrue(v < v12_5)
        self.assertTrue(v12_5 > v)

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
        self.assertEqual(Version(1, 1, 0, prerelease='foo').__cmp__('1.1.0-1'), 1)
        self.assertEqual(Version(1, 1, 0, prerelease=1).__cmp__('1.1.0-foo'), -1)
        self.assertEqual(Version(1, 1, 0).__cmp__('1.1.0-foo'), 1)
        self.assertEqual(Version(1, 1, 0, prerelease='foo').__cmp__('1.1.0'), -1)

    def test_cmp_raise_TypeError(self):
        self.assertRaises(TypeError, Version(1).__cmp__, None)

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
        self.assertEqual(str(Version.parse('1.0.1a')), '1.0.1a')
        self.assertEqual(str(Version.parse('1.0.1.2')), '1.0.1.2')

    def test_repr(self):
        self.assertEqual(repr(Version(1)), "Version.parse('1.0.0')")

    def test_raises_when_having_both_pre_and_postrelease(self):
        self.assertRaises(InvalidVersion,
                          Version, 1, prerelease=1, postrelease=1)


class TestPrereleaseTypePrecedence(TestCase):

    def test(self):
        self.assertEqual(get_prerelease_type_precedence(None), 2)
        self.assertEqual(get_prerelease_type_precedence('foo'), 1)
        self.assertEqual(get_prerelease_type_precedence(1), 0)
        self.assertRaises(TypeError, get_prerelease_type_precedence)


class TestPostreleaseTypePrecedence(TestCase):

    def test(self):
        self.assertEqual(get_postrelease_type_precedence(None), 0)
        self.assertEqual(get_postrelease_type_precedence('foo'), 2)
        self.assertEqual(get_postrelease_type_precedence(1), 1)
        self.assertRaises(TypeError, get_postrelease_type_precedence)
