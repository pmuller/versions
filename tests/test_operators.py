from unittest import TestCase

from versions import operators


class TestOperator(TestCase):

    def test_parse_eq(self):
        self.assertEqual(operators.Operator.parse('=='),
                         operators.eq)

    def test_parse_ne(self):
        self.assertEqual(operators.Operator.parse('!='),
                         operators.ne)

    def test_parse_le(self):
        self.assertEqual(operators.Operator.parse('<='),
                         operators.le)

    def test_parse_lt(self):
        self.assertEqual(operators.Operator.parse('<'),
                         operators.lt)

    def test_parse_ge(self):
        self.assertEqual(operators.Operator.parse('>='),
                         operators.ge)

    def test_parse_gt(self):
        self.assertEqual(operators.Operator.parse('>'),
                         operators.gt)

    def test_parse_raises_InvalidOperator(self):
        self.assertRaises(operators.InvalidOperator,
                          operators.Operator.parse, 'junk')

    def test_str(self):
        self.assertEqual(str(operators.eq), operators.eq.string)

    def test_call(self):
        self.assertTrue(operators.eq(1, 1))
        self.assertTrue(operators.ne(2, 1))
        self.assertTrue(operators.lt(2, 3))
        self.assertTrue(operators.le(2, 3))
        self.assertTrue(operators.gt(3, 2))
        self.assertTrue(operators.ge(3, 2))

    def test_repr(self):
        self.assertEqual(repr(operators.eq), "Operator.parse('==')")
