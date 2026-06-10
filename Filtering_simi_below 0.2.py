import pandas as pd
import os

# Directly assign the input CSV file path
input_file = r"/Users/parijat/Desktop/Research_Projects/7_Floridanema50_Tychonamide Analogue/FLORIDANEMAMIDE_clustering/Array_flm/CyanoMET_All_.csv"
# Check if file exists
if not os.path.exists(input_file):
    print(f"Error: File '{input_file}' not found.")
    exit()

# Load the CSV file, ensuring the first row is read as column headers
df = pd.read_csv(input_file, index_col=0)  # Set the first column as index (molecule names)

# Store the molecule names (both row and column names)
molecule_names = df.columns.tolist()  # First row (column names)
df.index.name = "Name"  # Rename the index for clarity

# Convert the matrix to numeric values (excluding row/column names)
df_numeric = df.apply(pd.to_numeric, errors='coerce')

# Replace values ≤ 0.2 with 0
df_numeric[df_numeric <= 0.21] = 0

# Restore molecule names
df_numeric.columns = molecule_names  # Restore column names
df_numeric.index = df.index  # Restore row names

# Directly assign the output folder
output_folder = r"/Users/parijat/Desktop/Research_Projects/7_Floridanema50_Tychonamide Analogue/FLORIDANEMAMIDE_clustering/Array_flm"
os.makedirs(output_folder, exist_ok=True)

# Ask for the output file name
output_file = input("Enter the name of the output CSV file (including .csv extension): ")

# Construct the full output file path
output_path = os.path.join(output_folder, output_file)

# Save the modified CSV
df_numeric.to_csv(output_path)

print(f"Modified CSV saved at: {output_path}")     #map4_array_mc gesim_array_mc
