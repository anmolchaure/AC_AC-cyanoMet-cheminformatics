import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

# === Step 1: Load the similarity matrix ===
file_path = r"/Users/parijat/Desktop/Research_Projects/7_Floridanema50_Tychonamide Analogue/FLORIDANEMAMIDE_clustering/Array_flm/Microviridin_Tyc_cluster_array.csv"
df = pd.read_csv(file_path, index_col=0)

# === Step 2: Flatten full matrix and remove diagonal values (1.0) ===
flattened_all = df.values.flatten()
flattened_all = flattened_all[flattened_all != 1]

# === Step 3: Plot full matrix distribution ===
fig_full = px.histogram(
    x=flattened_all, 
    nbins=50,
    opacity=0.7,
    marginal="box",
    histnorm="probability density",
    title="Distribution of Tanimoto Similarity Values",
    labels={"x": "Similarity Value"}
)
fig_full.update_layout(bargap=0.1)
fig_full.write_html(r"/Users/parijat/Desktop/Research_Projects/7_Floridanema50_Tychonamide Analogue/FLORIDANEMAMIDE_clustering/Array_flm/Microviridin_Tychonamide_cluster.html")

# === Step 4: Extract upper triangle only (no redundancy) ===
upper_tri_values = df.where(np.triu(np.ones(df.shape), k=1).astype(bool)).stack()

# === Step 5: Compute statistics ===
mean_sim = upper_tri_values.mean()
median_sim = upper_tri_values.median()
var_sim = upper_tri_values.var()
std_sim = upper_tri_values.std()
percentile_75 = np.percentile(upper_tri_values, 75)
threshold_ = mean_sim+std_sim

print("Mean Similarity:", mean_sim)
print("Median Similarity:", median_sim)
print("Variance of Similarity:", var_sim)
print("Standard Deviation:", std_sim)
print("75th Percentile Threshold:", percentile_75)
print ("threshold:", threshold_)



