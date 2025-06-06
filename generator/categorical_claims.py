"""
This module contains the code to generate categorical claims.
"""

from faker import Faker

def generate_categorical_claims(sources, noise):
    """
    Generates a list of categorical claims.
    """
    # Initialize Faker instance
    faker = Faker()
    # Initialize an empty list for claims
    data = []
    # Initialize truth
    truth = faker.country()
    # Iterate over the number of sources
    for i in range(sources):
        if noise > 0:
            nationality = faker.country()
            noise -= 1
        else:
            nationality = truth
        entry = {
            "sourceId": f"source{i+1}",
            "fact": nationality
        }
        # Add entry to the list of claims
        data.append(entry)
    # Return the list of claims
    return data
