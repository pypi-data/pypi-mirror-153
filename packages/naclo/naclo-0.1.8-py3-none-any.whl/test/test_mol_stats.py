import unittest
from naclo import mol_stats
from naclo import mol_conversion


class TestMolStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_smile = 'CN=C=O'
        cls.test_mols = mol_conversion.smiles_2_mols([cls.test_smile, 'C'])
        return super().setUpClass()
    
    def test_carbon_num(self):
        self.assertEqual(
            mol_stats.carbon_num(self.test_smile),
            2
        )
    
    def test_mol_weights(self):
        self.assertEqual(
            list(map(lambda x: round(x, 3), mol_stats.mol_weights(self.test_mols))), 
            [57.021, 16.031]
        )


if __name__ == '__main__':
    unittest.main()
