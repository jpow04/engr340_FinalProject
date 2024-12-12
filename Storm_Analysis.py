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


# Convert damage values to read spreadsheet properly
def convert_damage(value):
    if isinstance(value, str):
        if value.endswith('B'):
            return float(value[:-1]) * 1e9  # 1 billion
        elif value.endswith('M'):
            return float(value[:-1]) * 1e6  # 1 million
        elif value.endswith('K'):
            return float(value[:-1]) * 1e3  # 1 thousand
        else:
            return float(value.replace('$', '').strip())  # Remove interfering characters
    return float(value)


# Analyze data across entire dataset
def analyze_dataset(directory):
    combined_data = pd.DataFrame()  # Establish dataframe for 10 year data period

    # Iterate through all CSV files for years 2023 to 2014
    for year in range(2023, 2013, -1):
        file_name = f"StormEvents_details-ftp_v1.0_d{year}.csv"  # csv file-names
        file_path = os.path.join(directory, file_name)
        data = load_data(file_path)
        if data is not None:  # Check if data loaded properly
            # Damage column conversion
            for column in ['DAMAGE_PROPERTY', 'DAMAGE_CROPS']:
                if column in data.columns:
                    data[column] = data[column].apply(convert_damage)
            data['YEAR'] = year  # Identity dataset year
            combined_data = pd.concat([combined_data, data], ignore_index=True)  # Combine datasets into single dataframe

        # Group and sum by storm type
    combined_summary = {
        'Direct Deaths': combined_data.groupby('EVENT_TYPE')['DEATHS_DIRECT'].sum(),
        'Property Damage': combined_data.groupby('EVENT_TYPE')['DAMAGE_PROPERTY'].sum()
    }
    for category, data in combined_summary.items():
        print(f"\nMost impactful storm types for {category} over 10 years:")
        sorted_data = data.sort_values(ascending=False)
        for event_type, value in sorted_data.head(10).items():  # Print the 10 most damaging storms
            print(f"{event_type} caused {value:.2f} {category.lower()}.")

    return combined_data


# Graph the 10 most impactful storm types over 10 years
def graph_impact_over_time(data, impact_column, title, ylabel):
    # Group data by storm type and year, adding storm impact value
    grouped = data.groupby(['EVENT_TYPE', 'YEAR'])[impact_column].sum().reset_index()

    # Get the 10 most impactful storm types
    total_impact = grouped.groupby('EVENT_TYPE')[impact_column].sum()  # Add impact value for each storm type
    top_10_storms = total_impact.sort_values(ascending=False).head(10).index  # Identify 10 most impactful storms

    # Filter data for the top 10 storm types
    top_10_data = grouped[grouped['EVENT_TYPE'].isin(top_10_storms)]

    # Plot each storm type for each year
    plt.figure(figsize=(12, 8))
    for storm in top_10_storms:
        storm_data = top_10_data[top_10_data['EVENT_TYPE'] == storm]  # Select storm type
        plt.plot(storm_data['YEAR'], storm_data[impact_column], marker='o', label=storm)  # Plot each storm type for each year

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
    combined_data = analyze_dataset(path_to_directory)

    # Graph the impact of the top 10 storm types over time
    graph_impact_over_time(combined_data, 'DEATHS_DIRECT', "Direct Deaths Over 10 Years", "Death Count")
    graph_impact_over_time(combined_data, 'DAMAGE_PROPERTY', "Property Damage Over 10 Years", "Damage Cost (10 Billion Dollars)")
