import unittest
import pandas as pd
from rdkit import Chem
from rdkit.Chem import PandasTools

import naclo
from naclo import dataframes


class TestDataframes(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_df = pd.DataFrame({'a': [4, '5', '6'], 'b': ['6', '5', '4']})
        cls.mol_test_df = pd.DataFrame({
            'SMILES': ['O=C(O)C1(Sc2ccnc3ccc(Br)cc23)CCC1', 
                       'O=C(O)C1(Sc2ccnc3ccc(C4CC4)cc23)CCC1', 
                       'CC(C)(Sc1ccncc1-c1ccc(C#N)c2ccccc12)C(=O)O',
                       None],
            'Molecule': [Chem.MolFromSmiles('O=C(O)C1(Sc2ccnc3ccc(Br)cc23)CCC1'),
                         Chem.MolFromSmiles('O=C(O)C1(Sc2ccnc3ccc(C4CC4)cc23)CCC1'),
                         Chem.MolFromSmiles('CC(C)(Sc1ccncc1-c1ccc(C#N)c2ccccc12)C(=O)O'),
                         None],
            'InChi': [Chem.MolToInchiKey(Chem.MolFromSmiles('O=C(O)C1(Sc2ccnc3ccc(Br)cc23)CCC1')),
                      Chem.MolToInchiKey(Chem.MolFromSmiles('O=C(O)C1(Sc2ccnc3ccc(C4CC4)cc23)CCC1')),
                      Chem.MolToInchiKey(Chem.MolFromSmiles('CC(C)(Sc1ccncc1-c1ccc(C#N)c2ccccc12)C(=O)O')),
                      None]
        })
        
        cls.excel_df = pd.read_excel('test/excel_test_case.xlsx')
        cls.excel_df = dataframes.df_smiles_2_mols(cls.excel_df, 'Smiles', 'Molecule')
        cls.sdf_df = PandasTools.LoadSDF('test/sdf_test_case.sdf', molColName='Molecule')
        cls.sdf_df.ID = list(range(4))
        
        return super().setUpClass()
    
    def test_df_smiles_2_mols(self):
         # Test with dropna
        out1 = dataframes.df_smiles_2_mols(self.mol_test_df, 'SMILES', 'ROMol')
        assert out1.ROMol.map(Chem.MolToSmiles, na_action='ignore').equals(self.mol_test_df.Molecule.map(Chem.MolToSmiles, na_action='ignore').dropna())
        
        # Test without dropna
        out2 = dataframes.df_smiles_2_mols(self.mol_test_df, 'SMILES', 'ROMol', dropna=False)
        assert out2.ROMol.map(Chem.MolToSmiles, na_action='ignore').equals(self.mol_test_df.Molecule.map(Chem.MolToSmiles, na_action='ignore'))
    
    def test_df_mols_2_inchi_keys(self):
        # Test with dropna
        out1 = dataframes.df_mols_2_inchi_keys(self.mol_test_df, 'Molecule', 'inchi')
        assert out1.inchi.equals(self.mol_test_df.InChi.dropna())
        
        # Test without dropna
        out2 = dataframes.df_mols_2_inchi_keys(self.mol_test_df, 'Molecule', 'inchi', dropna=False)
        assert out2.inchi.equals(self.mol_test_df.InChi)
        
    def test_df_mols_2_smiles(self):
        # Test with dropna
        out1 = dataframes.df_mols_2_smiles(self.mol_test_df, 'Molecule', 'smiles')
        assert out1.smiles.equals(self.mol_test_df.SMILES.dropna())
        
        # Test without dropna
        out2 = dataframes.df_mols_2_smiles(self.mol_test_df, 'Molecule', 'smiles', dropna=False)
        assert out2.smiles.equals(self.mol_test_df.SMILES)
        
    def test_write_sdf(self):
        # Write new and load new
        dataframes.write_sdf(self.excel_df, 'test/sdf_test_out.sdf', mol_col_name='Molecule')
        load_sdf = PandasTools.LoadSDF('test/sdf_test_out.sdf', molColName='Molecule')
        
        # Ensure Mols are the same
        self.assertEqual(
            naclo.mols_2_smiles(load_sdf.Molecule),
            naclo.mols_2_smiles(self.sdf_df.Molecule)
        )
        
        # Ensure original SMILES are the same
        assert load_sdf.Smiles.equals(self.sdf_df.Smiles)
