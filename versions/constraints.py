import re
from collections import defaultdict

from .constraint import Constraint
from .operators import eq, lt, gt, le, ge
from .errors import Error


class ExclusiveConstraints(Error):
    """Raised when cannot merge a new constraint with pre-existing
    constraints.
    """
    def __init__(self, constraint, constraints):
        self.constraint = constraint
        self.constraints = constraints
        self.message = 'Constraint %s conflicts with constraints %s' % (
            constraint, ', '.join(str(c) for c in constraints))


class Constraints(object):
    """A collection of :class:`Contraint` objects.
    """
    def __init__(self, constraints=None):
        #: List of :class:`Constraint`.
        self.constraints = list(constraints) if constraints else []

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(tuple(self.constraints))

    def match(self, version):
        """Match ``version`` with this collection of constraints.

        :param version: Version to match against this collection of \
        constraints.
        :type version: version string or :class:`Version`
        :rtype: ``True`` if ``version`` satisfies this collection of \
        constraint, ``False`` if it doesn't.
        """
        return all(constraint.match(version)
                   for constraint in self.constraints)
    __contains__ = match

    def __str__(self):
        return ','.join(str(constraint) for constraint in self.constraints)

    def __repr__(self):
        if self.constraints:
            return 'Constraints.parse(%r)' % str(self)
        else:
            return 'Constraints()'

    def __iadd__(self, constraint):
        """Add a new constraint to this collection of constraints.

        Example::

            >>> constraints = Constraints()
            >>> constraints += '>1'
            >>> constraints
            Constraints.parse('>1.0.0')
            >>> constraints += '<2'
            >>> constraints
            Constraints.parse('>1.0.0,<2.0.0')

        """
        self.constraints = merge(self.constraints, constraint)
        return self

    def __add__(self, constraint):
        """Returns a new constraint collection, resulting in the merge of 
        this collection with ``constraint``.

        Example::

            >>> constraints = Constraints()
            >>> constraints
            Constraints()
            >>> constraints + '>1'
            Constraints.parse('>1.0.0')
            >>> constraints + '>1' + '<2'
            Constraints.parse('>1.0.0,<2.0.0')

        """
        return Constraints(merge(self.constraints, constraint))

    @classmethod
    def parse(cls, constraints_string):
        """Parses a ``constraints_string`` and returns a
        :class:`Constraints` object.
        """
        constraint_strings = re.split(r'\s*,\s*', constraints_string)
        return Constraints(Constraint.parse(constraint_str)
                           for constraint_str in constraint_strings)


def merge(constraints, new_constraint):
    """Merge a ``new_constraint`` into ``constraints``.

    :param constraints: Current constraints.
    :type constraints: Iterable of :class:`Constraint` objects.
    :param new_constraint: New contraint to merge with current constraints.
    :type new_constraint: string or :class:`Constraint`
    :rtype: ``list`` of :class:`Constraint` objects.
    :raises: :exc:`ExclusiveConstraints`

    """
    # Parse string constraints.
    if isinstance(new_constraint, str):
        new_constraint = Constraint.parse(new_constraint)
    # Merge is easy if there are no previous constraint
    if not constraints:
        return [new_constraint]
    elif new_constraint.operator == eq:
        raise ExclusiveConstraints(new_constraint, constraints)
    # Dictionary :class:`Operator`: set of :class:`Version`.
    operators = defaultdict(set)
    for constraint in constraints:
        operators[constraint.operator].add(constraint.version)
    # Add the new constraint
    operators[new_constraint.operator].add(new_constraint.version)
    # Get most recent version required by > constraints.
    if gt in operators:
        gt_ver = sorted(operators[gt])[-1]
    else:
        gt_ver = None
    # Get most recent version required by >= constraints.
    if ge in operators:
        ge_ver = sorted(operators[ge])[-1]
    else:
        ge_ver = None
    # Get least recent version required by < constraints.
    if lt in operators:
        lt_ver = sorted(operators[lt])[0]
    else:
        lt_ver = None
    # Get least recent version required by <= constraints.
    if le in operators:
        le_ver = sorted(operators[le])[0]
    else:
        le_ver = None
    # Most restrictive LT/LE constraint.
    l_constraint = None
    if le_ver:
        if lt_ver:
            if le_ver < lt_ver:
                # <= 1, < 2
                l_constraint = Constraint(le, le_ver)
            else:
                # <= 2, < 1
                # <= 2, < 2
                l_constraint = Constraint(lt, lt_ver)
        else:
            l_constraint = Constraint(le, le_ver)
    elif lt_ver:
        l_constraint = Constraint(lt, lt_ver)
    # Most restrictive GT/GE constraint.
    g_constraint = None
    if ge_ver:
        if gt_ver:
            if ge_ver <= gt_ver:
                # >= 1, > 2
                # >= 2, > 2
                g_constraint = Constraint(gt, gt_ver)
            else:
                # >= 2, > 1
                g_constraint = Constraint(ge, ge_ver)
        else:
            g_constraint = Constraint(ge, ge_ver)
    elif gt_ver:
        g_constraint = Constraint(gt, gt_ver)

    eq_constraint = None

    # Check if g_constraint and l_constraint are conflicting
    if g_constraint and l_constraint:
        if g_constraint.version == l_constraint.version:
            if g_constraint.operator == ge and l_constraint.operator == le:
                # Merge >= and <= constraints on same version to a ==
                # constraint
                eq_constraint = Constraint(eq, g_constraint.version)
            else:
                raise ExclusiveConstraints(g_constraint, [l_constraint])
        elif g_constraint.version > l_constraint.version:
            raise ExclusiveConstraints(g_constraint, [l_constraint])

    if eq_constraint:
        return [eq_constraint]

    else:
        result = []

        if g_constraint:
            result.append(g_constraint)
        if l_constraint:
            result.append(l_constraint)

        return result
