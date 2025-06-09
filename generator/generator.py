"""
This module contains the main logic for generating the datasets for the testbed.
It can generate datasets based on the configuration provided and based on the 
specified level of noise.
"""


from categorical_claims import generate_categorical_claims
from continuous_claims import generate_continuous_claims
from string_claims import generate_string_claims

import argparse
import os
import json

SEPARATOR_LENGTH = 50
OUTPUT_DIR       = "datasets/"

class Generator:
    """
    Dataset Generator Class.

    This class is responsible for generating datasets based on the specified
    parameters such as datatype, number of sources, and noise level.
    It initializes with the provided parameters and prints the settings.
    The `generate` method is intended to contain the logic for the dataset
    generation. The resulting dataset is saved to a specified output directory.
    """

    def __init__(self, datatype, sources, noise):
        self.type = datatype
        self.sources = sources
        self.noise = int(noise * sources)
        print("\n \033[1mDataset Generator\033[0m")
        print("\n > Settings:")
        print(f"     Datatype : {self.type}")
        print(f"     Sources  : {self.sources}")
        print(f"     Noise    : {self.noise} noisy sources ({int(self.noise / self.sources * 100)}%)")
        print("\n" + "=" * SEPARATOR_LENGTH)

    def _generate_string_dataset(self):
        """
        Generates a string dataset (stub implementation).
        """
        print("Generating string dataset...")
        # Initialize an empty dataset
        data = {
            "objects": [
                {
                    "name": "name",
                    "datatype": "string",
                    "truth": "",
                    "claims": []
                }
            ],
            "sources": []
        }
        # Add claims to the string object
        data["objects"][0]["claims"], truth = generate_string_claims(
            self.sources,
            self.noise
        )
        # Set the truth value for the string object
        data["objects"][0]["truth"] = truth
        # Return the dataset
        return data

    def _generate_continuous_dataset(self):
        """
        Generates a continuous dataset (stub implementation).
        """
        print("Generating continuous dataset...")
        # Initialize an empty dataset
        data = {
            "objects": [
                {
                    "name": "age",
                    "datatype": "continuous",
                    "truth": "",
                    "claims": []
                }
            ],
            "sources": []
        }
        # Add claims to the continuous object
        data["objects"][0]["claims"], truth = generate_continuous_claims(
            self.sources,
            self.noise
        )
        # Set the truth value for the string object
        data["objects"][0]["truth"] = truth
        # Return the dataset
        return data

    def _generate_categorical_dataset(self):
        """
        Generates a categorical dataset.
        """
        print("Generating categorical dataset...")
        # Initialize an empty dataset
        data = {
            "objects": [
                {
                    "name": "nationality",
                    "datatype": "categorical",
                    "truth": "",
                    "claims": []
                }
            ],
            "sources": []
        }
        # Add claims to the categorical object
        data["objects"][0]["claims"], truth = generate_categorical_claims(
            self.sources,
            self.noise
        )
        # Set the truth value for the string object
        data["objects"][0]["truth"] = truth
        # Return the dataset
        return data

    def _generate_heterogeneous_dataset(self):
        """
        Generates a heterogeneous dataset (stub implementation).
        """
        print("Generating heterogeneous dataset...")
        # Initialize an empty dataset
        data = {
            "objects": [
                {
                    "name": "name",
                    "datatype": "string",
                    "truth": "",
                    "claims": []
                },
                {
                    "name": "nationality",
                    "datatype": "categorical",
                    "truth": "",
                    "claims": []
                },
                {
                    "name": "age",
                    "datatype": "continuous",
                    "truth": "",
                    "claims": []
                }
            ],
            "sources": []
        }

        # Add string claims
        data["objects"][0]["claims"], truth = generate_string_claims(
            self.sources,
            self.noise
        )
        # Set the truth value for the string object
        data["objects"][0]["truth"] = truth

        # Add categorical claims
        data["objects"][1]["claims"], truth = generate_categorical_claims(
            self.sources,
            self.noise
        )
        # Set the truth value for the string object
        data["objects"][1]["truth"] = truth

        # Add continuous claims
        data["objects"][2]["claims"], truth = generate_continuous_claims(
            self.sources,
            self.noise
        )
        # Set the truth value for the string object
        data["objects"][2]["truth"] = truth

        # Return the dataset
        return data

    def generate(self):
        """
        Generates the dataset based on the specified parameters.
        """
        # Initial message
        print("Generating dataset...")\
        # Check the type of dataset to generate
        if self.type == "string":
            data = self._generate_string_dataset()
        elif self.type == "continuous":
            data = self._generate_continuous_dataset()
        elif self.type == "categorical":
            data = self._generate_categorical_dataset()
        elif self.type == "heterogeneous":
            data = self._generate_heterogeneous_dataset()
        else:
            raise ValueError("Invalid datatype specified.")
        # Build the outout dire for the datatype
        output_path = OUTPUT_DIR + "" + self.type + "/"
        # Save the dataset to the output directory
        print(f"Dataset generated with success! Saving to {output_path}...")
        # Ensure the output directory exists
        os.makedirs(output_path, exist_ok=True)
        # Build the output path
        output_path = os.path.join(output_path, f"s{self.sources}_n{self.noise}.json")
        # Save the dataset to the JSON file
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
        print("Dataset saved with success!")
def main():
    """
    Main function to parse arguments and initiate dataset generation.
    """
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Dataset Generator ")
    # Add arguments
    parser.add_argument("-d", "--datatype",type=str,
        choices=["string", "continuous", "categorical", "heterogeneous"],
        help="Type of data: 'string', 'continuous', 'categorical', or 'heterogeneous'"
    )
    parser.add_argument("-s", "--sources", type=int, required=True, help="Number of sources")
    parser.add_argument("-n", "--noise", type=float, help="Percentage of noise to add [0.0,1.0]")
    args = parser.parse_args()
    # Initialize generator with parameters
    generator = Generator(args.datatype,args.sources, args.noise)
    # Generate the dataset
    generator.generate()

if __name__ == "__main__":
    main()
