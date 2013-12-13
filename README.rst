.. image:: https://secure.travis-ci.org/pmuller/versions.png?branch=master
        :target: https://travis-ci.org/pmuller/versions

versions is a Python library to parse and compare package versions.

Documentation: `versions.rtfd.org <http://versions.rtfd.org/>`_

Basic usage
-----------

Version comparisons example::

    >>> from versions import Version
    >>> v1 = Version.parse('1')
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

``Version.parse`` expects a
`Semantic Version 2.0 <http://semver.org/spec/v2.0.0.html>`_ string and 
returns a corresponding ``Version`` object::

    >>> from versions import Version
    >>> v = Version.parse('1.2.0-dev+foo.bar')
    >>> v.major, v.minor, v.patch, v.prerelease, v.build_metadata
    (1, 2, 0, 'dev', 'foo.bar')

If it isn't a semantic version string, the parser tries to normalize it::

    >>> v = Version.parse('1')
    >>> v.major, v.minor, v.patch, v.prerelease, v.build_metadata
    (1, 0, 0, None, None)


Version constraint matching
---------------------------

versions also implements version constraint parsing and evaluation::

    >>> from versions import Constraint
    >>> Constraint.parse('>1').match('2')
    True
    >>> Constraint.parse('<2').match(Version.parse('1'))
    True

For conveniance, constraint matching can be tested using the ``in`` operator::

    >>> '1.5' in Constraint.parse('<2')
    True
    >>> Version('2') in Constraint.parse('!=2')
    False

Constraints can be merged using ``Constraints``::

    >>> from versions import Constraints
    >>> '1.0' in Constraints.parse('>1,<2')
    False
    >>> '1.5' in Constraints.parse('>1,<2')
    True
    >>> '2.0' in Constraints.parse('>1,<2')
    False


.. image:: https://d2weczhvl823v0.cloudfront.net/pmuller/versions/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free
