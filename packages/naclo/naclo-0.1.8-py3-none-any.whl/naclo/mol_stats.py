from rdkit.Chem.Descriptors import ExactMolWt


def mol_weights(mols):  # *
    """Finds molecular weights from list of Mols.

    Args:
        mols (list): Contains RDKit Mol objects.

    Returns:
        list: Molecular weights. Numeric.
    """
    return [ExactMolWt(mol) for mol in mols]

def carbon_num(smile):  # *
    """Finds number of carbons present in SMILES string.

    Args:
        smile (str): Mol SMILES representation.

    Returns:
        int: Number of carbons in SMILES.
    """
    return smile.lower().count('c')
