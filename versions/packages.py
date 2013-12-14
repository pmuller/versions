import re

from .requirements import Requirement
from .version import Version
from .errors import Error


RE = re.compile(r"""
^
\s*
(?P<name>[A-Za-z0-9_\-]+)
\s*
-
\s*
(?P<version>
    # major version number
    \d+
    (?:
        \.
        # minor version number
        \d+
        (?:
            \.
            # patch version number
            \d+
        )?
    )?
    (?:
        -
        # pre-release version number
        [0-9a-zA-Z.-]*
    )?
    (?:
        \+
        # build metadata
        [0-9a-zA-Z.-]*
    )?
)
\s*
$
""", re.X)


class InvalidPackageExpression(Error):
    """Raised failing to parse a package expression.
    """
    def __init__(self, expression):
        self.expression = expression
        message = 'Invalid package expression: %s' % expression
        super(InvalidPackageExpression, self).__init__(message)


class InvalidPackageInfo(Error):
    """Raised failing to parse a package expression info.
    """
    def __init__(self, info):
        self.info = info
        message = 'Invalid package expression info: %s' % info
        super(InvalidPackageInfo, self).__init__(message)


class Package(object):
    """A package.

    :param str name: Package name.
    :param version: Package version.
    :type version: :class:`Version`

    """
    def __init__(self, name, version, dependencies=None):
        #: Package name.
        self.name = name
        #: Package version.
        self.version = version
        #: ``set`` of :class:`Requirement` objects
        self.dependencies = dependencies or set()

    def __hash__(self):
        return hash(self.name) ^ hash(self.version)

    @classmethod
    def parse(self, package_expression):
        """Parse a ``package_expression`` into a :class:`Package` object.
        """
        parts = re.split(r'\s*;\s*', package_expression)
        name_ver_str = parts[0]
        infos = parts[1:]
        dependencies = set()

        name_ver_match = RE.match(name_ver_str)
        if not name_ver_match:
            raise InvalidPackageExpression(name_ver_str)

        name, version_str = name_ver_match.groups()
        version = Version.parse(version_str)

        for info in infos:
            if info.startswith('depends '):
                dependency_str = info.split(' ', 1)[1]
                dependency = Requirement.parse(dependency_str)
                dependencies.add(dependency)
            else:
                raise InvalidPackageInfo(info)

        return Package(name, version, dependencies)
