import numpy as np
import pandas as pd
from typing import List

def normalize(matrix: np.ndarray) -> np.ndarray:
    """Normalize a matrix using min-max scaling."""
    return (matrix - np.min(matrix, axis=0)) / (np.max(matrix, axis=0) - np.min(matrix, axis=0))

def voronoi_segments(start: np.ndarray, end: np.ndarray) -> np.ndarray:
    """Calculate the Voronoi-like segments between start and end in 3D."""
    k = len(start)  # Dimensions
    distances = (end - start) / 2
    breakpoints = [start]
    for i in range(1, k + 1):
        segment_start = start + np.sum(distances[:i]) * np.eye(k)[i-1]
        breakpoints.append(segment_start)
    breakpoints.append(end)
    return np.array(breakpoints)

def calculate_distances(point: np.ndarray, curve: np.ndarray) -> float:
    """Calculate the distance from a point to the curve."""
    distances = [np.linalg.norm(point - segment) for segment in curve]
    return min(distances)

def safety_score(aspiration_points: np.ndarray, status_quo_points: np.ndarray, evaluation_points: np.ndarray) -> List[float]:
    """Calculate the Safety Principle scores for evaluation points."""
    scores = []
    for eval_point in evaluation_points:
        total_score = 0
        for aspiration in aspiration_points:
            for status_quo in status_quo_points:
                voronoi_curve = voronoi_segments(status_quo, aspiration)
                shortest_distance = calculate_distances(eval_point, voronoi_curve)
                total_score += shortest_distance
        scores.append(total_score)
    return scores

def gui_spcs(df: pd.DataFrame, additional_params) -> pd.DataFrame:
    """
    GUI function for Safety Principle scoring.
    - df: DataFrame containing hotel data.
    - additional_params: Parameters passed, expected to include:
      - 'criteria': The 3D criteria for the analysis (e.g., ['Price', 'Overall_Rating', 'Value_Rating']).
    """
    criteria = additional_params.get('criteria', ["Price", "Overall_Rating", "Value_Rating"])
    
    selected_data = df[criteria].to_numpy()

    normalized_data = normalize(selected_data)

    aspiration_points = np.array([np.max(normalized_data, axis=0)])  # Top performers
    status_quo_points = np.array([np.min(normalized_data, axis=0)])  # Bottom performers

    df['SAFETY_PRINCIPAL_score'] = safety_score(aspiration_points, status_quo_points, normalized_data)
    return df