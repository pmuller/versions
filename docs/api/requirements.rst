requirements
------------

.. py:module:: versions.requirements

:class:`Requirement` objects are used to define a requirement on a package
using constraints on its name, and optionally on its version or build options.

The :meth:`Requirement.parse` class method parses requirement strings into
:class:`Requirement` objects::

    >>> from versions import Requirement
    >>> r = Requirement.parse('foo')
    >>> r.name
    'foo'
    >>> r = Requirement.parse('foo >1.0, <2.0')
    >>> r.version_constraints
    Contraints.parse('>1.0.0,<2.0.0')
    >>> r = Requirement.parse('vim [python, perl] >7')
    >>> r.build_options
    set(['python', 'perl'])

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


.. autoclass:: Requirement
    :members:
    :member-order: bysource
