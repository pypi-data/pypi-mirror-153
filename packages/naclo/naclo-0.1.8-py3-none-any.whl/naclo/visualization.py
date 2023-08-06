import numpy as np
from rdkit import DataStructs


def sim_matrix(row_keys, col_keys, key_type='ecfp'):
    """Constructs a tanimoto matrix from ecfp or maccs fingerprints.

    :param row_keys: Collection of fingerprints
    :type row_keys: iter[binary]]
    :param col_keys: Collection of fingerprints 2
    :type col_keys: iter[binary]
    :param key_type: Fingerprint type, defaults to 'ecfp'
    :type key_type: str, optional
    :return: Tanimoto array
    :rtype: np.array()
    """
    
    # Initialize zero array
    full_array = np.zeros((len(row_keys), len(col_keys)))

    # Run through rows and cols of matrix according to key_type
    for i, row in enumerate(row_keys):
        for j, col in enumerate(col_keys):
            if key_type == 'ecfp':
                similarity = DataStructs.TanimotoSimilarity(row, col)
            elif key_type == 'maccs':
                similarity = DataStructs.FingerprintSimilarity(row, col)
            else:
                raise('Key type must be either "ecfp" or "maccs".')
                
            full_array[i][j] = similarity
    
    return full_array

# def plot_tsne(df, smiles_col, names_col=None, descriptors='ecfp6', alpha=1, color_col=None, continuous_grad=False):
#     seed = 42
    
#     X = []
#     error_indices = []
#     num_errors = 0
    
#     if descriptors == 'ecfp6':
#         X = ecfp6_descriptors(df[smiles_col])
        
#     elif descriptors == 'other' or descriptors == 'other_norm':
#         other_df = other_descriptors(df, [smiles_col, color_col, names_col, 'ROMol'])
#         if descriptors == 'other_norm':
#             other_df = z_norm(other_df)
#         X = other_df.to_numpy()
        
#     elif descriptors == 'ecfp6_other':
#         other_df = other_descriptors(df, [smiles_col, color_col, names_col, 'ROMol'])
#         norm_other_X = z_norm(other_df).to_numpy()
#         ecfp6_X = ecfp6_descriptors(df[smiles_col])
#         X = np.concatenate((ecfp6_X, norm_other_X), axis=1)
    
#     # Remove errors
#     fin_suppl = df.loc[~df.index.isin(error_indices)]
#     # save the full t-SNE
#     tsne = TSNE(n_components=2, random_state=seed)
#     X_fit = tsne.fit_transform(X)
#     fin_suppl['t-SNE 1'] = X_fit.T[0]
#     fin_suppl['t-SNE 2'] = X_fit.T[1]
    
#     # fin_suppl.sort_values(by=color_col, inplace=True)
    
#     if color_col:
#         fig = px.scatter(fin_suppl, x='t-SNE 1', y='t-SNE 2', color=color_col, render_mode='svg')
#     else:
#         fig = px.scatter(fin_suppl, x='t-SNE 1', y='t-SNE 2', render_mode='svg')
#     # fig = plt.figure()
#     # for cat in fin_suppl[color_col].unique():
#     #     temp = fin_suppl.where(fin_suppl[color_col] == cat)
#     #     plt.scatter(temp['tsne_x'], temp['tsne_y'], alpha=alpha)
    
#     # plt.scatter(fin_suppl['tsne_x'], fin_suppl['tsne_y'])
#     # plt.show()
#     return fig, fin_suppl


# def ecfp6_descriptors(smiles):
#     X = []
#     error_indices = []
#     num_errors = 0
    
#     for smile in smiles:
#         try:
#             mol = AllChem.MolFromSmiles(smile)
#             arr = np.zeros((0,))
#             fingerprint = AllChem.GetMorganFingerprintAsBitVect(mol, 2)
#             DataStructs.ConvertToNumpyArray(fingerprint, arr)
#             X.append(arr)
#         except:
#             num_errors += 1
#             error_indices.append(num_errors - 1)
#             pass
        
#     return X