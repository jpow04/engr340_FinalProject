import pandas as pd
import matplotlib.pyplot as plt
import os


# Load the CSV file
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None


# Convert damage values so spreadsheet works
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


# Analyze data across multiple years
def analyze_10_years(directory):
    combined_data = pd.DataFrame()

    # Iterate through all CSV files for years 2023 to 2014
    for year in range(2023, 2013, -1):
        file_name = f"StormEvents_details-ftp_v1.0_d{year}.csv"
        file_path = os.path.join(directory, file_name)
        data = load_data(file_path)
        if data is not None:
            # Damage columns conversion
            for column in ['DAMAGE_PROPERTY', 'DAMAGE_CROPS']:
                if column in data.columns:
                    data[column] = data[column].apply(convert_damage)
            data['YEAR'] = year
            combined_data = pd.concat([combined_data, data], ignore_index=True)

    return combined_data


# Graph the 10 most impactful storm types over 10 years
def graph_impact_over_time(data, impact_column, title, ylabel):
    # Group data by storm type and year
    grouped = data.groupby(['EVENT_TYPE', 'YEAR'])[impact_column].sum().reset_index()

    # Get the 10 most impactful storm types
    total_impact = grouped.groupby('EVENT_TYPE')[impact_column].sum()
    top_10_storms = total_impact.sort_values(ascending=False).head(10).index

    # Filter data for the top 10 storm types
    top_10_data = grouped[grouped['EVENT_TYPE'].isin(top_10_storms)]

    # Plot each storm type
    plt.figure(figsize=(12, 8))
    for storm in top_10_storms:
        storm_data = top_10_data[top_10_data['EVENT_TYPE'] == storm]
        plt.plot(storm_data['YEAR'], storm_data[impact_column], marker='o', label=storm)

    plt.title(title)
    plt.xlabel('Year')
    plt.xticks(range(2014, 2024))  # Ensure all years are labeled
    plt.ylabel(ylabel)
    plt.legend(title="Storm Types", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Define the directory containing the data
    path_to_directory = "./data/"

    # Analyze data across 10 years
    combined_data = analyze_10_years(path_to_directory)

    # Graph the impact of the top 10 storm types over time
    graph_impact_over_time(combined_data, 'DEATHS_DIRECT', "Direct Deaths Over 10 Years", "Death Count")
    graph_impact_over_time(combined_data, 'DAMAGE_PROPERTY', "Property Damage Over 10 Years", "Damage Amount (USD)")
