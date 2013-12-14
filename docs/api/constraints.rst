constraints
-----------

.. py:module:: versions.constraints

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

.. note:: The :class:`Constraints` object must be on the left side of the ``+`` operator.
    The :class:`Constraint` object must be on right side.

If the constraint is a string, it is automatically parsed into a
:class:`Constraint` object.
So the previous example can be shortened as::

    >>> Constraints() + '<2' + '!=1.5'
    Constraints.parse('<2.0.0,!=1.5.0')

Matching
++++++++

:class:`Constraints` objects work like :class:`Constraint` objects: they have
a :meth:`Contraints.match` method which returns ``True`` when passed a
:class:`Version` matching all constraints::

    >>> Constraints.parse('>=1,<2').match('1.4')
    True
    >>> '1.4' in Constraints.parse('>=1.2,<2,!=1.4')
    False

Conflicts
=========

When merging conflicting constraints, an :exc:`ExclusiveConstraints`
exception is raised::

    >>> Constraints.parse('<1') + '>1'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/pmuller/dev/versions/versions/constraints.py", line 102, in __add__
        return Constraints(merge(self.constraints + [constraint]))
      File "/Users/pmuller/dev/versions/versions/constraints.py", line 209, in merge
        raise ExclusiveConstraints(g_constraint, [l_constraint])
    versions.constraints.ExclusiveConstraints: Constraint >1.0.0 conflicts with constraints <1.0.0

    >>> Constraints.parse('<1') + '==1'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/pmuller/dev/versions/versions/constraints.py", line 102, in __add__
        return Constraints(merge(self.constraints + [constraint]))
      File "/Users/pmuller/dev/versions/versions/constraints.py", line 223, in merge
        raise ExclusiveConstraints(eq_constraint, conflict_list)
    versions.constraints.ExclusiveConstraints: Constraint ==1.0.0 conflicts with constraints <1.0.0

    >>> Constraints.parse('>=1') + '!=1' + '<=1'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/pmuller/dev/versions/versions/constraints.py", line 102, in __add__
        return Constraints(merge(self.constraints + [constraint]))
      File "/Users/pmuller/dev/versions/versions/constraints.py", line 223, in merge
        raise ExclusiveConstraints(eq_constraint, conflict_list)
    versions.constraints.ExclusiveConstraints: Constraint ==1.0.0 conflicts with constraints !=1.0.0


.. autoexception:: versions.constraints.ExclusiveConstraints
    :members:
