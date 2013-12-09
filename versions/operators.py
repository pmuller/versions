import operator

from .errors import Error


#: Dictionary of operator function: operator string
OP_FUNC_TO_STR = {operator.eq: '==', operator.ne: '!=', operator.gt: '>',
             operator.ge: '>=', operator.lt: '<', operator.le: '<='}
#: Dictionary of operator string: operator function
STR_TO_OP_FUNC = dict((s, op) for op, s in OP_FUNC_TO_STR.items())


class InvalidOperator(Error):
    """Raised when failing to parse an operator.
    """
    def __init__(self, operator):
        #: The bogus operator.
        self.operator = operator
        message = 'Invalid operator: %r' % operator
        super(InvalidOperator, self).__init__(message)


class Operator(object):
    """A package version constraint operator.

    :param callable func: The operator callable.
    :param str string: The operator string representation.
    """
    def __init__(self, func, string):
        #: Operator callable
        self.func = func
        #: Operator string representation
        self.string = string

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.func)

    def __call__(self, a, b):
        return self.func(a, b)

    def __str__(self):
        return self.string

    def __repr__(self):
        return 'Operator.parse(%r)' % str(self)

    @classmethod
    def parse(cls, string):
        """Parses `string` and returns an :class:`Operator`
        object.

        :raises: :exc:`InvalidOperator` If `string` is not \
        a valid operator.

        Valid operators are ``==``, ``!=``, ``<``, ``>``, ``<=``, and ``>=``.

        """
        if string in STR_TO_OP_FUNC:
            return cls(STR_TO_OP_FUNC[string], string)
        else:
            raise InvalidOperator(string)


#: == :class:`Operator`
eq = Operator(operator.eq, '==')
#: != :class:`Operator`
ne = Operator(operator.ne, '!=')
#: < :class:`Operator`
lt = Operator(operator.lt, '<')
#: <= :class:`Operator`
le = Operator(operator.le, '<=')
#: > :class:`Operator`
gt = Operator(operator.gt, '>')
#: >= :class:`Operator`
ge = Operator(operator.ge, '>=')
