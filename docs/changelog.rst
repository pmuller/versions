=========
Changelog
=========

* :support:`0` Renamed exceptions.
* :support:`0` Improved all docs!
* :feature:`0` Added :class:`~versions.repositories.Pool`.
* :feature:`0` Added :class:`~versions.repositories.Repository`.
* :release:`0.6.0 <2013-12-14>`
* :feature:`0` Completed implementation of :class:`~versions.requirements.Requirement`.
* :feature:`0` :class:`~versions.constraint.Constraint` now supports merging with
  :class:`~versions.constraint.Constraint` or
  :class:`~versions.constraints.Constraints` objects using the ``+`` operator.
* :support:`0` More documentation for :mod:`~versions.packages`.
* :release:`0.5.0 <2013-12-13>`
* :support:`0` Base implementation of :class:`~versions.requirements.Requirement`.
* :release:`0.4.0 <2013-12-13>`
* :feature:`0` Added :class:`~versions.packages.Package`.
* :release:`0.3.0 <2013-12-10>`
* :bug:`0` Fixed :meth:`~versions.constraints.Constraints.parse`:
  it was not merged containts after parsing.
* :support:`0` Simplified `versions.version.Version.__cmp__` for readability.
* :support:`0` Wrote more docs on constraints.
* :release:`0.2.0 <2013-12-09>`
* :feature:`0` Base implementation of :class:`~versions.version.Version`,
  :class:`~versions.constraint.Constraint` and
  :class:`~versions.constraints.Constraints`.
