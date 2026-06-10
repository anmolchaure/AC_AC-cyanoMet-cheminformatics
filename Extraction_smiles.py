import pandas as pd
import os

def extract_molecules_in_box(csv_path, output_dir, output_name, xmin, xmax, ymin, ymax):
    # Load the CSV file
    df = pd.read_csv(csv_path)

    # Define the required columns
    required_columns = {'PaCMAP1', 'PaCMAP2', 'Name', 'SMILES', 'Genus', 'Species', 'Genus_Species'}

    # Check for necessary columns regardless of order
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        print(f"Error: The CSV file is missing the following columns: {', '.join(missing_columns)}.")
        return

    # Adjust min and max values if swapped
    if xmin > xmax:
        xmin, xmax = xmax, xmin
        print(f"Swapped xmin and xmax to maintain correct range: xmin={xmin}, xmax={xmax}")
    if ymin > ymax:
        ymin, ymax = ymax, ymin
        print(f"Swapped ymin and ymax to maintain correct range: ymin={ymin}, ymax={ymax}")

    # Filter molecules that fall within the box coordinates
    filtered_df = df[(df['PaCMAP1'] >= xmin) & (df['PaCMAP1'] <= xmax) & (df['PaCMAP2'] >= ymin) & (df['PaCMAP2'] <= ymax)]

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{output_name}.csv")

    # Save the filtered molecule information to the output CSV file
    filtered_df[['Name', 'SMILES', 'Genus', 'Species', 'Genus_Species']].to_csv(output_path, index=False)
    print(f"Molecules within the specified box have been saved to {output_path}")

# Example usage
if __name__ == "__main__":
    csv_path = r"/Users/parijat/Desktop/Research_Projects/7_Floridanema50_Tychonamide Analogue/FLORIDANEMAMIDE_clustering/Output_clustering/CyanoMet_proper_coordinaties_final.csv"
    output_dir = r"/Users/parijat/Desktop/Research_Projects/7_Floridanema50_Tychonamide Analogue/FLORIDANEMAMIDE_clustering/DATABASE"
    output_name = input("Enter the output file name (without extension): ")
    xmin = float(input("Enter xmin: "))
    xmax = float(input("Enter xmax: "))
    ymin = float(input("Enter ymin: "))
    ymax = float(input("Enter ymax: "))

    extract_molecules_in_box(csv_path, output_dir, output_name, xmin, xmax, ymin, ymax)

