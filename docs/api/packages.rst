packages
--------

.. py:module:: versions.packages

.. _package-expressions:

Package expressions
===================

Package expressions are strings representing a software package.
They are defined by this EBNF grammar:

.. productionlist::
    package_expression: name '-' version_expression dependency*
    name: [A-Za-z0-9][-A-Za-z0-9]*
    dependency: ';' 'depends' requirement_expression
    requirement_expression: name build_options? constraints_expression?
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

The :meth:`Package.parse` class method parses package expressions into
corresponding :class:`Package` objects::

    >>> from versions import Package
    >>> p = Package.parse('foo-1.0')
    >>> p.name
    'foo'
    >>> p.version
    Version.parse('1.0.0')

Dependencies can also be specified in a package expression::

    >>> package = Package.parse('foo-1.0; depends bar; depends baz >1, <2')
    >>> package.dependencies
    set([Requirement.parse('baz>1.0.0,<2.0.0'), Requirement.parse('bar')])


.. autoclass:: Package
    :members:
    :member-order: bysource
