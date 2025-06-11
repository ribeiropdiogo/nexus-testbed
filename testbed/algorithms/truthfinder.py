"""
This module contains the code responsible for the implementation
of the TruthFinder algorithm proposed by Yin et al. used for data
consolidation purposes.
"""
import sys
import random
import json
import math
import warnings
from decimal import Decimal, getcontext
import numpy as np
import pandas as pd
from numpy.linalg import norm

getcontext().prec = 125

from metrics import calculate_metrics

warnings.filterwarnings("error")

def euclidean_distance(x,y):
    """
    Calculate the Euclidean distance between two vectors.
    """
    return np.sqrt(sum(pow(float(a)-float(b),2) for a, b in zip(x, y)))

# Damerau – Levenshtein: optimal string alignment distance
def optimal_string_alignment_distance(f1, f2):
    """
    Calculate the Damerau–Levenshtein optimal string alignment distance
    between two strings.
    """
	# Create a table to store the results of subproblems
    dp = [[0 for j in range(len(f2)+1)] for i in range(len(f1)+1)]

	# Initialize the table
    for i in range(len(f1)+1):
        dp[i][0] = i
    for j in range(len(f2)+1):
        dp[0][j] = j

	# Populate the table using dynamic programming
    for i in range(1, len(f1)+1):
        for j in range(1, len(f2)+1):
            if f1[i-1] == f2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

	# Return the edit distance
    return dp[len(f1)][len(f2)]

def continuous_implication(f1, f2):
    """
    This function calculates the implication between two continuous values.
    """
    # Get the maximum between f1 and f2
    max_value = max(f1,f2)
    # Calculate the euclidean distance
    distance =  euclidean_distance([f1],[f2])
    # Normalize between -1 and 1
    i = 2 * ((float(distance)-float(max_value))/(0-float(max_value))) - 1
    # Return the normalized value
    return i

def categorical_implication(f1, f2):
    """
    This function calculates the implication between two categorical values.
    """
    # Both facts are equal
    if f1 == f2:
        # If f1 is correct, f2 is likely to be correct
        return 1
    else:
        # The facts are differents
        # If f1 is correct, f2 is likely to be wrong
        return -1

def string_implication(f1, f2):
    """
    This function calculates the implication between two strings
    """
    # Get the length of f1
    size = len(f1)
    # Calculate the Damerau–Levenshtein optimal string alignment distance
    distance =  optimal_string_alignment_distance(f1,f2)
    # Normalize between -1 and 1
    i = 2 * ((distance-size)/(0-size)) - 1
    # Return the normalized value
    return i

def sigmoid(x):
    """
    This function is included to avoid possible negative confidence scores.

            Parameters:
                    x (float): Product of dampening factor and fact confidence

            Returns:
                    confidence (float): Confidence score of the fact
    """
    # Avoid negative values (Eq. 8)
    x = Decimal(1 / (Decimal(1) + Decimal(math.exp(-x))))
    if x == 0 or x == 1:
        # Raise an error
        raise ValueError("Sigmoid function returned 0 or 1. Check precision.")
    # Return the sigmoid function value
    return x

class TruthFinder(object):
    """
    The TruthFinder represents the algorithm and includes all the necessary
    logic to compute the fact confidences and trustworthiness scores.

    Attributes
    ----------
    implication : function
        implication function returning a value between -1 and 1
    dampening_factor : float
        dampening factor
    influence_related : float
        influence between related facts

    Methods
    -------
    confidence_score(df):
        Calculates the confidence scores.
    adjusted_confidence_score(df):
        Calculates the adjusted confidence scores.
    compute_fact_confidence(df):
        Calculates the fact confidence.
    update_fact_confidence(df):
        Updates the fact confidence.
    update_source_trustworthiness(df):
        Updates the source trustworthiness.
    iteration(df):
        Performs an iteration.
    stop_condition(t1,t2,threshold):
        Verifies if stop condition is met.
    run(dataframe,max_iterations=200,threshold=1e-6,initial_trustworthiness=0.9):
        Executes the algorithm.
    """
    def __init__(self,dampening_factor=0.3,influence_related=0.5):
        # Verify if values are in the accepted interval
        assert 0 < dampening_factor < 1
        assert 0 <= influence_related <= 1
        # Initialize values
        self.dampening_factor = dampening_factor
        self.influence_related = influence_related

    def confidence_score(self, df):
        """
        This function calculates the confidence scores.

                Parameters:
                        df (dataframe): Dataframe containing the sources,
                            facts, objects, trustworthiness and fact confidence

                Returns:
                        df (datafram): Dataframe with new confidence scores
        """
        # Trustworthiness score of source (Eq. 3)
        trustworthiness_score = lambda x: -math.log(1-x)
        # Calculate confidence for each fact
        for i, row in df.iterrows():
            # Get the trustworthiness score of each source providing f
            ts = df.loc[df["fact"] == row["fact"], "trustworthiness"]
            # Sum the trustworthiness score of each source providing f (Eq. 5)
            confidence_score = sum(trustworthiness_score(t) for t in ts)
            # Set the calculate confidence for the fact
            df.at[i, "fact_confidence"] = confidence_score
        # Return the data
        return df

    def adjusted_confidence_score(self, df):
        """
        This function calculates the adjusted confidence scores.

                Parameters:
                        df (dataframe): Dataframe containing the sources,
                            facts, objects, trustworthiness and fact confidence

                Returns:
                        df (datafram): Dataframe with adjusted confidence scores
        """
        adjusted = {}
        # Iterate through the facts
        for i, row1 in df.iterrows():
            # Get the first fact
            f1 = row1["fact"]
            # Initialize the sum
            sum = 0
            # Iterate through the facts
            for j, row2 in df.drop_duplicates("fact").iterrows():
                # Get the second fact
                f2 = row2["fact"]
                # Compare the facts
                if f1 == f2:
                    # Ignore if they are the same facts
                    continue
                if row1["datatype"] == "continuous":
                    # Add the product between confidence score of f2 and implication
                    sum += row2["fact_confidence"] * continuous_implication(f2, f1)
                elif row1["datatype"] == "string":
                    sum += row2["fact_confidence"] * string_implication(f2, f1)
                elif row1["datatype"] == "categorical":
                    sum += row2["fact_confidence"] * categorical_implication(f2, f1)
            # Calculate the adjusted confidence score (Eq. 6)
            adjusted[i] = self.influence_related * sum + row1["fact_confidence"]
        # Iterate through the facts
        for i, row1 in df.iterrows():
            # Update the values of confidence scores
            df.at[i, "fact_confidence"] = adjusted[i]
        # Return the data
        return df

    def compute_fact_confidence(self, df):
        """
        This function calculates the fact confidence scores.

                Parameters:
                        df (dataframe): Dataframe containing the sources,
                            facts, objects, trustworthiness and fact confidence

                Returns:
                        df (datafram): Dataframe with new fact confidence scores
        """
        # Calculate the confidence of f (Eq. 8)
        s = lambda x: sigmoid(self.dampening_factor * x)
        # Iterate through facts
        for i, row in df.iterrows():
            # Calculate and update confidence of the fact
            df.at[i, "fact_confidence"] = s(row["fact_confidence"])
        # Return the data
        return df

    def update_fact_confidence(self,df):
        """
        This function iterates through the dataframe, calling all the functions
        required to calculate the confidence scores for each fact related to an
        object.

                Parameters:
                        df (dataframe): Dataframe containing the sources,
                            facts, objects, trustworthiness and fact confidence

                Returns:
                        df (datafram): Dataframe with confidence scores
        """
        # Iterate through every object
        for object_ in df["object"].unique():
            # Get indices for the object
            indices = df["object"] == object_
            # Get entries in df related to the object
            d = df.loc[indices]
            # Calculate the confidence scores
            d = self.confidence_score(d)
            # Calculate the adjusted confidence scores
            d = self.adjusted_confidence_score(d)
            # Calculate the fact confidences
            df.loc[indices] = self.compute_fact_confidence(d)
        #print("Fact Confidence: " + str(df["fact_confidence"].values))
        # Return the data
        return df

    def update_source_trustworthiness(self,df):
        """
        This function iterates through the dataframe, calling all the functions
        required to calculate the source trustworthiness scores.

                Parameters:
                        df (dataframe): Dataframe containing the sources,
                            facts, objects, trustworthiness and fact confidence

                Returns:
                        df (datafram): Dataframe with source trustworthiness
        """
        # Iterate through the sources
        for source in df["source"].unique():
            # Get the indices for the source
            indices = df["source"] == source
            # Get the confidence scores of facts provided by the source
            cs = df.loc[indices, "fact_confidence"]
            # Sum the confidence scores and divide by the number of facts provided (Eq. 1)
            df.loc[indices, "trustworthiness"] = sum(cs) / len(cs)
        #print("Source Trustworthiness: " + str(df["trustworthiness"].values))
        # Return the data
        return df

    def iteration(self,df):
        """
        This function performs an iteration of the algorithm.

                Parameters:
                        df (dataframe): Dataframe containing the sources,
                            facts, objects, trustworthiness and fact confidence

                Returns:
                        df (dataframe): Dataframe with updated fact confidence and
                            source trustworthiness
        """
        # Update the fact confidence
        df = self.update_fact_confidence(df)
        # Update the source trustworthiness
        df = self.update_source_trustworthiness(df)
        # Return the data
        return df

    def calculate_change(self,t1,t2):
        """
        This function returns the change in trustworthiness between two vectors.

                Parameters:
                        t1 (array): Trustworthiness scores before the new iteration
                        t2 (array): Trustworthiness scores after the new iteration

                Returns:
                        float: Relative change between two vectors
        """
        # Calculate the cosine similarity
        cosine = np.dot(t2,t1)/(norm(t2)*norm(t1))
        # Change in trustworthiness is measured as 1 - cosine similarity
        change = 1 - cosine
        # Return True if under threshold and False if over threshold
        return change

    def run(self,dataframe,max_iterations=200,threshold=1e-6,initial_trustworthiness=0.9):
        """
        This function executes the TruthFinder algorithm.

                Parameters:
                        dataframe (dataframe): Dataframe containing sources, facts, and objects
                        max_iterations (int): Maximum number of allowed iterations
                        threshold (float): Threshold value for stopping condition
                        initial_trustworthiness (float): Initial trustworthiness score for all sources

                Returns:
                        dataframe: Dataframe containing original data, as well as fact confidence
                        and source trustworthiness
        """
        # Initialize dataframe to capture evolution of source trustworthiness
        source_evolution = pd.DataFrame(dataframe["source"].tolist(),columns=["source"])
        # Initialize dataframe to capture evolution of fact confidence
        fact_evolution = pd.DataFrame(dataframe["fact"].tolist(),columns=["fact"])
        # Initialize trustworthiness change array
        change_evolution = []
        # Add initial trustworthiness
        source_evolution["0"] = np.ones(len(source_evolution.index)) * initial_trustworthiness
        # Add initial confidence
        fact_evolution["0"] = np.zeros(len(fact_evolution.index))
        # Initialize trustworthiness
        dataframe["trustworthiness"] = [Decimal(initial_trustworthiness)] * len(dataframe.index)
        # Initialize fact_confidence
        dataframe["fact_confidence"] = [Decimal(0)] * len(dataframe.index)
        # Loop until max_iterations
        for i in range(max_iterations):
            # Remove duplicates for sources and get trustworthiness for each
            t1 = dataframe.drop_duplicates("source")["trustworthiness"]
            # Perform an iteration
            try:
                dataframe = self.iteration(dataframe)
            except ValueError as e:
                # If a ValueError occurs, print the error and exit
                print(f"Error during iteration {i}: {e}")
                print(dataframe)
            # Remove duplicates for sources and get trustworthiness for each
            t2 = dataframe.drop_duplicates("source")["trustworthiness"]
            # Calculate cosine similarity
            change = self.calculate_change(t1, t2)
            # Append to evolution array
            change_evolution.append(change)
            # Check if difference is below threshold
            if change < threshold:
                # Exit loop and return data
                return dataframe, source_evolution, fact_evolution, change_evolution
        # Return data
        return dataframe, source_evolution, fact_evolution, change_evolution

def build_dataframe(claims, obj, datatype):
    """
    Build a dataframe from the claims.
    """
    # Create a list to hold the data
    data = []
    # Iterate through claims
    for claim in claims:
        # Append the data to the list
        data.append({
            "source": claim['sourceId'],
            "fact": float(claim['fact']) if datatype == "continuous" else claim['fact'],
            "object": obj,
            "datatype": datatype
        })
    # Create a dataframe from the data
    return pd.DataFrame(data)

def assess(dataset, output):
    """
    Consume the input dataset file and use TruthFinder.
    """
    # Read input file
    with open(dataset, "r", encoding="utf-8") as file:
        # Load JSON data
        data = json.load(file)
        # Iterate through objects
        for obj in data['objects']:
            # Extract claimssourceId
            claims = obj['claims']
            # Shuffle claims to ensure randomness
            random.shuffle(claims)
            # Build a dataframe from claims
            dataframe = build_dataframe(claims,obj['name'],obj['datatype'])
            # Initialize TruthFinder
            tf = TruthFinder(dampening_factor=0.2, influence_related=0.5)
            # Run TruthFinder algorithm
            df, _, _, _ = tf.run(dataframe, max_iterations=4, threshold=1e-6, initial_trustworthiness=0.5)
            # Extract the truth
            result = df['fact'][0]
            # Create a result object
            data = {
                "result": str(result),
                "truth": str(obj['truth']),
                "datatype": obj['datatype']
            }
            # Calculate distances
            data['metrics'] = calculate_metrics(data)
            # Append result to output
            output['results'].append(data)

if __name__ == "__main__":
    # Initialize json object
    output = {
        "algorithm": "TruthFinder",
        "results": [],
    }
    # Check if command line arguments are provided
    if len(sys.argv) > 1:
        # Extract command line arguments
        datatype    = sys.argv[1]
        input_file  = sys.argv[2]
        output_file = sys.argv[3]
        # Perform assessment
        assess(input_file, output)
        # Write output to file
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4)
    else:
        # Print usage message
        print("Usage: python majority.py <datatype> <input_file> <output_file>")
        print("Example: python majority.py testbed truth/gold.txt output.json")
        sys.exit(1)