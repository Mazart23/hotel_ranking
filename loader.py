import csv

import pandas as pd

from geolocator import get_coordinates, calc_distance


def load_data(file_path: str) -> pd.DataFrame:

    columns = [
        "Hotel_ID", "Username", "Price", "Location", "Overall_Rating", 
        "Value_Rating", "Rooms_Rating", "Location_Rating", 
        "Cleanliness_Rating", "Front_Desk_Rating", "Service_Rating", 
        "Business_Service_Rating"
    ]

    # Data filtering
    print("Data fetching...")
    clean_data = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 12:
                clean_data.append(row)
            elif len(row) == 13 and row[2] == "1":
                row.pop(2)
                clean_data.append(row)

    df = pd.DataFrame(clean_data[1:], columns=columns)

    df = df[df['Location'] != 'Unknown']

    cols = df.columns.tolist()
    price_idx, location_idx = cols.index("Price"), cols.index("Location")
    cols[price_idx], cols[location_idx] = cols[location_idx], cols[price_idx]
    df = df[cols]

    rating_columns = [col for col in df.columns if 'Rating' in col]
    df[rating_columns] = df[rating_columns].astype(int).replace(-1, 1)

    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')  # Convert to numeric, set invalid to NaN
    df = df.dropna(subset=['Price'])  # Drop rows with invalid prices
    df['Price'] = df['Price'].astype(int)  # Convert back to integer

    # Get coords based on location
    print("Coords gatchering...")
    unique_locations = df['Location'].unique()

    location_coords = {
        loc: get_coordinates(loc) for loc in unique_locations
    }

    df['Latitude'] = df['Location'].map(lambda loc: location_coords[loc][0])
    df['Longitude'] = df['Location'].map(lambda loc: location_coords[loc][1])

    df = df.dropna(subset=['Latitude', 'Longitude'])

    df['Distance_From_Kraków'] = df.apply(calc_distance, axis=1)

    df = df.drop(columns=['Latitude', 'Longitude', 'Username'])

    print('Dataframe:\n', df.head())
    print('\nDataframe length:', len(df))
    print('\nDataframe describe:\n', df.describe())
    
    output_file = "cleaned_data.csv"
    df.to_csv(output_file, index=False)

      # Aggregation for each hotel
    print("Aggregating data...")
    aggregated_df = df.groupby('Hotel_ID').agg({
        'Location': 'first',
        'Price': 'mean',
        'Overall_Rating': 'mean',
        'Value_Rating': 'mean',
        'Rooms_Rating': 'mean',
        'Location_Rating': 'mean',
        'Cleanliness_Rating': 'mean',
        'Front_Desk_Rating': 'mean',
        'Service_Rating': 'mean',
        'Business_Service_Rating': 'mean',
        'Distance_From_Kraków': 'first'
    }).reset_index()

    # Add the Number_Of_Opinions column
    aggregated_df['Number_Of_Opinions'] = df.groupby('Hotel_ID').size().values

    # Round numerical columns to 2 decimal places where applicable
    ratings_columns = [col for col in aggregated_df.columns if 'Rating' in col or col == 'Price']
    aggregated_df[ratings_columns] = aggregated_df[ratings_columns].round(2)

    print('Aggregated Dataframe:\n', aggregated_df.head())
    print('\nAggregated Dataframe length:', len(aggregated_df))
    
    output_file = "cleaned_aggregated_data.csv"
    aggregated_df.to_csv(output_file, index=False)

    return aggregated_df

db = load_data("./datasets/reviews.dat")