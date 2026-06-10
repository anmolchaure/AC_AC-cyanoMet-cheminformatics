import pandas as pd
import numpy as np

# === Step 1: Load your similarity matrix ===
file_path = r"/Users/parijat/Desktop/Molecular Similarity Final/Similarity_Networks/GESim_Array/gesim_array_mc8TH99.csv"
df = pd.read_csv(file_path, index_col=0)

# === Step 2: Flatten the matrix ===
all_values = df.values.flatten()

# === Step 3: Keep only valid numerical values ===
numerical_values = all_values[np.isfinite(all_values)]  # Removes NaN or inf

# === Step 4: Filter non-zero values only ===
non_zero_values = numerical_values[numerical_values != 0]

# === Step 5: Compute statistics on non-zero values ===
summary = {
    "Total non-zero values": len(non_zero_values),
    "Mean (non-zero)": np.mean(non_zero_values),
    "Median (non-zero)": np.median(non_zero_values),
    "Variance (non-zero)": np.var(non_zero_values),
    "Standard Deviation (non-zero)": np.std(non_zero_values)
}

# === Step 6: Print the results ===
for key, value in summary.items():
    print(f"{key}: {value}")
