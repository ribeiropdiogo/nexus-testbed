"""
This module contains the code to generate continuous claims.
"""

from faker import Faker

def generate_continuous_claims(sources, noise):
    """
    Generates a list of continuous claims.
    """
    # Initialize Faker instance
    faker = Faker()
    # Initialize an empty list for claims
    data = []
    # Initialize truth
    truth = faker.random_int(min=25, max=35)
    # Iterate over the number of sources
    for i in range(sources):
        if noise > 0:
            age = truth + faker.random_int(min=-5, max=5)
            noise -= 1
        else:
            age = truth
        entry = {
            "sourceId": f"source{i+1}",
            "fact": age
        }
        # Add entry to the list of claims
        data.append(entry)
    # Return the list of claims
    return data
