version
-------

:class:`Version` objects are comparable with standard operators::

    >>> from versions import Version
    >>> v1 = Version(1)
    >>> v2 = Version.parse('2')
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


Version
=======

.. autoclass:: versions.version.Version
    :members: major, minor, prerelease, build_metadata, parse
    :member-order: bysource

InvalidVersion
==============

.. autoexception:: versions.version.InvalidVersion
    :members:
