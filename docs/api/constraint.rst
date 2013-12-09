constraint
----------

Examples::

    >>> from versions import Constraint
    >>> Constraint.parse('>1').match('2')
    True
    >>> Constraint.parse('<2').match(Version.parse('1'))
    True
    >>> '1.5' in Constraint.parse('== 1.0')
    False
    >>> '1.5' in Constraint.parse('> 1.0')
    True


Constraint
==========

.. autoclass:: versions.constraint.Constraint
    :members: operator, version, match, parse
    :member-order: bysource

InvalidConstraint
=================

.. autoexception:: versions.constraint.InvalidConstraint
    :members:
