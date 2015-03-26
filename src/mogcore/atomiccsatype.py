from abc import ABCMeta, abstractmethod
from util import CaseClass


class AtomicCsaType(CaseClass):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def table(self):
        """list of values"""

    def __init__(self, value):
        assert (isinstance(value, int))
        assert (0 <= value < len(self.table))
        assert (self.table[value] is not None)

        super(AtomicCsaType, self).__init__(value=value)
        self.__class__.table_inv = dict((v, k) for (k, v) in enumerate(self.table) if v is not None)

    def __str__(self):
        return self.table[self.value]

    @classmethod
    def from_string(cls, s):
        """Find index of the given string. If there is no matching index, raise ValueError."""
        index = cls.table_inv.get(s)
        if index is None:
            raise ValueError('Mal-formed CSA string for %s: %s' % (cls.__name__, s))
        return cls(index)
