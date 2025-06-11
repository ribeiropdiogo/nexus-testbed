"""
This module contains the logic to calculate metrics based on the similarity/distance
between the values resulting from the various algorithms and the truth.
"""

import textdistance as td

from distance import (
    euclidean_distance,
    manhattan_distance,
    canberra_distance
)

def calculate_metrics(data: dict):
    """
    Calculate metrics based on the result and truth.
    """
    # Extract truth and result
    truth = data['truth']
    result = data['result']
    # Check th edatatype and calculate metrics accordingly
    if data['datatype'] == "categorical":
        metrics = {
            "direct-comparison": 1 if truth == result else 0
        }
    elif data['datatype'] == "continuous":
        # Create a dictionary for the metrics
        metrics = {
            "euclidean-distance": euclidean_distance(float(truth), float(result)),
            "manhattan-distance": manhattan_distance(float(truth),float(result)),
            "canberra-distance": canberra_distance(float(truth),float(result)),
        }
    elif data['datatype'] == "string":
        metrics = {
            "jaro-winkler": td.jaro_winkler(str(truth),str(result)),
            "sorensen-dice": td.sorensen_dice(str(truth),str(result)),
            "damerau-levenshtein": td.damerau_levenshtein.normalized_similarity(str(truth),str(result))
        }
    else:
        # Raise an error for unknown datatype
        raise ValueError(f"Unknown datatype: {data}")

    return metrics
