import re
import sys

from .errors import Error


if sys.version_info[0] == 3:
    def cmp(a, b):
        if a > b:
            return 1
        elif a < b:
            return -1
        else:  # a == b
            return 0


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


class InvalidVersion(Error):
    """Raised when failing to parse a ``version``.
    """
    def __init__(self, version):
        #: The bogus version.
        self.version = version
        #: The error message.
        self.message = 'Invalid version: %r' % version


class Version(object):
    """A package version.

    :param int major: Version major number
    :param int minor: Version minor number
    :param int patch: Version patch number
    :param prerelease: Version prerelease
    :type prerelease: ``str``, ``int`` or ``None``
    :param build_metadata: Version build metadata
    :type build_metadata: ``None`` or ``set`` of ``str``

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
        build_md_h = hash(tuple(self.build_metadata)) if self.build_metadata \
            else hash(None)
        return hash(self.major) ^ hash(self.minor) ^ hash(self.patch) ^ \
            hash(self.prerelease) ^ build_md_h

    @classmethod
    def parse(cls, version_string):
        """Parses a ``version_string`` and returns a :py:class:`~Version`
        object::

            >>> Version.parse('1.0.0') > Version.parse('0.1')
            True

        """
        match = RE.match(version_string)
        if match:
            major_str, minor_str, patch_str, prerelease_str, \
                build_metadata_str = match.groups()

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

            if build_metadata_str:
                build_metadata = set(
                    s for s in build_metadata_str.split('.') if s)
            else:
                build_metadata = None

            return cls(major, minor, patch, prerelease, build_metadata)

        else:
            raise InvalidVersion(version_string)

    def __cmp__(self, other):
        if isinstance(other, str):
            other = Version.parse(other)
        if not isinstance(other, Version):
            raise InvalidVersion(other)
        if self.major > other.major:
            return 1
        elif self.major < other.major:
            return -1
        else:  # self.major == other.major
            if self.minor > other.minor:
                return 1
            elif self.minor < other.minor:
                return -1
            else:  # self.minor == other.minor
                if self.patch > other.patch:
                    return 1
                elif self.patch < other.patch:
                    return -1
                else:  # self.patch == other.patch
                    if self.prerelease is None and other.prerelease is None:
                        return 0
                    elif self.prerelease is not None \
                            and other.prerelease is None:
                        return -1
                    elif self.prerelease is None \
                            and other.prerelease is not None:
                        return 1
                    # self.prerelease is not None and
                    # other.prerelease is not None
                    else:
                        if isinstance(self.prerelease, int) and \
                                not isinstance(other.prerelease, int):
                            # other string prerelease has precedence
                            return -1
                        if not isinstance(self.prerelease, int) and \
                                isinstance(other.prerelease, int):
                            # self string prerelease has precedence
                            return 1
                        # self.prerelease and other.prerelease are both str
                        # or int
                        return cmp(self.prerelease, other.prerelease)

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
            version += '+' + '.'.join(sorted(self.build_metadata))
        return version

    def __repr__(self):
        return 'Version.parse(%r)' % str(self)
