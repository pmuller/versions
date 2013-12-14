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

    def __hash__(self):
        build_options_h = hash(tuple(self.build_options)
                               if self.build_options else None)
        return hash(self.name) ^ hash(self.version_constraints) ^ \
            build_options_h

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                other = Requirement.parse(other)
            except Error:
                return False
        return hash(self) == hash(other)

    def __str__(self):
        version_constraints = \
            self.version_constraints if self.version_constraints else ''
        if self.build_options:
            build_options = '[' + ','.join(sorted(self.build_options)) + ']'
        else:
            build_options = ''
        return '%s%s%s' % (self.name, build_options, version_constraints)

    def __repr__(self):
        return 'Requirement.parse(%r)' % str(self)

    def __add__(self, requirement):
        if isinstance(requirement, str):
            requirement = Requirement.parse(requirement)

        if self.name != requirement.name:
            raise InvalidRequirement(requirement)
        
        if self.version_constraints is None:
            version_constraints = requirement.version_constraints
        elif requirement.version_constraints is None:
            version_constraints = self.version_constraints
        else:
            version_constraints = \
                self.version_constraints + requirement.version_constraints

        if self.build_options is None:
            build_options = requirement.build_options
        elif requirement.build_options is None:
            build_options = self.build_options
        else:
            build_options = self.build_options | requirement.build_options

        return Requirement(self.name, version_constraints, build_options)

    def match(self, package):
        """Match ``package`` with the requirement.

        :param package: Package to test with the requirement.
        :type package: package expression string or :class:`Package`
        :returns: ``True`` if ``package`` satisfies the requirement.
        :rtype: bool

        """
        if isinstance(package, str):
            from .packages import Package
            package = Package.parse(package)

        if self.name != package.name:
            return False

        if self.version_constraints and \
                package.version not in self.version_constraints:
            return False

        if self.build_options:
            if package.version.build_metadata:
                pkg_build_opts = set(package.version.build_metadata.split('.'))
                if self.build_options - pkg_build_opts:
                    return False
                else:
                    return True
            else:
                return False
        else:
            return True
    __contains__ = match

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
