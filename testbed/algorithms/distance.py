"""
This module contains various distance functions that can be used
to calculate the distance between two values.
"""

import math

def euclidean_distance(x, y):
    """
    Calculate Euclidean distance between two values.
    """
    # Apply the formula for Euclidean distance
    distance = math.sqrt((x - y) ** 2)
    # Get the maximum of the two values
    maximum = max(x, y)
    # Normalize distance
    normalized_distance = distance/maximum
    # Return normalized distance
    return normalized_distance


def manhattan_distance(x, y):
    """
    Calculate Manhattan distance between two values.
    """
    # Calculate absolute difference
    distance = abs(x - y)
    # Get the maximum of the two values
    maximum = max(x, y)
    # Normalize distance
    normalized_distance = distance/maximum
    # Return normalized distance
    return normalized_distance

def cosine_distance(x, y):
    """
    Calculate cosine distance between two values.
    """
    # Handle zero values to avoid division by zero
    if x == 0 or y == 0:
        return 1.0
    # Calculate cosine similarity
    cosine_similarity = (x * y) / (abs(x) * abs(y))
    # Calculate cosine distance
    distance = 1 - cosine_similarity
    # Get the maximum of the two values
    maximum = max(x, y)
    # Normalize distance
    normalized_distance = distance/maximum
    # Return normalized distance
    return normalized_distance
