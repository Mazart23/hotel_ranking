import pandas as pd

def convert2float(csv_name: str, column:str):
    """ Conversion a specific column to floating point type

    Args:
        csv_name (str): Full name of a file with a data (extension need to be included)
        column (str): column to convert
    """
    db = pd.read_csv(f"./datasets/{csv_name}")
    db[column] = db[column].astype(float)
    db.to_csv(f"./datasets/{csv_name}")
    return