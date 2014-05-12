import re

from .errors import Error
from .compat import cmp


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
    (?P<postrelease_alpha>[A-Za-z]+)?
    |
    (?:
        \.
        (?P<postrelease_digit>\d+)?
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


def get_postrelease_type_precedence(postrelease):
    if isinstance(postrelease, str):
        return 2
    elif isinstance(postrelease, int):
        return 1
    elif postrelease is None:
        return 0
    else:
        raise TypeError(postrelease)


class InvalidVersion(Error):
    """Raised when a software version is invalid.
    """


class InvalidVersionExpression(InvalidVersion):
    """Raised when failing to parse a
    :ref:`version expression <version-expressions>`.
    """
    def __init__(self, version_expression):
        #: The bogus version expression.
        self.version_expression = version_expression
        message = 'Invalid version expression: %r' % version_expression
        super(InvalidVersionExpression, self).__init__(message)


class Version(object):
    """A package version.

    :param int major: Version major number
    :param int minor: Version minor number
    :param int patch: Version patch number
    :param postrelease: Version postrelease identifier
    :type postrelease: ``str``, ``int`` or ``None``
    :param prerelease: Version prerelease identifier
    :type prerelease: ``str``, ``int`` or ``None``
    :param build_metadata: Version build metadata
    :type build_metadata: ``None`` or ``str``

    This class constructor is usually not called directly.
    For version string parsing, see ``Version.parse``.

    """
    def __init__(self, major, minor=0, patch=0, postrelease=None,
                 prerelease=None, build_metadata=None):

        print 'wtf', postrelease, prerelease
        if postrelease is not None and prerelease is not None:
            raise InvalidVersion('A version cannot both have a pre- '
                                 'and a post-release identifier')

        #: Version major number
        self.major = major
        #: Version minor number
        self.minor = minor
        #: Version patch number
        self.patch = patch
        #: Version postrelease
        self.postrelease = postrelease
        #: Version prerelease
        self.prerelease = prerelease
        #: Version build metadata
        self.build_metadata = build_metadata

    def __hash__(self):
        return hash(self.major) ^ hash(self.minor) ^ hash(self.patch) ^ \
            hash(self.prerelease) ^ hash(self.postrelease) ^ \
            hash(self.build_metadata)

    @classmethod
    def parse(cls, version_string):
        """Parses a ``version_string`` and returns a :py:class:`~Version`
        object.
        """
        match = RE.match(version_string)
        if match:
            major_str, minor_str, patch_str, postrelease_alpha, \
                postrelease_digit, prerelease_str, build_metadata = \
                match.groups()

            if postrelease_digit:
                postrelease = int(postrelease_digit)
            else:
                postrelease = postrelease_alpha

            # A well-defined version cannot both have a pre- and a
            # post-release identifier.
            if postrelease and prerelease_str:
                raise InvalidVersionExpression(version_string)

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

            return cls(major, minor, patch,
                       postrelease, prerelease, build_metadata)

        else:
            raise InvalidVersionExpression(version_string)

    def __cmp__(self, other):
        if isinstance(other, str):
            other = Version.parse(other)
        
        if not isinstance(other, Version):
            raise TypeError(other)

        major_cmp = cmp(self.major, other.major)
        if major_cmp == 0:
            minor_cmp = cmp(self.minor, other.minor)
            if minor_cmp == 0:
                patch_cmp = cmp(self.patch, other.patch)
                if patch_cmp == 0:
                    if self.postrelease or other.postrelease:
                        postrelease_t_cmp = cmp(
                            get_postrelease_type_precedence(self.postrelease),
                            get_postrelease_type_precedence(other.postrelease))
                        if postrelease_t_cmp == 0:
                            if self.postrelease is None:
                                return 0
                            else:
                                return cmp(self.postrelease, other.postrelease)
                        else:
                            return postrelease_t_cmp
                    elif self.prerelease or other.prerelease:
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
                        return 0
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
        if self.postrelease:
            if isinstance(self.postrelease, int):
                version += '.%i' % self.postrelease
            else:
                version += self.postrelease
        elif self.prerelease:
            version += '-%s' % self.prerelease
        if self.build_metadata:
            version += '+' + self.build_metadata
        return version

    def __repr__(self):
        return 'Version.parse(%r)' % str(self)
