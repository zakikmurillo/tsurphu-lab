import unittest

from engines.year_mewa_parkha import mewa_for_gregorian_year, parkha_for_mewa
from engines.tibetan_year import tibetan_year

class TestYearCycles(unittest.TestCase):
    def test_mewa_examples(self):
        # 1984 Wood Rat -> mewa 1; luego 9,8,...
        self.assertEqual(mewa_for_gregorian_year(1984), 1)
        self.assertEqual(mewa_for_gregorian_year(1985), 9)
        self.assertEqual(mewa_for_gregorian_year(1986), 8)
        # 60 años después (mód 9): 2044 debería ser 4
        self.assertEqual(mewa_for_gregorian_year(2044), 4)

    def test_parkha_mapping_non5(self):
        self.assertEqual(parkha_for_mewa(1, polarity="yang").code, "Kham")
        self.assertEqual(parkha_for_mewa(2, polarity="yang").code, "Khon")
        self.assertEqual(parkha_for_mewa(9, polarity="yang").code, "Li")

    def test_tibetan_year_smoke(self):
        ty = tibetan_year(1984)
        self.assertEqual(ty.animal, "Rat")
        self.assertEqual(ty.element, "Wood")
        self.assertEqual(ty.mewa, 1)
        self.assertTrue(ty.parkha in {"Kham","Khon","Zin","Zon","Khen","Dwa","Gin","Li"})

if __name__ == "__main__":
    unittest.main()
