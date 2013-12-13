import re

from .errors import Error
from .constraints import Constraints


class InvalidRequirement(Error):
    """Raised when failing to parse a requirement expression.
    """
    def __init__(self, requirement):
        #: The bogus requirement expression
        self.requirement = requirement
        message = 'Invalid requirement: %s' % requirement
        super(InvalidRequirement, self).__init__(message)


# Regular expression user to parse package requirements.
RE = re.compile("""
^
\s*
(?P<name>[A-Za-z0-9_\-]+)
\s*
(?:
    \[
    \s*
    (?P<build_metadata>[A-Za-z0-9_\-, ]+)
    \s*
    \]
)?
\s*
(?P<version_constraints>[A-Za-z0-9_\-,!=\>\<\. ]+)*
\s*
$
""", re.X)


class Requirement(object):
    """Package requirements are used to define a dependency from a
    :class:`Package` to another.

    :param str name: The required package name.
    :param version_constraints: Constraints on the package version.
    :type version_constraints: :class:`Version` or ``None``
    :param build_options: Required build options.
    :type build_options: ``set`` of ``str`` or ``None``
    
    """
    def __init__(self, name, version_constraints=None, build_options=None):
        #: Name of the required package.
        self.name = name
        #: :class:`Constraints` on the required package version.
        self.version_constraints = version_constraints
        #: `set` of required build options
        self.build_options = build_options

    @classmethod
    def parse(cls, requirement_string):
        """Parses a ``requirement_string`` into a :class:`Requirement` object.

        :param str requirement_string: A package requirement expression.
        :rtype: :class:`Requirement`

        """
        match = RE.match(requirement_string)

        if match:
            name, build_metadata, version_constraints_str = match.groups()

            if version_constraints_str:
                version_constraints = \
                    Constraints.parse(version_constraints_str)
            else:
                version_constraints = None

            if build_metadata:
                build_options = \
                    set(o.strip() for o in build_metadata.split(','))
            else:
                build_options = None

            return cls(name, version_constraints, build_options)

        else:
            raise InvalidRequirement(requirement_string)
