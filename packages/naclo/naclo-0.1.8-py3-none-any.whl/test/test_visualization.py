import unittest
from rdkit import Chem
from rdkit.Chem import MACCSkeys
from naclo import mol_conversion, visualization
import numpy as np


class TestVisualization(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_smiles = ['CN=C=O', 'CCC', 'O']
        cls.test_mols = mol_conversion.smiles_2_mols(cls.test_smiles)
        cls.maccs_keys = mol_conversion.mols_2_maccs(cls.test_mols)
        cls.ecfp4_prints = mol_conversion.mols_2_ecfp(cls.test_mols, radius=2, return_numpy=False)
        cls.ecfp6_prints = mol_conversion.mols_2_ecfp(cls.test_mols, radius=3, return_numpy=False)
        return super().setUpClass()
    
    def test_sim_matrix(self):
        mat_maccs = visualization.sim_matrix(self.maccs_keys, self.maccs_keys, key_type='maccs')  # Test MACCS keys
        mat_ecfp4 = visualization.sim_matrix(self.ecfp4_prints, self.ecfp4_prints)  # Test ECFP4
        mat_ecfp6 = visualization.sim_matrix(self.ecfp6_prints, self.ecfp6_prints)  # Test ECFP6
        
        # Check same molecules equal 1 in matrix in all cases (along identity)
        np.testing.assert_array_equal(
            mat_maccs[np.eye(3, dtype=bool)],
            mat_ecfp4[np.eye(3, dtype=bool)],
            mat_ecfp6[np.eye(3, dtype=bool)],
            3*[1]
        )
        
        # Check maccs is different than ecfp but ecfp4,6 are equal
        self.assertFalse(
            np.array_equal(
                mat_maccs,
                mat_ecfp4
            )
        )
        np.testing.assert_array_equal(
            mat_ecfp4,
            mat_ecfp6
        )
        
        
if __name__ == '__main__':
    unittest.main()
