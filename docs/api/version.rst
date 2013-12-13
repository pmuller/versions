version
-------


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
    The build metadata are ignored


Parsing
+++++++

:class:`Version` has a convenient `parse` static method to parse
constrints strings into :class:`Version` objects.

The parser does its best to normalize the passed in string into a
`Semantic Version 2.0 <http://semver.org/spec/v2.0.0.html>`_ version::

    >>> from versions import Version
    >>> Version.parse('1')
    Version.parse('1.0.0')
    >>> Version.parse('1.0')
    Version.parse('1.0.0')
    >>> Version.parse('1.0.0')
    Version.parse('1.0.0')
    >>> Version.parse('1.0.0-dev')
    Version.parse('1.0.0-dev')
    >>> Version.parse('1.0.0+some.build.data')
    Version.parse('1.0.0+build.data.some')
    >>> Version.parse('1.0.0-alpha+some.build.data')
    Version.parse('1.0.0-alpha+build.data.some')
    >>> Version.parse('1.0.0-42')
    Version.parse('1.0.0-42')

When parsing fails, an `InvalidVersion` exception is raised:

.. autoexception:: versions.version.InvalidVersion
    :members:
