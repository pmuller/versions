constraints
-----------

.. py:module:: versions.constraints

.. _constraints-expressions:

Constraints expressions
=======================

Constraints expressions are strings representing multiple constraints on a
software version.
They are defined by this EBNF grammar:

.. productionlist::
    constraints_expression: constraint_expression (',' constraint_expression)*
    constraint_expression: operator version_expression
    operator: '==' | '!=' | '>' | '<' | '<=' | '>='
    version_expression: main | main '-' prerelease
    main: major ('.' minor ('.' patch)?)?
    major: number
    minor: number
    patch: number
    prerelease: string | number
    build_metadata: string
    number: [0-9]+
    string: [0-9a-zA-Z.-]+

They can be parsed into :class:`Constraints` objects using the
:meth:`Constraints.parse` class method.

Examples of valid constraint expressions::

    >>> from versions import Constraints

    >>> c = Constraints.parse('==1.0')
    >>> c.constraints
    [Constraint.parse('==1.0.0')]

    >>> c = Constraints.parse('>=1.0,<2,!=1.5')
    >>> c.constraints
    [Constraint.parse('!=1.5.0'), Constraint.parse('>=1.0.0'), Constraint.parse('<2.0.0')]


Constraints
===========

.. autoclass:: versions.constraints.Constraints
    :members: constraints, match, parse
    :member-order: bysource

Merging
+++++++

:class:`Constraint` objects can be merged using a :class:`Constraints` object
and the ``+`` operator::

    >>> from versions import Constraints, Constraint
    >>> Constraints() + Constraint.parse('<2') + Constraint.parse('!=1.5')
    Constraints.parse('<2.0.0,!=1.5.0')

.. note:: The :class:`Constraints` object must be on the left side of the
    ``+`` operator.
    The :class:`Constraint` object must be on right side.

If the constraint is a :ref:`constraints expression <constraints-expressions>`,
it is automatically parsed into a :class:`Constraints` object.

The previous example can therefore be shortened as::

    >>> Constraints() + '<2' + '!=1.5'
    Constraints.parse('!=1.5.0,<2.0.0')

Or::

    >>> Constraints() + '<2,!=1.5'
    Constraints.parse('!=1.5.0,<2.0.0')


Matching
++++++++

:class:`Constraints` objects work like :class:`.Constraint` objects: they have
a :meth:`Constraints.match` method which returns ``True`` when passed a
:ref:`version expression <version-expressions>` or :class:`.Version` matching
all constraints::

    >>> Constraints.parse('>=1,<2').match('1.4')
    True
    >>> '1.4' in Constraints.parse('>=1.2,<2,!=1.4')
    False

Conflicts
=========

When merging conflicting constraints, an :exc:`.ExclusiveConstraints`
exception is raised::

    >>> Constraints.parse('<1') + '>1'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "versions/constraints.py", line 96, in __add__
        return Constraints(self._merge(constraint))
      File "versions/constraints.py", line 89, in _merge
        return merge(self.constraints + constraints)
      File "versions/constraints.py", line 203, in merge
        raise ExclusiveConstraints(g_constraint, [l_constraint])
    versions.constraints.ExclusiveConstraints: Constraint >1.0.0 conflicts with constraints <1.0.0

    >>> Constraints.parse('<1') + '==1'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "versions/constraints.py", line 96, in __add__
        return Constraints(self._merge(constraint))
      File "versions/constraints.py", line 89, in _merge
        return merge(self.constraints + constraints)
      File "versions/constraints.py", line 217, in merge
        raise ExclusiveConstraints(eq_constraint, conflict_list)
    versions.constraints.ExclusiveConstraints: Constraint ==1.0.0 conflicts with constraints <1.0.0

    >>> Constraints.parse('>=1') + '!=1' + '<=1'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "versions/constraints.py", line 96, in __add__
        return Constraints(self._merge(constraint))
      File "versions/constraints.py", line 89, in _merge
        return merge(self.constraints + constraints)
      File "versions/constraints.py", line 217, in merge
        raise ExclusiveConstraints(eq_constraint, conflict_list)
    versions.constraints.ExclusiveConstraints: Constraint ==1.0.0 conflicts with constraints !=1.0.0


.. autoexception:: versions.constraints.ExclusiveConstraints
    :members:
