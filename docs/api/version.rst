version
-------

.. py:module:: versions.version

.. _version-expressions:

Version expressions
===================

Version expressions are strings representing a software version.
They are defined by this EBNF grammar:

.. productionlist::
    version_expression: main | main '-' prerelease | main '+' build_metadata | main '-' prerelease '+' build_metadata
    main: major ('.' minor ('.' patch)?)? postrelease?
    major: number
    minor: number
    patch: number
    postrelease: string
    prerelease: string | number
    build_metadata: string
    number: [0-9]+
    string: [0-9a-zA-Z.-]+

They can be parsed into :class:`Version` objects using the
:meth:`Version.parse` class method.

Omitted parts in an expression use these defaults:

==================  =============
Part                Default value
==================  =============
``minor``           0
``patch``           0
``postrelease``     ``None``
``prerelease``      ``None``
``build_metadata``  ``None``
==================  =============

Examples of valid version expressions::

    >>> from versions import Version
    >>> v = Version.parse('1')
    >>> v == '1.0'
    True
    >>> v == '1.0.0'
    True
    >>> v.major, v.minor, v.patch, v.prerelease, v.build_metadata
    (1, 0, 0, None, None)

    >>> v = Version.parse('1.2.3-dev+foo')
    >>> v.major, v.minor, v.patch, v.prerelease, v.build_metadata
    (1, 2, 3, 'dev', 'foo')

When parsing fails, an :exc:`.InvalidVersionExpression` exception is raised::

    >>> Version.parse('#@!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "versions/version.py", line 119, in parse
        raise InvalidVersionExpression(version_string)
    versions.version.InvalidVersionExpression: Invalid version expression: '#@!'


Version
=======

.. autoclass:: versions.version.Version
    :members: major, minor, prerelease, build_metadata, parse
    :member-order: bysource

Comparison
++++++++++

:class:`Version` objects are comparable with standard operators::

    >>> from versions import Version
    >>> v1 = Version(1)
    >>> v2 = Version(2)
    >>> v1 == v2
    False
    >>> v1 != v2
    True
    >>> v1 > v2
    False
    >>> v1 < v2
    True
    >>> v1 >= v2
    False
    >>> v1 <= v2
    True

.. hint:: When comparing 2 versions, only the version and the pre-release are
    used.
    The build metadata are ignored.

Errors
++++++

.. autoexception:: versions.version.InvalidVersionExpression
    :members:
