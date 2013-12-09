constraints
-----------

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


Constraints
===========

.. autoclass:: versions.constraints.Constraints
    :members: constraints, match, parse
    :member-order: bysource


ExclusiveConstraints
====================

.. autoexception:: versions.constraints.ExclusiveConstraints
    :members:
