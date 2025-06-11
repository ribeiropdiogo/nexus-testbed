# Nexus Testbed

This repository provides a comprehensive dataset generator designed to create synthetic datasets for various data types, including string, categorical, continuous, and heterogeneous data. The generated datasets simulate claims made by multiple sources about individuals, with configurable options to introduce predetermined amounts of known noise for robust testing scenarios.

In addition to dataset generation, the repository features a testbed for evaluating truth discovery algorithms. It supports benchmarking of the custom-developed Nexus algorithm, as well as widely-used algorithms such as Majority Voting, TruthFinder, and CRH. This enables systematic assessment and comparison of algorithmic performance on diverse and controlled datasets.

## Dataset Generation

The dataset generator is capable of creating datasets for `string`, `continuous`, `categorical`, and `heterogeneous` data. There are 2 parameters required for the generation. The number of `sources` for the dataset, and the amount of `noise` to be added (expressed in percentage).

The generator outputs files in the `datasets/` directory, organizing the content by its respective datatype. The filenames are in the format `sX_nY.json`, where `X` represents the `number of sources`, and `Y` represents the `number of entries with noise`.

To run the dataset generator, a script named `run.sh` can be used to quickly run the generator using a preset configuration or to pass specific configurations as required. The same script also allows to execute the tests described below.

### Dataset Description

- For `categorical` data, nationalities are used. The noise for this type consists of generating random country names.
- For `continuous` data, age is used. The noise consists in adding or removing years to the "true" age, with a maximum deviation of 5 years.
- For `string` data, names are used. The noise consists in either generating a new name, swapping one name by a random one, or simulate typos by removing or swapping adjacent characters.
- Lastly, `heterogeneous` data consists in a mix of the three previous data types.

## Test Execution

In order to execute the tests, a dataset is required to be previously generated. Other directories than the default `datasets/` can be used. The testbed can be executed using the supplied scripts `testbed.sh` and `run.sh` (more information below). There are four algorithms being used in the assessment: `Majority Voting`, `TruthFinder`, `CRH`, and `Nexus`. For each algorithm, a predetermined number of rounds is executed (5 by default). This value can be changed in the `testbed.sh` script by updating the `ROUNDS` variable. Moreover, in each execution, the claims are shuffled to ensure that their order does not affect the final result. The results of the testbed are saved into the `results/` directory, organized by datatype. The filenames are in the format `sX_nY_Z.json`, where `X` represents the `number of sources`, `Y` represents the `number of entries with noise`, and `Z` represents the `round` (`[1,ROUNDS]`).

### Requirements

Before running the tests, there are two requirements that need to be met. First, the required `Python` dependencies have to be installed. To do so, run the command below at the root of the project:

```bash
pip install -r requirements.txt
```

Second, `Nexus` has to be running. To launch it, `Docker` can be used. At the root of the repository of `Nexus`, run the following command to launch it:

```bash
docker compose up --build -d
```

### Output Format

The output format, represented below, includes information on the algorithm used, and for each datatype, it includes the output of the algorithm, the expected result (truth), and the respective metrics. For `categorical` data, `direct comparison` is used (1 if the values are equal, and 0 otherwise). For `string` data, `Jaro-Winkler`, `Sorensen-Dice`, and `Damerau-Levenshtein` are used to measure similarity. For `continuous` values, `Euclidean`, `Manhattan`, and `Canberra` distances are used.

```json
{
    "algorithm": "Majority Voting",
    "results": [
        {
            "result": "Gabriel Arias York",
            "truth": "Gabriel Arias York",
            "datatype": "string",
            "metrics": {
                "jaro-winkler": 1,
                "sorensen-dice": 1,
                "damerau-levenshtein": 1.0
            }
        },
        {
            "result": "Niger",
            "truth": "Niger",
            "datatype": "categorical",
            "metrics": {
                "direct-comparison": 1
            }
        },
        {
            "result": 27,
            "truth": 27,
            "datatype": "continuous",
            "metrics": {
                "euclidean-distance": 0.0,
                "manhattan-distance": 0.0,
                "canberra-distance": 0.0
            }
        }
    ]
}
```

### Statistics

In order to better understand the results of the testbed, detailed statistics are generated into the `stats/` directory. The format, as shown below, includes information on the average similarities for each datatype. All similarity values are normalized between 0 and 1.

```json
{
    "test": "s15_n9",
    "rounds": 5,
    "datatype": "heterogeneous",
    "average similiarty": 0.7545427496009688,
    "categorical": {
        "average similarity": 0.4
    },
    "continuous": {
        "average similarity": 0.9568379893840886,
        "average euclidean similarity": 0.9487082670906201,
        "average manhattan similarity": 0.9487082670906201,
        "average canberra similarity": 0.9730974339710257
    },
    "string": {
        "average similarity": 0.906790259418818,
        "average jaro-winkler similarity": 0.8877343090346186,
        "average sorensen-dice similarity": 0.9326364692218352,
        "average damerau-levenshtein similarity": 0.9
    }
}
```

## Reproducibility

In order to achieve the exact same results, we included the necessary scripts to run the tests on the dataset we used, which is located at `datasets/`. To reproduce the results, execute the `reproducibility.sh` script.

## Authors

- **Author information is omitted at this stage to preserve anonymity.**

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
