# import unittest
# from mogcore import *


# class TestSimpleState(unittest.TestCase):
#     def test_constructor(self):
#         s = SimpleState(0, [])
#         self.assertEqual(s.turn, 0)
#         self.assertEqual(s.pieces(), [-1] * 40)

#         s = SimpleState(0, list(range(20)))
#         self.assertEqual(s.turn, 0)
#         self.assertEqual(s.pieces(), list(range(20)) + [-1] * 20)

#         s = SimpleState(1, list(range(40)))
#         self.assertEqual(s.turn, 1)
#         self.assertEqual(s.pieces(), list(range(40)))

#     def test_eq(self):
#         s = SimpleState(0, [
#             0, 257, 2, 259, 4, 261, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337,
#             81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, -1, 81, 337,
#         ])
#         t = SimpleState(0, [
#             257, 0, 259, 2, 261, 4, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81,
#             337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, -1, 81, 337, 81, 337, 81,
#         ])
#         u = SimpleState(1, [
#             257, 0, 259, 2, 261, 4, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81,
#             337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, -1, 81, 337, 81, 337, 81,
#         ])
#         v = SimpleState(1, [
#             257, 0, 259, 2, 261, 4, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 337,
#             81, 81, 337, 81, 337, 81, 337, 81, 337, 81, 337, 81, -1, 81, 337, 81, 337, 81,
#         ])
#         self.assertEqual(s, t)
#         self.assertEqual(s != t, False)
#         self.assertNotEqual(t, u)
#         self.assertNotEqual(u, v)

#     def test_str(self):
#         def f(owner, promoted, ps):
#             return (owner.value << 8) | ((1 if promoted else 0) << 7) | ps.value

#         empty = SimpleState(0, [-1] * 40)
#         mate = SimpleState(0, [
#             -1, f(WHITE, False, P51),
#             f(BLACK, False, HAND), f(BLACK, False, HAND),
#             f(BLACK, False, HAND), f(BLACK, False, HAND),
#             f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND),
#             f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND),
#             f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND),
#             f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND),
#             f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND),
#             f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND),
#             f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND),
#             f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND),
#             f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND),
#             f(BLACK, False, HAND), f(BLACK, False, HAND), f(BLACK, False, HAND),
#         ])
#         hirate = SimpleState(0, [
#             f(BLACK, False, P59), f(WHITE, False, P51),
#             f(BLACK, False, P28), f(WHITE, False, P82),
#             f(BLACK, False, P88), f(WHITE, False, P22),
#             f(BLACK, False, P19), f(BLACK, False, P99), f(WHITE, False, P11), f(WHITE, False, P91),
#             f(BLACK, False, P49), f(BLACK, False, P69), f(WHITE, False, P41), f(WHITE, False, P61),
#             f(BLACK, False, P39), f(BLACK, False, P79), f(WHITE, False, P31), f(WHITE, False, P71),
#             f(BLACK, False, P29), f(BLACK, False, P89), f(WHITE, False, P21), f(WHITE, False, P81),
#             f(BLACK, False, P17), f(BLACK, False, P27), f(BLACK, False, P37),
#             f(BLACK, False, P47), f(BLACK, False, P57), f(BLACK, False, P67),
#             f(BLACK, False, P77), f(BLACK, False, P87), f(BLACK, False, P97),
#             f(WHITE, False, P13), f(WHITE, False, P23), f(WHITE, False, P33),
#             f(WHITE, False, P43), f(WHITE, False, P53), f(WHITE, False, P63),
#             f(WHITE, False, P73), f(WHITE, False, P83), f(WHITE, False, P93),
#         ])
#         handicapped = SimpleState(1, [
#             f(BLACK, False, P59), f(WHITE, False, P51),
#             f(BLACK, False, P28), -1,
#             f(BLACK, False, P88), -1,
#             f(BLACK, False, P19), f(BLACK, False, P99), f(WHITE, False, P11), f(WHITE, False, P91),
#             f(BLACK, False, P49), f(BLACK, False, P69), f(WHITE, False, P41), f(WHITE, False, P61),
#             f(BLACK, False, P39), f(BLACK, False, P79), f(WHITE, False, P31), f(WHITE, False, P71),
#             f(BLACK, False, P29), f(BLACK, False, P89), f(WHITE, False, P21), f(WHITE, False, P81),
#             f(BLACK, False, P17), f(BLACK, False, P27), f(BLACK, False, P37),
#             f(BLACK, False, P47), f(BLACK, False, P57), f(BLACK, False, P67),
#             f(BLACK, False, P77), f(BLACK, False, P87), f(BLACK, False, P97),
#             f(WHITE, False, P13), f(WHITE, False, P23), f(WHITE, False, P33),
#             f(WHITE, False, P43), f(WHITE, False, P53), f(WHITE, False, P63),
#             f(WHITE, False, P73), f(WHITE, False, P83), f(WHITE, False, P93),
#         ])
#         self.assertEqual(str(empty), '\n'.join([
#             'P1 *  *  *  *  *  *  *  *  * ',
#             'P2 *  *  *  *  *  *  *  *  * ',
#             'P3 *  *  *  *  *  *  *  *  * ',
#             'P4 *  *  *  *  *  *  *  *  * ',
#             'P5 *  *  *  *  *  *  *  *  * ',
#             'P6 *  *  *  *  *  *  *  *  * ',
#             'P7 *  *  *  *  *  *  *  *  * ',
#             'P8 *  *  *  *  *  *  *  *  * ',
#             'P9 *  *  *  *  *  *  *  *  * ',
#             'P+',
#             'P-',
#             '+'
#         ]))
#         self.assertEqual(str(mate), '\n'.join([
#             'P1 *  *  *  * -OU *  *  *  * ',
#             'P2 *  *  *  *  *  *  *  *  * ',
#             'P3 *  *  *  *  *  *  *  *  * ',
#             'P4 *  *  *  *  *  *  *  *  * ',
#             'P5 *  *  *  *  *  *  *  *  * ',
#             'P6 *  *  *  *  *  *  *  *  * ',
#             'P7 *  *  *  *  *  *  *  *  * ',
#             'P8 *  *  *  *  *  *  *  *  * ',
#             'P9 *  *  *  *  *  *  *  *  * ',
#             'P+00HI00HI00KA00KA00KI00KI00KI00KI00GI00GI00GI00GI00KE00KE00KE00KE00KY00KY00KY00KY'
#             '00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU',
#             'P-',
#             '+'
#         ]))
#         self.assertEqual(str(hirate), '\n'.join([
#             'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY',
#             'P2 * -HI *  *  *  *  * -KA * ',
#             'P3-FU-FU-FU-FU-FU-FU-FU-FU-FU',
#             'P4 *  *  *  *  *  *  *  *  * ',
#             'P5 *  *  *  *  *  *  *  *  * ',
#             'P6 *  *  *  *  *  *  *  *  * ',
#             'P7+FU+FU+FU+FU+FU+FU+FU+FU+FU',
#             'P8 * +KA *  *  *  *  * +HI * ',
#             'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY',
#             'P+',
#             'P-',
#             '+'
#         ]))
#         self.assertEqual(str(handicapped), '\n'.join([
#             'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY',
#             'P2 *  *  *  *  *  *  *  *  * ',
#             'P3-FU-FU-FU-FU-FU-FU-FU-FU-FU',
#             'P4 *  *  *  *  *  *  *  *  * ',
#             'P5 *  *  *  *  *  *  *  *  * ',
#             'P6 *  *  *  *  *  *  *  *  * ',
#             'P7+FU+FU+FU+FU+FU+FU+FU+FU+FU',
#             'P8 * +KA *  *  *  *  * +HI * ',
#             'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY',
#             'P+',
#             'P-',
#             '-'
#         ]))

#     def test_from_string(self):
#         def f(owner, promoted, ps):
#             return (owner.value << 8) | ((1 if promoted else 0) << 7) | ps.value

#         # initiated expression
#         self.assertEqual(SimpleState.from_string('PI\n+'),
#                          SimpleState(0, [
#                              f(BLACK, False, P59), f(WHITE, False, P51),
#                              f(BLACK, False, P28), f(WHITE, False, P82),
#                              f(BLACK, False, P88), f(WHITE, False, P22),
#                              f(BLACK, False, P19), f(BLACK, False, P99), f(WHITE, False, P11), f(WHITE, False, P91),
#                              f(BLACK, False, P49), f(BLACK, False, P69), f(WHITE, False, P41), f(WHITE, False, P61),
#                              f(BLACK, False, P39), f(BLACK, False, P79), f(WHITE, False, P31), f(WHITE, False, P71),
#                              f(BLACK, False, P29), f(BLACK, False, P89), f(WHITE, False, P21), f(WHITE, False, P81),
#                              f(BLACK, False, P17), f(BLACK, False, P27), f(BLACK, False, P37),
#                              f(BLACK, False, P47), f(BLACK, False, P57), f(BLACK, False, P67),
#                              f(BLACK, False, P77), f(BLACK, False, P87), f(BLACK, False, P97),
#                              f(WHITE, False, P13), f(WHITE, False, P23), f(WHITE, False, P33),
#                              f(WHITE, False, P43), f(WHITE, False, P53), f(WHITE, False, P63),
#                              f(WHITE, False, P73), f(WHITE, False, P83), f(WHITE, False, P93),
#                          ]))

#         self.assertEqual(SimpleState.from_string('PI\n-'),
#                          SimpleState(1, [
#                              f(BLACK, False, P59), f(WHITE, False, P51),
#                              f(BLACK, False, P28), f(WHITE, False, P82),
#                              f(BLACK, False, P88), f(WHITE, False, P22),
#                              f(BLACK, False, P19), f(BLACK, False, P99), f(WHITE, False, P11), f(WHITE, False, P91),
#                              f(BLACK, False, P49), f(BLACK, False, P69), f(WHITE, False, P41), f(WHITE, False, P61),
#                              f(BLACK, False, P39), f(BLACK, False, P79), f(WHITE, False, P31), f(WHITE, False, P71),
#                              f(BLACK, False, P29), f(BLACK, False, P89), f(WHITE, False, P21), f(WHITE, False, P81),
#                              f(BLACK, False, P17), f(BLACK, False, P27), f(BLACK, False, P37),
#                              f(BLACK, False, P47), f(BLACK, False, P57), f(BLACK, False, P67),
#                              f(BLACK, False, P77), f(BLACK, False, P87), f(BLACK, False, P97),
#                              f(WHITE, False, P13), f(WHITE, False, P23), f(WHITE, False, P33),
#                              f(WHITE, False, P43), f(WHITE, False, P53), f(WHITE, False, P63),
#                              f(WHITE, False, P73), f(WHITE, False, P83), f(WHITE, False, P93),
#                          ]))

#         self.assertEqual(SimpleState.from_string('PI82HI22KA19KY\n-'),
#                          SimpleState(1, [
#                              f(BLACK, False, P59), f(WHITE, False, P51),
#                              f(BLACK, False, P28), -1,
#                              f(BLACK, False, P88), -1,
#                              -1, f(BLACK, False, P99), f(WHITE, False, P11), f(WHITE, False, P91),
#                              f(BLACK, False, P49), f(BLACK, False, P69), f(WHITE, False, P41), f(WHITE, False, P61),
#                              f(BLACK, False, P39), f(BLACK, False, P79), f(WHITE, False, P31), f(WHITE, False, P71),
#                              f(BLACK, False, P29), f(BLACK, False, P89), f(WHITE, False, P21), f(WHITE, False, P81),
#                              f(BLACK, False, P17), f(BLACK, False, P27), f(BLACK, False, P37),
#                              f(BLACK, False, P47), f(BLACK, False, P57), f(BLACK, False, P67),
#                              f(BLACK, False, P77), f(BLACK, False, P87), f(BLACK, False, P97),
#                              f(WHITE, False, P13), f(WHITE, False, P23), f(WHITE, False, P33),
#                              f(WHITE, False, P43), f(WHITE, False, P53), f(WHITE, False, P63),
#                              f(WHITE, False, P73), f(WHITE, False, P83), f(WHITE, False, P93),
#                          ]))

#         # bundle expression
#         self.assertEqual(SimpleState.from_string(
#             'P1 *  *  *  *  *  *  *  *  * \n' +
#             'P2 *  *  *  *  *  *  *  *  * \n' +
#             'P3 *  *  *  *  *  *  *  *  * \n' +
#             'P4 *  *  *  *  *  *  *  *  * \n' +
#             'P5 *  *  *  *  *  *  *  *  * \n' +
#             'P6 *  *  *  *  *  *  *  *  * \n' +
#             'P7 *  *  *  *  *  *  *  *  * \n' +
#             'P8 *  *  *  *  *  *  *  *  * \n' +
#             'P9 *  *  *  *  *  *  *  *  * \n' +
#             '+'
#         ), SimpleState(0, [-1] * 40))

#         self.assertEqual(SimpleState.from_string(
#             'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY\n' +
#             'P2 * -HI *  *  *  *  * -KA * \n' +
#             'P3-FU-FU-FU-FU-FU-FU-FU-FU-FU\n' +
#             'P4 *  *  *  *  *  *  *  *  * \n' +
#             'P5 *  *  *  *  *  *  *  *  * \n' +
#             'P6 *  *  *  *  *  *  *  *  * \n' +
#             'P7+FU+FU+FU+FU+FU+FU+FU+FU+FU\n' +
#             'P8 * +KA *  *  *  *  * +HI * \n' +
#             'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY\n' +
#             '+'
#         ), SimpleState(0, [
#             f(BLACK, False, P59), f(WHITE, False, P51),
#             f(BLACK, False, P28), f(WHITE, False, P82),
#             f(BLACK, False, P88), f(WHITE, False, P22),
#             f(BLACK, False, P19), f(BLACK, False, P99), f(WHITE, False, P11), f(WHITE, False, P91),
#             f(BLACK, False, P49), f(BLACK, False, P69), f(WHITE, False, P41), f(WHITE, False, P61),
#             f(BLACK, False, P39), f(BLACK, False, P79), f(WHITE, False, P31), f(WHITE, False, P71),
#             f(BLACK, False, P29), f(BLACK, False, P89), f(WHITE, False, P21), f(WHITE, False, P81),
#             f(BLACK, False, P17), f(BLACK, False, P27), f(BLACK, False, P37),
#             f(BLACK, False, P47), f(BLACK, False, P57), f(BLACK, False, P67),
#             f(BLACK, False, P77), f(BLACK, False, P87), f(BLACK, False, P97),
#             f(WHITE, False, P13), f(WHITE, False, P23), f(WHITE, False, P33),
#             f(WHITE, False, P43), f(WHITE, False, P53), f(WHITE, False, P63),
#             f(WHITE, False, P73), f(WHITE, False, P83), f(WHITE, False, P93),
#         ]))

#         # single expression
#         self.assertEqual(SimpleState.from_string(
#             'PI82HI22KA\nP+82HI22KA\n+'
#         ), SimpleState(0, [
#             f(BLACK, False, P59), f(WHITE, False, P51),
#             f(BLACK, False, P28), f(BLACK, False, P82),
#             f(BLACK, False, P88), f(BLACK, False, P22),
#             f(BLACK, False, P19), f(BLACK, False, P99), f(WHITE, False, P11), f(WHITE, False, P91),
#             f(BLACK, False, P49), f(BLACK, False, P69), f(WHITE, False, P41), f(WHITE, False, P61),
#             f(BLACK, False, P39), f(BLACK, False, P79), f(WHITE, False, P31), f(WHITE, False, P71),
#             f(BLACK, False, P29), f(BLACK, False, P89), f(WHITE, False, P21), f(WHITE, False, P81),
#             f(BLACK, False, P17), f(BLACK, False, P27), f(BLACK, False, P37),
#             f(BLACK, False, P47), f(BLACK, False, P57), f(BLACK, False, P67),
#             f(BLACK, False, P77), f(BLACK, False, P87), f(BLACK, False, P97),
#             f(WHITE, False, P13), f(WHITE, False, P23), f(WHITE, False, P33),
#             f(WHITE, False, P43), f(WHITE, False, P53), f(WHITE, False, P63),
#             f(WHITE, False, P73), f(WHITE, False, P83), f(WHITE, False, P93),
#         ]))

#         self.assertEqual(SimpleState.from_string(
#             'P1 *  *  *  *  *  *  *  *  * \n' +
#             'P2 *  *  *  *  *  *  *  *  * \n' +
#             'P3 *  *  *  *  *  *  *  *  * \n' +
#             'P4 *  *  *  *  *  *  *  *  * \n' +
#             'P5 *  *  *  *  *  *  *  *  * \n' +
#             'P6 *  *  *  *  *  *  *  *  * \n' +
#             'P7 *  *  *  *  *  *  *  *  * \n' +
#             'P8 *  *  *  *  *  *  *  *  * \n' +
#             'P9 *  *  *  *  *  *  *  *  * \n' +
#             'P+99KY\nP+89KE\nP+79GI\nP+69KI\nP+59OU\nP+49KI\nP+39GI\nP+29KE\nP+19KY\nP+88KA\nP+28HI\n' +
#             'P+97FU\nP+87FU\nP+77FU\nP+67FU\nP+57FU\nP+47FU\nP+37FU\nP+27FU\nP+17FU\n' +
#             'P-93FU\nP-83FU\nP-73FU\nP-63FU\nP-53FU\nP-43FU\nP-33FU\nP-23FU\nP-13FU\nP-82HI\nP-22KA\n' +
#             'P-91KY\nP-81KE\nP-71GI\nP-61KI\nP-51OU\nP-41KI\nP-31GI\nP-21KE\nP-11KY\n' +
#             '+'
#         ), SimpleState(0, [
#             f(BLACK, False, P59), f(WHITE, False, P51),
#             f(BLACK, False, P28), f(WHITE, False, P82),
#             f(BLACK, False, P88), f(WHITE, False, P22),
#             f(BLACK, False, P19), f(BLACK, False, P99), f(WHITE, False, P11), f(WHITE, False, P91),
#             f(BLACK, False, P49), f(BLACK, False, P69), f(WHITE, False, P41), f(WHITE, False, P61),
#             f(BLACK, False, P39), f(BLACK, False, P79), f(WHITE, False, P31), f(WHITE, False, P71),
#             f(BLACK, False, P29), f(BLACK, False, P89), f(WHITE, False, P21), f(WHITE, False, P81),
#             f(BLACK, False, P17), f(BLACK, False, P27), f(BLACK, False, P37),
#             f(BLACK, False, P47), f(BLACK, False, P57), f(BLACK, False, P67),
#             f(BLACK, False, P77), f(BLACK, False, P87), f(BLACK, False, P97),
#             f(WHITE, False, P13), f(WHITE, False, P23), f(WHITE, False, P33),
#             f(WHITE, False, P43), f(WHITE, False, P53), f(WHITE, False, P63),
#             f(WHITE, False, P73), f(WHITE, False, P83), f(WHITE, False, P93),
#         ]))

#         self.assertEqual(SimpleState.from_string(
#             "P+59OU00FU\nP-51OU\nP+00FU\nP+11UM\nP-12TO\nP-00AL\n-"
#         ), SimpleState(1, [
#             f(BLACK, False, P59), f(WHITE, False, P51),
#             f(WHITE, False, HAND), f(WHITE, False, HAND),
#             f(BLACK, True, P11), f(WHITE, False, HAND),
#             f(WHITE, False, HAND), f(WHITE, False, HAND), f(WHITE, False, HAND), f(WHITE, False, HAND),
#             f(WHITE, False, HAND), f(WHITE, False, HAND), f(WHITE, False, HAND), f(WHITE, False, HAND),
#             f(WHITE, False, HAND), f(WHITE, False, HAND), f(WHITE, False, HAND), f(WHITE, False, HAND),
#             f(WHITE, False, HAND), f(WHITE, False, HAND), f(WHITE, False, HAND), f(WHITE, False, HAND),
#             f(BLACK, False, HAND), f(BLACK, False, HAND), f(WHITE, True, P12),
#             f(WHITE, False, HAND), f(WHITE, False, HAND), f(WHITE, False, HAND),
#             f(WHITE, False, HAND), f(WHITE, False, HAND), f(WHITE, False, HAND),
#             f(WHITE, False, HAND), f(WHITE, False, HAND), f(WHITE, False, HAND),
#             f(WHITE, False, HAND), f(WHITE, False, HAND), f(WHITE, False, HAND),
#             f(WHITE, False, HAND), f(WHITE, False, HAND), f(WHITE, False, HAND),
#         ]))

#         self.assertEqual(SimpleState.from_string("P+00AL\n-"), SimpleState(1, [-1] * 2 + [f(BLACK, False, HAND)] * 38))
#         self.assertEqual(SimpleState.from_string("P-00AL\n-"), SimpleState(1, [-1] * 2 + [f(WHITE, False, HAND)] * 38))
#         self.assertEqual(SimpleState.from_string(
#             "P+51OU00AL\n+"
#         ), SimpleState(0, [f(BLACK, False, P51), -1] + [f(BLACK, False, HAND)] * 38))
#         self.assertEqual(SimpleState.from_string(
#             "P+51OU\nP-00AL\n+"
#         ), SimpleState(0, [f(BLACK, False, P51), -1] + [f(WHITE, False, HAND)] * 38))

#     def test_from_string_invalid(self):
#         self.assertRaises(ValueError, SimpleState.from_string, '')
#         self.assertRaises(ValueError, SimpleState.from_string, 'PI')
#         self.assertRaises(ValueError, SimpleState.from_string, 'PI82KA\n+')
#         self.assertRaises(ValueError, SimpleState.from_string, 'PI82HI82HI\n+')
#         self.assertRaises(ValueError, SimpleState.from_string, 'PI8\n+')
#         self.assertRaises(ValueError, SimpleState.from_string, 'PI82\n+')
#         self.assertRaises(ValueError, SimpleState.from_string, 'PI82H\n+')
#         self.assertRaises(ValueError, SimpleState.from_string, 'P+00AL\nP-00AL\n+')
#         self.assertRaises(ValueError, SimpleState.from_string, 'PI55KA\nP-00AL55KA\n+')
#         self.assertRaises(ValueError, SimpleState.from_string, 'PI55KA\nP-00AL\nP-55KA\n+')
#         self.assertRaises(ValueError, SimpleState.from_string, 'P+11OU12OU\n+')
#         self.assertRaises(ValueError, SimpleState.from_string, 'P-11OU12OU\n+')
