from .requirements import Requirement


class Repository(object):
    """A package repository.
    
    :param packages: Repository packages.
    :type packages: :func:`set` of :class:`.Package` or `None`

    """
    def __init__(self, packages=None):
        #: :func:`set` of :class:`~versions.packages.Package` objects.
        self.packages = packages or set()

    def get(self, requirement):
        """Find packages matching ``requirement``.

        :param requirement: Requirement to match against repository packages.
        :type requirement: `str` or :class:`.Requirement`
        :returns: :func:`list` of matching :class:`.Package` objects.

        """
        if isinstance(requirement, str):
            requirement = Requirement.parse(requirement)
        return sorted(p for p in self.packages
                      if requirement.name == p.name and requirement.match(p))


class Pool(object):
    """A package repository pool.

    When querying a repository pool, it queries all repositories, and merges
    their results.

    :param repositories: Underlying package repositories.
    :type repositories: :func:`list` of :class:`Repository` or ``None``

    """
    def __init__(self, repositories=None):
        #: :func:`list` of :class:`Repository <repositories>`
        self.repositories = repositories or []

    def get(self, requirement):
        """Find packages matching ``requirement``.

        :param requirement: Requirement to get from all underlying \
        repositories.
        :type requirement: `str` or :class:`.Requirement`
        :returns: :func:`list` of matching :class:`.Package` objects.

        """
        if isinstance(requirement, str):
            requirement = Requirement.parse(requirement)
        packages = set()
        for repository in self.repositories:
            packages |= set(repository.get(requirement))
        return sorted(packages)
