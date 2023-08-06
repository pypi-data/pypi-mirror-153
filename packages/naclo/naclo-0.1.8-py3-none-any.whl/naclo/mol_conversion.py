from rdkit import Chem
import numpy as np
from rdkit.Chem import AllChem, MACCSkeys, DataStructs


def mols_2_smiles(mols):  # *
    """Generates SMILES strings from list of rdkit Mol objects.

    Args:
        mols (iter[rdkit Mol]): Contains RDKit Mols.

    Returns:
        list[str]: Contains SMILES strings.
    """
    return [Chem.MolToSmiles(mol) for mol in mols]

def smiles_2_mols(smiles):  # *
    """Generates rdkit Mol objects from SMILES strings.

    Args:
        smiles (iter[str]): Contains SMILES strings.

    Returns:
        list[rdkit Mol]: Contains RDKit Mols.
    """
    return [Chem.MolFromSmiles(smile) for smile in smiles]

def mols_2_inchi_keys(mols):  # *
    """Generates InChI key strings from rdkit Mol objects.

    Args:
        mols (iter[rdkit Mols]): Contains rdkit Mols.

    Returns:
        list[str]: Contains InChI key strings.
    """
    return [Chem.MolToInchiKey(mol) for mol in mols]

def smiles_2_inchi_keys(smiles):  # *
    """Generates InChI key strings from SMILES strings.

    Args:
        smiles (iter[str]): Contains SMILES strings.

    Returns:
        list[str]: Contains InChI key strings.
    """
    mols = smiles_2_mols(smiles)
    return mols_2_inchi_keys(mols)

def mols_2_ecfp(mols, radius=2, return_numpy=False, n_bits=1024):
    """Converts from rdkit mol objects to morgan fingerprints (full ECFP6).

    :param mols: Collection of mols
    :type mols: list[rdkit mol]
    :param radius: ECFP radius, defaults to 3 (ECFP6)
    :type radius: int, optional
    :return: Collection of ECFP vectors
    :rtype: list[rdkit BitVect]
    """
    if return_numpy:
        fingerprints = [AllChem.GetMorganFingerprintAsBitVect(m, radius, nBits=n_bits) for m in mols]
        
        X = []
        for fp in fingerprints:
            arr = np.array([])
            DataStructs.ConvertToNumpyArray(fp, arr)
            X.append(arr)
        return X
    else:
        return [AllChem.GetMorganFingerprint(m, radius) for m in mols]

def mols_2_maccs(mols):
    """Converts from mol objects to MACCS keys.

    :param mols: Collection of molecules
    :type mols: list[rdkit mol]
    :return: Collection of MACCS keys
    :rtype: list[rdkit BitVect]
    """
    return [MACCSkeys.GenMACCSKeys(m) for m in mols]
