constraint
----------

.. py:module:: versions.constraint

.. _constraint-expressions:

Constraint expressions
======================

Constraint expressions are strings representing a constraint on a software
version.
They are defined by this EBNF grammar:

.. productionlist::
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

They can be parsed into :class:`Constraint` objects using the
:meth:`Constraint.parse` class method.

Examples of valid constraint expressions::

    >>> from versions import Constraint
    >>> c = Constraint.parse('==1.0')
    >>> c.operator, c.version
    (Operator.parse('=='), Version.parse('1.0.0'))
    >>> c = Constraint.parse('>=1.2.3-dev+foo')
    >>> c.operator, c.version
    (Operator.parse('>='), Version.parse('1.2.3-dev+foo'))

When parsing fails, an :exc:`.InvalidConstraintExpression` exception is
raised::

    >>> Constraint.parse('WTF')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "versions/constraint.py", line 94, in parse
        raise InvalidConstraintExpression(constraint_expression)
    versions.constraint.InvalidConstraintExpression: Invalid constraint expression: 'WTF'


Constraint
==========

.. autoclass:: versions.constraint.Constraint
    :members: operator, version, match, parse
    :member-order: bysource


Matching
++++++++

The :meth:`Constraint.match` method returns ``True`` when passed a satisfying
:ref:`version expression <version-expressions>` or :class:`.Version` object::

    >>> from versions import Constraint, Version
    >>> Constraint.parse('>1').match('2')
    True
    >>> Constraint.parse('<2').match(Version(1))
    True

Matching can also be tested using the ``in`` operator::

    >>> '1.5' in Constraint.parse('== 1.0')
    False
    >>> Version(1, 5) in Constraint.parse('> 1.0')
    True
    >>> Version(1) in Constraint.parse('>= 2.0.0')
    False


Errors
++++++

.. autoexception:: versions.constraint.InvalidConstraintExpression
    :members:
