constraints
-----------

:class:`Constraint` objects can be merged using :class:`Constraints`::

    >>> from versions import Constraints, Constraint
    >>> '1.0' in Constraints.parse('>1,<2')
    False
    >>> '1.5' in Constraints.parse('>1,<2')
    True
    >>> '2.0' in Constraints.parse('>1,<2')
    False
    >>> Constraints.parse('>1') + '<2' + '!=1.5'
    Constraints.parse('>1.0.0,<2.0.0,!=1.5.0')


Constraints
===========

.. autoclass:: versions.constraints.Constraints
    :members: constraints, match, parse
    :member-order: bysource


ExclusiveConstraints
====================

.. autoexception:: versions.constraints.ExclusiveConstraints
    :members:
