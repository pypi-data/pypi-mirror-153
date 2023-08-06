from rdkit import Chem
from rdkit.Chem import AllChem


def init_neutralization_rxns(reactants_products={'[$([O-]);!$([O-][#7])]': 'O'}):
    """Builds reactions from dict of reactants and products.

    Args:
        reactants (dict, optional): Reactants (keys) and products (values) SMARTS subgroups. \
            Defaults to Carboxylic acids and alcohols ('[$([O-]);!$([O-][#7])]', 'O').

    Returns:
        dict: Contains Mol representations of reactants.
    """
    reactions = {}
    for reactant in reactants_products.keys():
        product = reactants_products[reactant]
        reactions[Chem.MolFromSmarts(reactant)] = Chem.MolFromSmarts(product)
        
    return reactions

def neutralize_charges(mols, reactants_products={'[$([O-]);!$([O-][#7])]': 'O'}):
    """Neutralizes Mol charges by replacing reactants with products.

    Args:
        mols (list): RDKit Mol objects. Mols to neutralize.
        reactants_products (dict, optional): Reactants (keys) and products (values) SMARTS subgroups. \
            Defaults to Carboxylic acids and alcohols ('[$([O-]);!$([O-][#7])]', 'O').

    Returns:
        list: Neutralized RDKit Mols.
    """
    reactions = init_neutralization_rxns(reactants_products=reactants_products)
    
    neutralized_mols = []
    for mol in mols:
        # Iterate over neutralization reactions
        for (reactant, product) in zip(reactions.keys(), reactions.values()):
            # Loop until all instances have been found
            while mol.HasSubstructMatch(reactant):
                mol = AllChem.ReplaceSubstructs(mol, reactant, product)[0]
                mol.UpdatePropertyCache()     
        
        neutralized_mols.append(mol)
        
    return neutralized_mols
