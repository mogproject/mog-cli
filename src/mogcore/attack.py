import cmogcore
from .atomiccsatype import AtomicCsaType


class Attack(cmogcore.Attack):
    @staticmethod
    def get_attack(*args):
        return cmogcore.Attack.get_attack(*[Attack.unwrap(x) for x in args])

    @staticmethod
    def unwrap(x):
        if isinstance(x, AtomicCsaType):
            return x.value
        return x
