class Package(object):
    """A package.

    :param str name: Package name.
    :param version: Package version.
    :type version: :class:`Version`

    """
    def __init__(self, name, version):
        #: Package name
        self.name = name
        #: Package version
        self.version = version

    def __hash__(self):
        return hash(self.name) ^ hash(self.version)
