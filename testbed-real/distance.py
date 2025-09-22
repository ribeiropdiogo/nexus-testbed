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
    # Check for zero maximum to avoid division by zero
    if maximum == 0 and distance == 0:
        # If both values are zero, distance is zero
        return 0.0
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
    # Check for zero maximum to avoid division by zero
    if maximum == 0 and distance == 0:
        # If both values are zero, distance is zero
        return 0.0
    # Normalize distance
    normalized_distance = distance/maximum
    # Return normalized distance
    return normalized_distance

def cosine_distance(x: float, y: float) -> float:
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
    # Check for zero maximum to avoid division by zero
    if maximum == 0 and distance == 0:
        # If both values are zero, distance is zero
        return 0.0
    # Normalize distance
    normalized_distance = distance/maximum
    # Return normalized distance
    return normalized_distance

def squared_difference(x: float, y: float) -> float:
    """
    Calculates the squared difference between two values.
    """
    # Calculate squared difference
    squared_diff = (x - y) ** 2
    # Return similarity
    return squared_diff

def canberra_distance(x: float, y: float, epsilon: float = 1e-8) -> float:
    """
    Calculate Canberra distance between two values.
    """
    # Calculate Canberra distance
    distance = abs(x - y) / (abs(x) + abs(y) + epsilon)
    # Return similarity
    return distance
