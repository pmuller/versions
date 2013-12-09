versions is a Python library for software version comparison
------------------------------------------------------------

Quick examples:

* Compare versions::

    >>> from versions import Version
    >>> Version.parse('2.0.0') > Version.parse('1.0.0')
    True

* Test if constraints are satisfied by a version::

    >>> from versions import Constraint, Constraints
    >>> '2.0' in Constraint.parse('>1')
    True
    >>> '1.5' in Constraints.parse('>1,<2')
    True


Contents
========

.. toctree::
   :maxdepth: 4

   quickstart
   api/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
