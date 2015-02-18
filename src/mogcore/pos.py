from .atomiccsatype import AtomicCsaType


class Pos(AtomicCsaType):
    table = ['%d%d' % (i % 9 + 1, i // 9 + 1) for i in range(81)] + ['00']

    def __init__(self, value):
        super(Pos, self).__init__(value)
        self.file = None if value < 0 else value % 9 + 1
        self.rank = None if value < 0 else value // 9 + 1

(
    P11, P21, P31, P41, P51, P61, P71, P81, P91,
    P12, P22, P32, P42, P52, P62, P72, P82, P92,
    P13, P23, P33, P43, P53, P63, P73, P83, P93,
    P14, P24, P34, P44, P54, P64, P74, P84, P94,
    P15, P25, P35, P45, P55, P65, P75, P85, P95,
    P16, P26, P36, P46, P56, P66, P76, P86, P96,
    P17, P27, P37, P47, P57, P67, P77, P87, P97,
    P18, P28, P38, P48, P58, P68, P78, P88, P98,
    P19, P29, P39, P49, P59, P69, P79, P89, P99,
    HAND
) = (Pos(i) for i in range(82))
