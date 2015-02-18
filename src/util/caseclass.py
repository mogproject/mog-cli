class CaseClass(object):
    """
    Implementation like Scala's case class

    Usage:
      class YourClass(CaseClass):
          def __init__(self, foo, bar):
              super(YourClass, self).__init__(foo=foo, bar=bar)
    """

    def __init__(self, **params):
        """
        :param params: key-value pairs
        """
        self.__keys = params.keys()
        for k, v in params.items():
            setattr(self, k, v)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        for k in self.__keys:
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            # compare with class names
            return self.__class__.__name__ < other.__class__.__name__

        for k in self.__keys:
            a, b = getattr(self, k), getattr(other, k)
            if a < b:
                return True
            if a > b:
                return False
        return False

    def __hash__(self):
        return hash(tuple((k, getattr(self, k)) for k in self.__keys))

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join('%s=%r' % (k, getattr(self, k)) for k in self.__keys))
