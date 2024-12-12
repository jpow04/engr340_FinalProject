import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

# Make sure that parsing properly reads spreadsheet values
def convert_damage(value):
    if isinstance(value, str):
        if value.endswith('B'):
            return float(value[:-1]) * 1e9
        elif value.endswith('M'):
            return float(value[:-1]) * 1e6
        elif value.endswith('K'):
            return float(value[:-1]) * 1e3
        else:
            return float(value.replace('$', '').strip())
    return float(value)

# Analyze data by category
def storm_impact(data):
    # Fix damage columns and make sure pandas reads them properly
    for column in ['DAMAGE_PROPERTY', 'DAMAGE_CROPS']:
        if column in data.columns:
            data[column] = data[column].apply(convert_damage)

    # Group and sum by storm type in a dictionary
    impact_summary = {
        'Direct Injuries': data.groupby('EVENT_TYPE')['INJURIES_DIRECT'].sum().sort_values(ascending=False),
        'Direct Deaths': data.groupby('EVENT_TYPE')['DEATHS_DIRECT'].sum().sort_values(ascending=False),
        'Property Damage': data.groupby('EVENT_TYPE')['DAMAGE_PROPERTY'].sum().sort_values(ascending=False),
        'Crop Damage': data.groupby('EVENT_TYPE')['DAMAGE_CROPS'].sum().sort_values(ascending=False)
    }

    return impact_summary


# Plot results
def plot_results(results):
    # Injuries and Deaths Graph
    plt.figure(figsize=(12, 6))
    plt.plot(results['Direct Injuries'], label='Direct Injuries', marker='o')
    plt.plot(results['Direct Deaths'], label='Direct Deaths', marker='o')
    plt.title('Injuries and Deaths by Storm Type')
    plt.xlabel('Storm Type')
    plt.ylabel('Count')
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Damage Graph
    plt.figure(figsize=(12, 6))
    plt.plot(results['Property Damage'], label='Property Damage', marker='o')
    plt.plot(results['Crop Damage'], label='Crop Damage', marker='o')
    plt.title('Property and Crop Damage by Storm Type')
    plt.xlabel('Storm Type')
    plt.ylabel('Damage (USD)')
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Print results
def print_results(results):
    for category, data in results.items():
        print(f"\nTop storm types for {category}:")
        for event_type, value in data.head(20).items():
            print(f"{event_type} caused {value:.2f} {category.lower()}.")

if __name__ == "__main__":
    # Define the directory and file name
    path_to_directory = "./data/"
    file_name = "StormEvents_details-ftp_v1.0_d2017.csv"
    file_path = path_to_directory + file_name

    storm_data = load_data(file_path)

    if storm_data is not None:
        results = storm_impact(storm_data)
        print_results(results)
        plot_results(results)

