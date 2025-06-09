# Nexus Testbed

This repository provides a comprehensive dataset generator designed to create synthetic datasets for various data types, including string, categorical, continuous, and heterogeneous data. The generated datasets simulate claims made by multiple sources about individuals, with configurable options to introduce predetermined amounts of known noise for robust testing scenarios.

In addition to dataset generation, the repository features a testbed for evaluating truth discovery algorithms. It supports benchmarking of the custom-developed Nexus algorithm, as well as widely-used algorithms such as Majority Voting, TruthFinder, and CRH. This enables systematic assessment and comparison of algorithmic performance on diverse and controlled datasets.

## Dataset Generation

The dataset generator is capable of creating datasets for `string`, `continuous`, `categorical`, and `heterogeneous` data. There are 2 parameters required for the generation. The number of `sources` for the dataset, and the amount of `noise` to be added (expressed in percentage).

The generator outputs files in the `datasets/` directory, organizing the content by its respective datatype. The filenames are in the format `sX_nY.json`, where `X` representes the `number of sources`, and `Y` represents the `number of entries with noise`.

To run the dataset generator, a script named `run.sh` can be used to quickly run the generator using a preset configuration or to pass specific configurations as required. The same script also allows to execute the tests described below.

### Dataset Description

- For `categorical` data, nationalities are used. The noise for this type consists of generating random country names.
- For `continuous` data, age is used. The noise consists in adding or removing years to the "true" age, with a maximum deviation of 5 years.
- For `string` data, names are used. The noise consists in either generating a new name, swapping one name by a random one, or simulate typos by removing or swapping adjacent characters.
- Lastly, `heterogeneous` data consists in a mix of the three previous data types.

## Test Execution

## Reproducibility

