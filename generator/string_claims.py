"""
This module contains the code to generate string claims.
"""

from numpy import add
from faker import Faker
import random
import string


def add_noise_to_string(name):
    """
    Adds noise to a string by replacing characters, adding typos, or removing characters.
    """
    name_chars = list(name)
    num_changes = random.randint(2, 3)
    # Get indices of non-space characters
    non_space_indices = [i for i, c in enumerate(name_chars) if c != ' ']
    indices = random.sample(non_space_indices, min(num_changes, len(non_space_indices)))
    # Iterate over the selected indices
    for idx in indices:
        if random.random() < 0.5:
            # Replace character
            name_chars[idx] = random.choice(string.ascii_letters)
        else:
            # Remove character
            name_chars[idx] = ''
    # Rebuild the string
    name = ''.join(name_chars)
    # Return the modified string
    return name

def generate_string_claims(sources, noise):
    """
    Generates a list of string claims.
    """
    # Initialize Faker instance
    faker = Faker()
    # Initialize an empty list for claims
    data = []
    # Initialize truth
    num_last_names = faker.random_int(min=2, max=3)
    last_names = " ".join(faker.last_name() for _ in range(num_last_names))
    truth = f"{faker.first_name()} {last_names}"
    # Iterate over the number of sources
    for i in range(sources):
        if noise > 0:
            if faker.random_int(min=1, max=10) <= 3:  # 30% chance
                num_last_names = faker.random_int(min=2, max=3)
                last_names = " ".join(faker.last_name() for _ in range(num_last_names))
                name = f"{faker.first_name()} {last_names}"
            else:
                name = add_noise_to_string(truth)
            noise -= 1
        else:
            name = truth
        entry = {
            "sourceId": f"source{i+1}",
            "fact": name
        }
        # Add entry to the list of claims
        data.append(entry)
    # Return the list of claims
    return data
