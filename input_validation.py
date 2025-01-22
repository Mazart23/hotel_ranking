from typing import List
import re
import numpy as np

def validate(weights, regex) -> bool:
    """ Check if input is valid

    Args:
        weights (List[str]): list containing weights from user
        regex (str): regex to match with weights

    Returns:
        bool: is validate
    """
    
    result = np.array([re.match(regex, text) for text in weights])
    return np.all(result)
