packages
--------


Package
=======

.. autoclass:: versions.packages.Package
    :members:
    :member-order: bysource

Parsing
+++++++

:class:`Package` can be represented as strings using this EBNF grammar::

    package             ::= name version build_metadata_spec?
    version             ::= [-A-Za-z0-9_.]+
    build_metadata_spec ::= '+' [-A-Za-z0-9_.]+

Examples:
* ``foo 1.0.0``
* ``bar 1.0.0+some.build.options``

A package string can be parsed into a :class:`Package` object Using
`Package.parse`::

    >>> from versions import Package
    >>> package = Package.parse('foo 1.0.0+bar')
    >>> package.name, package.version
    ('foo', Version.parse('1.0.0+bar'))
