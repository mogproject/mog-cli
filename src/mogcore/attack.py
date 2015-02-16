import cmogcore
from mogcore import Turn


class Attack(cmogcore.Attack):
    @staticmethod
    def get_attack(*args):
        return cmogcore.Attack.get_attack(*[Attack.unwrap(x) for x in args])

    @staticmethod
    def unwrap(x):
        for t in [Turn]:
            if isinstance(x, t):  # TODO: refactor after implement of CsaType
                return x.value
        return x
