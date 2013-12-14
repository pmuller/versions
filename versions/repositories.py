from .requirements import Requirement


class Repository(object):
    """A package repository.
    
    :param packages: Repository packages.
    :type packages: :func:`set` of :class:`~versions.packages.Package`, \
    or `None`

    """
    def __init__(self, packages=None):
        #: :func:`set` of :class:`~versions.packages.Package` objects.
        self.packages = packages or set()

    def get(self, requirement):
        """Find packages matching ``requirement``.

        :param requirement: Requirement to match against repository packages.
        :type requirement: `str` or :class:`~versions.requirements.Requirement`
        :returns: `list` of matching :class:`~versions.packages.Package` \
        objects.

        """
        if isinstance(requirement, str):
            requirement = Requirement.parse(requirement)
        return sorted(p for p in self.packages
                      if requirement.name == p.name and requirement.match(p))
