import unittest

import arithmetic_expr as ae


class ArithmeticExprTest(unittest.TestCase):

    def test_apply_operator(self):
        self.assertEqual(5, ae.apply_operator(2, '+', 3))
        self.assertEqual(-1, ae.apply_operator(2, '-', 3))
        self.assertEqual(10, ae.apply_operator(2, '*', 5))
        self.assertEqual(3, ae.apply_operator(6, '/', 2))
        self.assertEqual(4.5, ae.apply_operator(9, '/', 2))

    def test_crossover(self):
        c1 = '11110000'
        c2 = '00001111'
        self.assertEqual(('11111111', '00000000'), ae.crossover(c1, c2, 4))
        self.assertEqual((c1, c2), ae.crossover(c1, c2, len(c1)))


if __name__ == '__main__':
    unittest.main()
