import pacmap
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.io as pio
import os

# ---- GLOBAL PLOT STYLE ---- #
pio.templates.default = "simple_white"  # clean white background

# ---- FILE PATHS ---- #
input_file_path = r"/Users/parijat/Desktop/Research_Projects/7_Floridanema50_Tychonamide Analogue/FLORIDANEMAMIDE_clustering/Array_flm/CyanoMet_ALL_TH21.csv"
genus_file_path = r"/Users/parijat/Desktop/Research_Projects/7_Floridanema50_Tychonamide Analogue/FLORIDANEMAMIDE_clustering/DATABASE/cynometdbV3_2024_with_trichonew.csv"
output_directory = r"/Users/parijat/Desktop/Research_Projects/7_Floridanema50_Tychonamide Analogue/FLORIDANEMAMIDE_clustering/Output_clustering"

# ---- LOAD SIMILARITY MATRIX ---- #
similarity_df = pd.read_csv(input_file_path, index_col=0)

# 🔴 CRITICAL FIX: force numeric
similarity_df = similarity_df.apply(pd.to_numeric, errors='coerce')

similarity_df.index = similarity_df.index.str.strip()
similarity_df.columns = similarity_df.columns.str.strip()
similarity_df.index.name = "Name"

# Optional: keep only valid similarity values
similarity_df = similarity_df.clip(lower=0, upper=1)

# ---- LOAD GENUS INFO ---- #
genus_df = pd.read_csv(genus_file_path, encoding='utf-8')[
    ['Name', 'Genus', 'Species', 'SMILES', 'Genus_Species']
]
genus_df['Name'] = genus_df['Name'].str.strip()

# ---- MERGE ---- #
merged_df = pd.merge(
    similarity_df.reset_index(),
    genus_df,
    on='Name',
    how='left'
).set_index('Name')

# ---- FEATURES ---- #
feature_cols = merged_df.drop(columns=['Genus', 'Species', 'SMILES', 'Genus_Species'])

# ---- STANDARDIZE & PCA ---- #
scaler = StandardScaler()
scaled_data = scaler.fit_transform(feature_cols.values)

pca = PCA(n_components=10)
pca_result = pca.fit_transform(scaled_data)

# ---- PaCMAP ---- #
n_neighbors = int(input("Enter the number of neighbors for PaCMAP (e.g., 15): ").strip())
num_iters = 2000

pacmap_model = pacmap.PaCMAP(
    n_neighbors=n_neighbors,
    num_iters=num_iters,
    random_state=42
)

pacmap_result = pacmap_model.fit_transform(pca_result)

print(f"✅ PaCMAP completed with {n_neighbors} neighbors and {num_iters} iterations.")

# ---- Silhouette Score ---- #
kmeans = KMeans(n_clusters=5, random_state=42, n_init=20)
cluster_labels = kmeans.fit_predict(pacmap_result)

silhouette_avg = silhouette_score(pacmap_result, cluster_labels)
print(f"Silhouette Score after PCA+PaCMAP: {silhouette_avg:.3f}")

# ---- FINAL DF ---- #
pacmap_df = pd.DataFrame(
    pacmap_result,
    columns=['PaCMAP1', 'PaCMAP2'],
    index=merged_df.index
)

pacmap_df['Genus'] = merged_df['Genus']
pacmap_df['Species'] = merged_df['Species']
pacmap_df['Genus_Species'] = merged_df['Genus_Species']
pacmap_df['SMILES'] = merged_df['SMILES']

# ---- OUTPUT NAME ---- #
base_filename = input("Enter the base filename for the plots: ").strip()

# ---- SAVE DATA ---- #
output_csv = os.path.join(output_directory, f"{base_filename}_PaCMAP_coordinates.csv")
pacmap_df.reset_index().to_csv(output_csv, index=False)
print(f"✅ Coordinates saved: {output_csv}")

# ---- COLORBLIND FRIENDLY PALETTE ---- #
color_palette = px.colors.qualitative.Safe

# ---- 2D PLOT ---- #
fig_2d = px.scatter(
    pacmap_df,
    x='PaCMAP1',
    y='PaCMAP2',
    color='Genus_Species',
    color_discrete_sequence=color_palette,
    hover_name=pacmap_df.index,
    hover_data={
        'Genus': True,
        'Species': True,
        'Genus_Species': False,
        'PaCMAP1': False,
        'PaCMAP2': False
    },
    title=f"PaCMAP projection of cyanobacterial metabolites (Threshold=0.21) (n={n_neighbors}, silhouette={silhouette_avg:.2f})"
)

# ---- CLEAN LAYOUT ---- #
fig_2d.update_layout(
    legend_title_text='Genus + Species',
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(r=150),
    font=dict(size=14)
)

fig_2d.update_traces(marker=dict(size=6, opacity=0.8))

output_2d = os.path.join(
    output_directory,
    f"{base_filename}_PaCMAP_2D_n{n_neighbors}_s{silhouette_avg:.2f}.html"
)

fig_2d.write_html(output_2d)
print(f"✅ 2D plot saved: {output_2d}")

# ---- 3D PLOT ---- #
pacmap_model_3d = pacmap.PaCMAP(
    n_neighbors=n_neighbors,
    n_components=3,
    random_state=42
)

pacmap_3d = pacmap_model_3d.fit_transform(pca_result)

pacmap_df_3d = pd.DataFrame(
    pacmap_3d,
    columns=['PaCMAP1', 'PaCMAP2', 'PaCMAP3'],
    index=merged_df.index
)

pacmap_df_3d['Genus'] = merged_df['Genus']

fig_3d = px.scatter_3d(
    pacmap_df_3d,
    x='PaCMAP1',
    y='PaCMAP2',
    z='PaCMAP3',
    color='Genus',
    color_discrete_sequence=color_palette,
    hover_name=pacmap_df_3d.index,
    title=f"3D PaCMAP (n={n_neighbors})"
)

fig_3d.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Optional save
# output_3d = os.path.join(output_directory, f"{base_filename}_PaCMAP_3D.html")
# fig_3d.write_html(output_3d)