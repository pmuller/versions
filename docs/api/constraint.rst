constraint
----------

The ``constraint`` module defines the :class:`Constraint` class which matches
:class:`Version` objects (and parsable version strings).

Examples::

    >>> from versions import Constraint, Version
    >>> Constraint.parse('>1').match('2')
    True
    >>> Constraint.parse('<2').match(Version.parse('1'))
    True
    >>> '1.5' in Constraint.parse('== 1.0')
    False
    >>> Version(1, 5) in Constraint.parse('> 1.0')
    True
    >>> Version(1) in Constraint.parse('>= 2.0.0, < 3.0.0')
    False


Constraint strings
==================

:class:`Constraint` has a convenient `parse` static method to parse
constrints strings into :class:`Constraint` objects.

Constraint strings are composed of a constraint operator (see next section),
followed by a valid version string.

Constraint operators
++++++++++++++++++++

Valid operators:
``==``, ``!=``, ``<``, ``>``, ``<=`` and ``>=``.


Constraint
==========

.. autoclass:: versions.constraint.Constraint
    :members: operator, version, match, parse
    :member-order: bysource

InvalidConstraint
=================

.. autoexception:: versions.constraint.InvalidConstraint
    :members:
