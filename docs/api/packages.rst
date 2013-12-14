packages
--------

.. py:module:: versions.packages

:class:`Package` objects are used to define a package.

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
