import pandas as pd

# Define a mapping from UF to Brazilian Region
def uf_to_region(uf):
    mapping = {
        # North
        'AC': 'North', 'AP': 'North', 'AM': 'North', 'PA': 'North', 'RO': 'North', 'RR': 'North', 'TO': 'North',
        # Northeast
        'AL': 'Northeast', 'BA': 'Northeast', 'CE': 'Northeast', 'MA': 'Northeast', 'PB': 'Northeast',
        'PI': 'Northeast', 'PE': 'Northeast', 'RN': 'Northeast', 'SE': 'Northeast',
        # Southeast
        'ES': 'Southeast', 'MG': 'Southeast', 'RJ': 'Southeast', 'SP': 'Southeast',
        # South
        'PR': 'South', 'RS': 'South', 'SC': 'South',
        # Central-West
        'DF': 'Central-West', 'GO': 'Central-West', 'MT': 'Central-West', 'MS': 'Central-West'
    }
    return mapping.get(uf, 'Unknown')

def main():
    # Load data from CSV file
    file_path = 'censo2023.csv'
    df = pd.read_csv(file_path)

    # Group data by MUNICÍPIO and UF: sum the values of "Qtde Matrículas" per municipality.
    grouped = df.groupby(['MUNICÍPIO', 'UF'], as_index=False)['Qtde Matrículas'].sum()

    # Calculating statistics per UF: minimum, maximum and average across municipalities
    uf_stats = grouped.groupby('UF')['Qtde Matrículas'].agg(['min', 'max', 'mean']).reset_index()
    uf_stats.rename(columns={'min': 'Min', 'max': 'Max', 'mean': 'Average'}, inplace=True)

    print("Statistics per UF (municipality sums):")
    print(uf_stats)

    # Map each UF to its respective Brazilian region and add as a new column.
    grouped['Region'] = grouped['UF'].apply(uf_to_region)

    # Calculating statistics per Brazilian region: min, max and average across municipalities
    region_stats = grouped.groupby('Region')['Qtde Matrículas'].agg(['min', 'max', 'mean']).reset_index()
    region_stats.rename(columns={'min': 'Min', 'max': 'Max', 'mean': 'Average'}, inplace=True)

    print("\nStatistics per Brazilian Region (municipality sums):")
    print(region_stats)

if __name__ == "__main__":
    main()
