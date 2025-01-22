import pandas as pd

def select(csv_name: str):
    """ Function for selecting each type of field to separate files

    Args:
        csv_name (str): Full name of a file with a data (extension need to be included)
    """
    db = pd.read_csv(f"./datasets/{csv_name}")
    av_types = ["tech", "hum", "lek", "sci", "ekon", "spo", "sport", "wojs"]
    
    for type in av_types:
        type_db = db.loc[db["Rodzaj kierunku"] == type]
        type_db.to_csv(f"./datasets/{type}.csv", index=False)
    
    pass