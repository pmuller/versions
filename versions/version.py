import re
import sys

from .errors import Error


if sys.version_info[0] == 3:
    cmp = lambda a, b: (a > b) - (a < b)


# Regular expression used to parse versions.
# It parses semantic versions and tries to normalize not semantic versions
# into semantic ones.
RE = re.compile("""
^
(?P<major>\d+)
(?:
    \.
    (?P<minor>\d+)
    (?:
        \.
        (?P<patch>\d+)
    )?
)?
(?:
    -
    (?P<prerelease>[0-9a-zA-Z.-]*)
)?
(?:
    \+
    (?P<build_metadata>[0-9a-zA-Z.-]*)
)?
$
""", re.X)


def get_prerelease_type_precedence(prerelease):
    if prerelease is None:
        return 2
    elif isinstance(prerelease, str):
        return 1
    elif isinstance(prerelease, int):
        return 0
    else:
        raise TypeError(prerelease)


class InvalidVersion(Error):
    """Raised when failing to parse a ``version``.
    """
    def __init__(self, version):
        #: The bogus version.
        self.version = version
        message = 'Invalid version: %r' % version
        super(InvalidVersion, self).__init__(message)


class Version(object):
    """A package version.

    :param int major: Version major number
    :param int minor: Version minor number
    :param int patch: Version patch number
    :param prerelease: Version prerelease
    :type prerelease: ``str``, ``int`` or ``None``
    :param build_metadata: Version build metadata
    :type build_metadata: ``None`` or ``str``

    This class constructor is usually not called directly.
    For version string parsing, see ``Version.parse``.

    """
    def __init__(self, major, minor=0, patch=0, prerelease=None,
                 build_metadata=None):
        #: Version major number
        self.major = major
        #: Version minor number
        self.minor = minor
        #: Version patch number
        self.patch = patch
        #: Version prerelease
        self.prerelease = prerelease
        #: Version build metadata
        self.build_metadata = build_metadata

    def __hash__(self):
        return hash(self.major) ^ hash(self.minor) ^ hash(self.patch) ^ \
            hash(self.prerelease) ^ hash(self.build_metadata)

    @classmethod
    def parse(cls, version_string):
        """Parses a ``version_string`` and returns a :py:class:`~Version`
        object.
        """
        match = RE.match(version_string)
        if match:
            major_str, minor_str, patch_str, prerelease_str, \
                build_metadata = match.groups()

            major = int(major_str)

            if minor_str:
                minor = int(minor_str)
            else:
                minor = 0

            if patch_str:
                patch = int(patch_str)
            else:
                patch = 0

            if prerelease_str:
                try:
                    prerelease = int(prerelease_str)
                except ValueError:
                    prerelease = prerelease_str
            else:
                prerelease = None

            return cls(major, minor, patch, prerelease, build_metadata)

        else:
            raise InvalidVersion(version_string)

    def __cmp__(self, other):
        
        if isinstance(other, str):
            other = Version.parse(other)
        
        if not isinstance(other, Version):
            raise InvalidVersion(other)

        major_cmp = cmp(self.major, other.major)
        if major_cmp == 0:
            minor_cmp = cmp(self.minor, other.minor)
            if minor_cmp == 0:
                patch_cmp = cmp(self.patch, other.patch)
                if patch_cmp == 0:
                    prerelease_t_cmp = cmp(
                        get_prerelease_type_precedence(self.prerelease),
                        get_prerelease_type_precedence(other.prerelease))
                    if prerelease_t_cmp == 0:
                        if self.prerelease is None:
                            return 0
                        else:
                            return cmp(self.prerelease, other.prerelease)
                    else:
                        return prerelease_t_cmp
                else:
                    return patch_cmp
            else:
                return minor_cmp
        else:
            return major_cmp

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __str__(self):
        """Convert version objects to strings::

            >>> str(Version.parse('1.0.0')) == '1.0.0'
            True
            >>> str(Version.parse('1.0')) == '1.0.0'
            True

        """
        version = '%i.%i.%i' % (self.major, self.minor, self.patch)
        if self.prerelease:
            version += '-%s' % self.prerelease
        if self.build_metadata:
            version += '+' + self.build_metadata
        return version

    def __repr__(self):
        return 'Version.parse(%r)' % str(self)
