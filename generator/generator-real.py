"""
This module contains the main logic for generating the datasets for the testbed.
It can generate datasets based on the configuration provided and based on the 
specified level of noise.
"""

from diabetes import generate as diabetes

import argparse

SEPARATOR_LENGTH = 50
OUTPUT_DIR       = "datasets-real/"

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

    def generate(self):
        """
        Generates the dataset based on the specified parameters.
        """
        if self.noise + 1  < self.sources:
            # Initial message
            print("\n Generating dataset...")\
            # Build the outout dire for the datatype
            output_path = OUTPUT_DIR + "" + self.type + "/"
            # Check the type of dataset to generate
            if self.type == "diabetes":
                diabetes.generate(sources=self.sources, noise=self.noise, output_path=output_path)
            else:
                raise ValueError("Invalid datatype specified.")
            print("\n Dataset saved with success!")
        else:
            print("\n The number of noisy sources is greater than s-1.")

def main():
    """
    Main function to parse arguments and initiate dataset generation.
    """
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Dataset Generator ")
    # Add arguments
    parser.add_argument("-d", "--datatype",type=str,
        choices=["diabetes", "wine", "adult"],
        help="Type of data: 'diabetes', 'wine', or 'adult'"
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
