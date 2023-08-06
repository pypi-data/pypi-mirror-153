import unittest
from lcbuilder.HarmonicSelector import HarmonicSelector


class TestsHarmonics(unittest.TestCase):
    def test_t0s_matching(self):
        assert HarmonicSelector.matches_t0(1, 1, 1, 1)
        assert HarmonicSelector.matches_t0(1, 2, 1, -2)
        assert HarmonicSelector.matches_t0(1, 3, 1, -3)
        assert HarmonicSelector.matches_t0(3, 2.66, 1, 3)
        assert HarmonicSelector.matches_t0(2, 2.5, 1, 2)
        assert HarmonicSelector.matches_t0(1, 1.01, 1, 1)
        assert HarmonicSelector.matches_t0(1, 2.01, 1, -2)
        assert HarmonicSelector.matches_t0(1, 3.01, 1, -3)
        assert HarmonicSelector.matches_t0(2, 1.505, 1, 2)
        assert HarmonicSelector.matches_t0(0.99, 1, 1, 1)
        assert HarmonicSelector.matches_t0(0.99, 2, 1, -2)
        assert HarmonicSelector.matches_t0(0.99, 3, 1, -3)
        assert HarmonicSelector.matches_t0(2.99, 2.66, 1, 3)
        assert HarmonicSelector.matches_t0(2.0, 2.51, 1, 2)
        assert not HarmonicSelector.matches_t0(2.0, 2.6, 1, 2)
        assert not HarmonicSelector.matches_t0(1000.0, 1005.0, 3, -2)

    def test_periods_matching(self):
        assert HarmonicSelector.multiple_of(1, 3)
        assert HarmonicSelector.multiple_of(1, 2)
        assert HarmonicSelector.multiple_of(1, 1)
        assert HarmonicSelector.multiple_of(3, 1)
        assert HarmonicSelector.multiple_of(2, 1)
        assert HarmonicSelector.multiple_of(1, 3.01)
        assert HarmonicSelector.multiple_of(1, 2.01)
        assert HarmonicSelector.multiple_of(1.01, 1)
        assert HarmonicSelector.multiple_of(2.01, 1)
        assert HarmonicSelector.multiple_of(1.01, 1.02)
        assert not HarmonicSelector.multiple_of(3, 2)
        assert not HarmonicSelector.multiple_of(2, 3)
        assert not HarmonicSelector.multiple_of(1.99, 4.06)

    def test_harmonic(self):
        assert HarmonicSelector.is_harmonic(1000.0, 1002.0, 4, 2)
        assert HarmonicSelector.is_harmonic(1000.0, 1004.0, 6, 2)
        assert HarmonicSelector.is_harmonic(1002.0, 1004.0, 2, 4)
        assert HarmonicSelector.is_harmonic(1004.0, 1000.0, 2, 6)
        assert HarmonicSelector.is_harmonic(1000.0, 999.99, 2, 2)
        assert not HarmonicSelector.is_harmonic(1000.0, 996.99, 2, 2)
        assert not HarmonicSelector.is_harmonic(1000.0, 996.99, 2, 4)


if __name__ == '__main__':
    unittest.main()
