import re

from .version import Version
from .operators import Operator
from .errors import Error


# Regular expression used to parse version constraints
RE = re.compile("""
^
\s*
(?P<operator>==|!=|\<|\>|\<=|\>=)
\s*
(?P<version>[0-9A-Za-z_\-\.\+]+)
\s*
$
""", re.X)


class InvalidConstraint(Error):
    """Raised when failing to parse a ``constraint``.
    """
    def __init__(self, constraint):
        #: The bogus constraint.
        self.constraint = constraint
        message = 'Invalid constraint: %r' % constraint
        super(InvalidConstraint, self).__init__(message)


class Constraint(object):
    """A constraint on a package version.

    :param operator: The constraint operator.
    :type operator: :class:`Operator`
    :param version: The constraint version.
    :type version: :class:`Version`
    """
    def __init__(self, operator, version):
        #: The constraint :class:`Operator`.
        self.operator = operator
        #: The constraint :class:`Version`.
        self.version = version

    def __str__(self):
        return str(self.operator) + str(self.version)

    def __repr__(self):
        return 'Constraint.parse(%r)' % str(self)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.operator) ^ hash(self.version)

    def __add__(self, other):
        from .constraints import Constraints
        return Constraints([self]) + other

    def match(self, version):
        """Match ``version`` with the contraint.

        :param version: Version to match against the constraint.
        :type version: version string or :class:`Version`
        :rtype: ``True`` if ``version`` satisfies the constraint, \
        ``False`` if it doesn't.
        """
        if isinstance(version, str):
            version = Version.parse(version)
        return self.operator(version, self.version)
    __contains__ = match

    @classmethod
    def parse(cls, constraint_string):
        """Parses a ``constraint`` string and returns a \
        :class:`Constraint` object.

        :raises: :exc:`InvalidConstraint` when parsing fails.
        """
        match = RE.match(constraint_string)

        if match:
            operator_str, version_str = match.groups()
            operator = Operator.parse(operator_str)
            version = Version.parse(version_str)
            return cls(operator, version)

        else:
            raise InvalidConstraint(constraint_string)
