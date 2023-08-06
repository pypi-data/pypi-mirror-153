import unittest
from naclo import neutralize
from naclo import mol_conversion


class TestNeutralize(unittest.TestCase):
    def test_init_neutralization_rxns(self):
        rxns = neutralize.init_neutralization_rxns()
        rxns = list(rxns.values()) +  list(rxns.keys())
        
        self.assertEqual(
            mol_conversion.mols_2_smiles(rxns),
            ['O', '*']
        )  # What does test_init_neutralization do????
        

    def test_neutralize_charges(self):
        # Doesn't do anything yet
        pass


if __name__ == '__main__':
    unittest.main()
