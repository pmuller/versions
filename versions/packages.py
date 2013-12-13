import re

from .version import Version
from .errors import Error


class InvalidPackage(Error):
    """Raised when failing to parse a ``package``.
    """
    def __init__(self, package):
        #: The bogus package.
        self.package = package
        message = 'Invalid package: %r' % package
        super(InvalidPackage, self).__init__(message)


class Package(object):
    """A package.

    :param str name: Package name.
    :param version: Package version.
    :type version: :class:`Version`

    """
    def __init__(self, name, version):
        #: Package name
        self.name = name
        #: Package version
        self.version = version

    def __hash__(self):
        return hash(self.name) ^ hash(self.version)

    @classmethod
    def parse(cls, package_string):
        """Parses a ``package_string``.

        :param str package_string: Package string expression.
        :rtype: :class:`Package`

        """
        parts = re.split('\s+', package_string, 1)
        if len(parts) != 2:
            raise InvalidPackage(package_string)
        name, version_str = parts
        version = Version.parse(version_str)
        return Package(name, version)
