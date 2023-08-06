import unittest
import mwx.utilus as ut


class TestTokenizerMethods(unittest.TestCase):

    def test_split_words1(self):
        s = ' '
        c = ','
        values = (
            ## ("f(1 * 2), f (1 / 2)", ['f(1 * 2)', c, s, 'f (1 / 2)']),
            ("f(1 * 2), f (1 / 2)", ['f(1 * 2)', c, ' f (1 / 2)']),
            ("f(1,\n  2)", ['f(1,\n  2)']),
        )
        for text, result in values:
            ret = ut.split_words(text)
            print(text, ret)
            self.assertEqual(ret, result)


if __name__ == "__main__":
    unittest.main()
