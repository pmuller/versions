requirements
------------

.. py:module:: versions.requirements

.. _requirement-expressions:

Requirement expressions
=======================

Requirement expressions are strings representing a required software package.
They are defined by this EBNF grammar:

.. productionlist::
    requirement_expression: name build_options? constraints_expression?
    name: [A-Za-z0-9][-A-Za-z0-9]*
    build_options: '[' name (',' name)* ']'
    constraints_expression: constraint_expression (',' constraint_expression)*
    constraint_expression: operator version_expression
    operator: '==' | '!=' | '>' | '<' | '<=' | '>='
    version_expression: main | main '-' prerelease | main '+' build_metadata | main '-' prerelease '+' build_metadata
    main: major ('.' minor ('.' patch)?)?
    major: number
    minor: number
    patch: number
    prerelease: string | number
    build_metadata: string
    number: [0-9]+
    string: [0-9a-zA-Z.-]+

The :meth:`Requirement.parse` class method parses requirement expressions into
:class:`Requirement` objects::

    >>> from versions import Requirement
    >>> r = Requirement.parse('foo')
    >>> r.name
    'foo'
    >>> r = Requirement.parse('foo >1.0, <2.0')
    >>> r.version_constraints
    Constraints.parse('>1.0.0,<2.0.0')
    >>> r = Requirement.parse('vim [python, perl] >7')
    >>> r.build_options
    set(['python', 'perl'])


Matching
========

The :meth:`Requirement.match` method returns ``True`` when passed a package
which satisfies the requirement::

    >>> from versions import Requirement, Package, Version
    >>> Requirement('foo').match(Package('foo', Version.parse('1.0')))
    True

If passed a ``str``, it is automatically parsed using
:meth:`.Package.parse`::

    >>> Requirement.parse('foo [baz, bar] >0.9').match('foo-1.0+bar.baz')
    True

Matching can also be tested using the ``in`` operator::

    >>> 'foo-0.2' in Requirement.parse('foo [bar] >0.9')
    False


Requirement
===========

.. autoclass:: Requirement
    :members:
    :member-order: bysource
