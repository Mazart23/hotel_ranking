from UTA.uta import *
import numpy as np
import pandas as pd 
pd.options.mode.chained_assignment = None  # default='warn'
import matplotlib.pyplot as plt

def uta(df, max_or_min):
    # Select relevant criteria columns for evaluation
    criteria = df[["Price", "Overall_Rating", "Value_Rating", 
                    "Rooms_Rating", "Location_Rating", 
                    "Cleanliness_Rating", "Front_Desk_Rating", 
                    "Service_Rating", "Business_Service_Rating", "Number_Of_Opinions"]]
    
    # Rename columns to shorter names for convenience
    criteria.rename(columns={
        "Price": "Price", 
        "Overall_Rating": "OR", 
        "Value_Rating": "VR", 
        "Rooms_Rating": "RR", 
        "Location_Rating": "LR", 
        "Cleanliness_Rating": "CR", 
        "Front_Desk_Rating": "FR", 
        "Service_Rating": "SR", 
        "Business_Service_Rating": "BSR",
        "Number_Of_Opinions": "NO"
    }, inplace=True)

    # Prepare points as a NumPy array
    points = []
    for _, row in criteria.iterrows():
        points.append([row.Price, row.OR, row.VR, row.RR, row.LR, row.CR, row.FR, row.SR, row.BSR, row.NO])
    points = np.array(points)

    # Get min and max for normalization
    min_vals, max_vals = get_min_max(points)

    # Convert max_or_min (maximize/minimize) to binary flags
    max_or_min = np.where(max_or_min == "min", 0, 1)

    # Define utility functions manually or proportionally
    func_utility = [
        [0.2, 0.02, 0],  # Price (minimize)
        [0.2, 0.16, 0.12, 0.08, 0],  # Overall Rating
        [0.2, 0.16, 0.12, 0.08, 0],  # Value Rating
        [0.2, 0.16, 0.12, 0.08, 0],  # Rooms Rating
        [0.2, 0.16, 0.12, 0.08, 0],  # Location Rating
        [0.2, 0.16, 0.12, 0.08, 0],  # Cleanliness Rating
        [0.2, 0.16, 0.12, 0.08, 0],  # Front Desk Rating
        [0.2, 0.16, 0.12, 0.08, 0],  # Service Rating
        [0.2, 0.16, 0.12, 0.08, 0],  # Business Service Rating
        [0.2, 0.02, 0]
    ]

    # Divide ranges into compartments
    compartments = split(min_vals, max_vals, np.array([2, 4, 4, 4, 4, 4, 4, 4, 4, 2]), max_or_min, func_utility)

    # Compute utility function values
    u = [function_value(compartments[i], max_or_min[i]) for i in range(len(compartments))]

    # Rank alternatives based on utility scores
    scores = [rank(u, compartments, point) for point in points]

    df["UTA_score"] = scores

    return df

    
