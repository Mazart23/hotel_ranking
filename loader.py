import csv

import pandas as pd

from geolocator import get_coordinates


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

    # Get coords based on location
    print("Coords gatchering...")
    unique_locations = df['Location'].unique()

    location_coords = {
        loc: get_coordinates(loc) for loc in unique_locations
    }

    df['Latitude'] = df['Location'].map(lambda loc: location_coords[loc][0])
    df['Longitude'] = df['Location'].map(lambda loc: location_coords[loc][1])

    print('Dataframe:\n', df.head())
    print('\nDataframe length:', len(df))
    print('\nDataframe describe:\n', df.describe())
    
    return df