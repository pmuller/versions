import re
import logging
from collections import defaultdict

from .constraint import Constraint
from .operators import eq, lt, gt, le, ge, ne
from .errors import Error


LOGGER = logging.getLogger(__name__)


class ExclusiveConstraints(Error):
    """Raised when cannot merge a new constraint with pre-existing
    constraints.
    """
    def __init__(self, constraint, constraints):
        #: The conflicting constraint.
        self.constraint = constraint
        #: The constraints with which it conflicts.
        self.constraints = constraints
        message = 'Constraint %s conflicts with constraints %s' % (
            constraint, ', '.join(str(c) for c in constraints))
        super(ExclusiveConstraints, self).__init__(message)


class Constraints(object):
    """A collection of :class:`Constraint` objects.
    """
    def __init__(self, constraints=None):
        #: List of :class:`Constraint`.
        self.constraints = list(constraints) if constraints else []

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                other = Constraints.parse(other)
            except Error:
                return False
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

    def _merge(self, constraint):
        """Wrapper for :func:`merge`.

        It merges `constraint` with current ones and returns the list of
        merged constraints.
        It does not modify the current object.

        :param constraint: The constraint(s) to merge with current constraints.
        :type: :class:`Constraint`, :class:`Constraints` or `str`
        :returns: List of :class:`Constraint` objects.
        :rtype: list

        """
        if isinstance(constraint, str):
            constraints = [Constraint.parse(constraint)]
        elif isinstance(constraint, Constraint):
            constraints = [constraint]
        elif isinstance(constraint, Constraints):
            constraints = constraint.constraints
        else:
            raise TypeError(constraint)

        return merge(self.constraints + constraints)

    def __iadd__(self, constraint):
        self.constraints = self._merge(constraint)
        return self

    def __add__(self, constraint):
        return Constraints(self._merge(constraint))

    @classmethod
    def parse(cls, constraints_string):
        """Parses a ``constraints_string`` and returns a
        :class:`Constraints` object.
        """
        constraint_strings = re.split(r'\s*,\s*', constraints_string)
        return Constraints(merge(Constraint.parse(constraint_str)
                                 for constraint_str in constraint_strings))


def merge(constraints):
    """Merge ``constraints``.

    It removes dupplicate, pruned and merged constraints.

    :param constraints: Current constraints.
    :type constraints: Iterable of :class:`Constraint` objects.
    :rtype: ``list`` of :class:`Constraint` objects.
    :raises: :exc:`ExclusiveConstraints`

    """
    # Dictionary :class:`Operator`: set of :class:`Version`.
    operators = defaultdict(set)
    for constraint in constraints:
        LOGGER.debug('%r %r',type(constraint),constraint)
        operators[constraint.operator].add(constraint.version)
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
            le_constraint = Constraint(le, le_ver)
            lt_constraint = Constraint(lt, lt_ver)

            if le_ver < lt_ver:
                # <= 1, < 2
                l_constraint = le_constraint
                l_less_restrictive_c = lt_constraint
            else:
                # <= 2, < 1
                # <= 2, < 2
                l_constraint = lt_constraint
                l_less_restrictive_c = le_constraint

            LOGGER.debug('Removed constraint %s because it is less '
                         'restrictive than %s', l_less_restrictive_c,
                         l_constraint)
        else:
            l_constraint = Constraint(le, le_ver)
    elif lt_ver:
        l_constraint = Constraint(lt, lt_ver)
    # Most restrictive GT/GE constraint.
    g_constraint = None
    if ge_ver:
        if gt_ver:
            gt_constraint = Constraint(gt, gt_ver)
            ge_constraint = Constraint(ge, ge_ver)

            if ge_ver <= gt_ver:
                # >= 1, > 2
                # >= 2, > 2
                g_constraint = gt_constraint
                g_less_restrictive_c = ge_constraint
            else:
                # >= 2, > 1
                g_constraint = ge_constraint
                g_less_restrictive_c = gt_constraint

            LOGGER.debug('Removed constraint %s because it is less '
                         'restrictive than %s', g_less_restrictive_c,
                         g_constraint)
        else:
            g_constraint = Constraint(ge, ge_ver)
    elif gt_ver:
        g_constraint = Constraint(gt, gt_ver)

    # Check if g_constraint and l_constraint are conflicting
    if g_constraint and l_constraint:
        if g_constraint.version == l_constraint.version:
            if g_constraint.operator == ge and l_constraint.operator == le:
                # Merge >= and <= constraints on same version to a ==
                # constraint
                operators[eq].add(g_constraint.version)
                LOGGER.debug('Merged constraints: %s and %s into ==%s',
                             l_constraint, g_constraint, g_constraint.version)
                l_constraint, g_constraint = None, None
            else:
                raise ExclusiveConstraints(g_constraint, [l_constraint])
        elif g_constraint.version > l_constraint.version:
            raise ExclusiveConstraints(g_constraint, [l_constraint])

    ne_constraints = [Constraint(ne, v) for v in operators[ne]]
    eq_constraints = [Constraint(eq, v) for v in operators[eq]]

    if eq_constraints:
        eq_constraint = eq_constraints.pop()
        # An eq constraint conflicts with other constraints
        if g_constraint or l_constraint or ne_constraints or eq_constraints:
            conflict_list = [c for c in (g_constraint, l_constraint) if c]
            conflict_list.extend(ne_constraints)
            conflict_list.extend(eq_constraints)
            raise ExclusiveConstraints(eq_constraint, conflict_list)

        return [eq_constraint]

    else:
        constraints = ne_constraints + [g_constraint, l_constraint]
        return [c for c in constraints if c]
