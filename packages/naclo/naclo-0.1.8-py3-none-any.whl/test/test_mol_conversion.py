import unittest
from naclo import mol_conversion
from rdkit.Chem import PandasTools
import pandas as pd


class TestMolConversion(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Load excel test data
        test_excel = pd.read_excel('test/excel_test_case.xlsx')
        cls.excel_smiles = list(test_excel.Smiles)
        cls.excel_inchi_keys = list(test_excel.InChi)

        # Load SDF test data
        test_sdf = PandasTools.LoadSDF('test/sdf_test_case.sdf', molColName='Molecule')
        cls.sdf_mols = list(test_sdf.Molecule)
        cls.sdf_smiles = list(test_sdf.Smiles)
        
        return super().setUpClass()
    
    def test_mols_2_smiles(self):
        self.assertEqual(
            self.sdf_smiles, 
            mol_conversion.mols_2_smiles(self.sdf_mols)
        )
        
    def test_smiles_2_mols(self):
        self.assertEqual(
            self.excel_smiles,
            mol_conversion.mols_2_smiles(mol_conversion.smiles_2_mols(self.excel_smiles))
        )
        
    def test_mols_2_inchi_keys(self):
        self.assertEqual(
            self.excel_inchi_keys,
            mol_conversion.mols_2_inchi_keys(mol_conversion.smiles_2_mols(self.excel_smiles))
        )
        
    def test_smiles_2_inchi_keys(self):
        self.assertEqual(
            self.excel_inchi_keys, 
            mol_conversion.smiles_2_inchi_keys(self.excel_smiles)
        )

    def test_mols_2_ecfp(self):
        ecfp = mol_conversion.mols_2_ecfp(self.sdf_mols, return_numpy=True)
        print(ecfp)
        for i in ecfp:
            print(len(i))
            print(sum(i))
        
    def test_mols_2_maccs(self):
        mol_conversion.mols_2_maccs(self.sdf_mols)


if __name__ == '__main__':
    unittest.main()
