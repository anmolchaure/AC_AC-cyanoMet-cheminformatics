import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs
import numpy as np
import os

# Load the dataset
file_path = r"/Users/parijat/Desktop/Research_Projects/7_Floridanema50_Tychonamide Analogue/FLORIDANEMAMIDE_clustering/DATABASE/cynometdbV3_2024_with_trichonew.csv"
df = pd.read_csv(file_path)

# Prompt for similarity method
similarity_method = input("Choose similarity method: 'Tanimoto' or 'Tversky': ").strip().lower()

if similarity_method not in ['tanimoto', 'tversky']:
    raise ValueError("Invalid similarity method. Choose either 'Tanimoto' or 'Tversky'.")

# Generate Morgan fingerprints
fingerprints = []
for smile in df['SMILES']:
    mol = Chem.MolFromSmiles(smile)
    if mol is not None:
        fingerprints.append(AllChem.GetMorganFingerprintAsBitVect(mol, 3, nBits=2048))
    else:
        fingerprints.append(None)

# Initialize empty similarity matrix
n = len(fingerprints)
similarity_matrix = np.zeros((n, n))

# Tversky parameters
alpha = 0.95
beta = 0.05

# Compute similarity only where both fingerprints exist
for i in range(n):
    for j in range(n):
        if i != j and fingerprints[i] is not None and fingerprints[j] is not None:
            if similarity_method == 'tanimoto':
                similarity = DataStructs.TanimotoSimilarity(fingerprints[i], fingerprints[j])
            else:  # tversky
                similarity = DataStructs.TverskySimilarity(fingerprints[i], fingerprints[j], alpha, beta)
            similarity_matrix[i, j] = similarity

# Convert to DataFrame
similarity_df = pd.DataFrame(similarity_matrix, index=df['Name'], columns=df['Name'])

# Prompt for output file
output_file_name = input("Enter the output file name (without extension): ").strip()
output_directory = r"/Users/parijat/Desktop/Research_Projects/7_Floridanema50_Tychonamide Analogue/FLORIDANEMAMIDE_clustering/Array_flm"
output_file_path = os.path.join(output_directory, f"{output_file_name}.csv")

# Save result
similarity_df.to_csv(output_file_path)

print(f"✅ Similarity matrix using {similarity_method.capitalize()} method saved to:\n{output_file_path}")
