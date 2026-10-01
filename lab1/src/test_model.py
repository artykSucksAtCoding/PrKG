import unittest
from model import ColorMath

class TestColorMath(unittest.TestCase):
    def test_rgb_to_hsv_red(self):
        h, s, v = ColorMath.rgb_to_hsv(255, 0, 0)
        self.assertEqual(round(h), 0)
        self.assertEqual(round(s), 100)
        self.assertEqual(round(v), 100)

    def test_hsv_to_rgb_blue(self):
        r, g, b = ColorMath.hsv_to_rgb(240, 100, 100)
        self.assertEqual(round(r), 0)
        self.assertEqual(round(g), 0)
        self.assertEqual(round(b), 255)

    def test_cmyk_gcr_red(self):
        c, m, y, k = ColorMath.rgb_to_cmyk(255, 0, 0, method="GCR")
        self.assertEqual(round(c), 0)
        self.assertEqual(round(m), 100)
        self.assertEqual(round(y), 100)
        self.assertEqual(round(k), 0)

    def test_cmyk_to_rgb_red(self):
        r, g, b = ColorMath.cmyk_to_rgb(0, 100, 100, 0)
        self.assertEqual(round(r), 255)
        self.assertEqual(round(g), 0)
        self.assertEqual(round(b), 0)

if __name__ == '__main__':
    unittest.main()