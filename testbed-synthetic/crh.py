"""
This module contains the code responsible for the implementation
of the CRH algorithm proposed by Li et al. used for data
consolidation purposes.
"""
import sys
import json
import random
import warnings
import numpy as np
import statistics
import pandas as pd
from numpy.linalg import norm

from metrics import calculate_metrics

warnings.filterwarnings("error")
np.seterr(divide = 'ignore', invalid='ignore')

class CRH(object):
    """
    The CRH algorithm represents all the necessary logic to compute respective weights
    and truths for the supplied data.

    Methods
    -------
    strcmp(s1,s2):
        Copies the strcmp behaviour from matlab.
    calculate_change(t1,t2):
        Calculates the cosine similarity between two arrays.
    categorical_loss_function(truth,value):
        Calculates loss for categorical values.
    continuous_loss_function(self,truth,value,values):
        Calculates loss for continuous values.
    voting_averaging(df,W):
        Performs voting and averaging.
    calculate_initial_truths(df,W):
        Calculates the initial truths.
    update_weight(df,X,W):
        Updates the weights in an iteration.
    update_truth(self,df,X,W):
        Updates the truths in an iteration.
    iterate(df,X,W):
        Performs an iteration of the algorithm.
    run(dataframe,max_iterations=5,threshold=1e-6):
        Executes the algorithm.
    """
    def strcmp(self,s1,s2):
        """
        This function emulates the strcmp function present in Matlab. Given an
        array s1, it returns an array with the same size, where each positions
        has a 1 if the value in the corresponding position of s1 equals s2, and
        0 otherwise.

                Parameters:
                        s1 (list): Array of values
                        s2 (str): String to be compared

                Returns:
                        v (list): List of 0 and 1
        """
        # Initialize v
        v = []
        # Iterate array s1
        for i, observation in enumerate(s1):
            # If the observation is equal to s2
            if observation == s2:
                # Add 1 to v
                v.append(1)
            else:
                # Otherwise, add 0
                v.append(0)
        # Return v
        return v

    def calculate_change(self,t1,t2):
        """
        This function returns the change in trustworthiness between two vectors.

                Parameters:
                        t1 (list): Snapshot of weights
                        t2 (list): Current weights

                Returns:
                        float: Relative change between two vectors
        """
        # Calculate the cosine similarity
        cosine = np.dot(t2,t1)/(norm(t2)*norm(t1))
        # Change in trustworthiness is measured as 1 - cosine similarity
        change = 1 - cosine
        # Return True if under threshold and False if over threshold
        return change

    def categorical_loss_function(self,truth,value):
        """
        The categorical loss function consists of a 0-1 loss function
        which returns 0 if the given value is equal to the truth, and
        0 otherwise.

                Parameters:
                        truth (str): String corresponding to the truth
                        value (str): String corresponding to a value

                Returns:
                        result (int): Either 0 or 1
        """
        # Check if values are equal
        if value == truth:
            # Return 0
            return 0
        else:
            # Otherwise, return 1
            return 1
        
    def string_loss_function(self,truth,value):
        """
        The string loss function consists of a 0-1 loss function
        which returns 0 if the given value is equal to the truth, and
        0 otherwise.

                Parameters:
                        truth (str): String corresponding to the truth
                        value (str): String corresponding to a value

                Returns:
                        result (int): Either 0 or 1
        """
        # Create a table to store the results of subproblems
        dp = [[0 for j in range(len(value)+1)] for i in range(len(truth)+1)]

        # Initialize the table
        for i in range(len(truth)+1):
            dp[i][0] = i
        for j in range(len(value)+1):
            dp[0][j] = j

        # Populate the table using dynamic programming
        for i in range(1, len(truth)+1):
            for j in range(1, len(value)+1):
                if truth[i-1] == value[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

        # Return the edit distance
        return dp[len(truth)][len(value)]

    def continuous_loss_function(self,truth,value,values):
        """
        The continuous loss function consists of a normalized squared
        loss function returning a float value.

                Parameters:
                        truth (floar): Value corresponding to the truth
                        value (float): Value to be analyzed
                        values  (lst): List of all values

                Returns:
                        normalized_squared_loss (floar): Normalized squared loss
        """
        # If the values are all the same, return 0
        normalized_squared_loss = 0
        # Check if the values are not all the same
        if np.std(values) > 0:
            # Calculate the normalized squared loss
            normalized_squared_loss = (float(truth)-float(value))**2/(np.std(values))
        # Return the normalized squared loss
        return normalized_squared_loss

    def voting_averaging(self,df,W):
        """
        This function performs voting and averaging of the facts related to
        an object, returning the calculated truth.

                Parameters:
                        df (dataframe): Dataframe containing the entries
                        W (dataframe): Dataframe containing the weights

                Returns:
                        v (list): List of 0 and 1
        """
        # Get the observations as a list
        observations = df["fact"].tolist()
        # If the datatype of the object is continuous, perform averaging
        if df.iloc[0]["datatype"] == "continuous":
            # Map the list of observations to a list of floats
            observations = list(map(float, observations))
            # Calculate the mean of the observations
            m = statistics.mean(observations)
            # Return m as the truth
            return m
        # If the datatype of the object is categorical, perform weighed voting
        else:
            # Initialize the array of weights (w)
            w = []
            # Iterate the entries about the object
            for i, row in df.iterrows():
                # Retrieve the weight of the source of the entry and append to w
                w.append((W.loc[W["source"] == row["source"]])["weight"].values[0])
            # Initialize the array of weighed occurences
            weighted_occurences = []
            # Get the sorted list of unique observations (the array must be sorted
            # to preserve consistency)
            unique_observations = sorted(list(set(observations)))
            # Iterate through each unique observation
            for o, observation in enumerate(unique_observations):
                # Calculate the weighed occurence
                wo = sum(np.multiply(self.strcmp(observations,unique_observations[o]),w))
                # Append the weighed occurence
                weighted_occurences.append(wo)
            # Get the index of the max value
            index = np.argmax(weighted_occurences)
            # Return the observation with the highest weight
            return unique_observations[index]

    def calculate_initial_truths(self,df,W):
        """
        This function calculates the initial truths for each object in the
        given dataframe using the supplied weights.

                Parameters:
                        df (dataframe): Dataframe containing the entries
                        W (dataframe): Dataframe containing the weights

                Returns:
                        initial_truths (dataframe): Dataframe containing the truths
        """
        # Initialize the dataframe with one entry per unique object
        initial_truths = pd.DataFrame(
                list(zip(df["object"].unique(),[None] * len(df["object"].unique()))),
                columns=["object", "truth"]
            )
        # Iterate through every unique object in df
        for object_ in df["object"].unique():
            # Get indices in df for the object
            indices = df["object"] == object_
            # Get entries in df related to the object
            d = df.loc[indices]
            # Conduct voting/averaging
            truth = self.voting_averaging(d,W)
            # Set the truth for the object
            initial_truths.loc[initial_truths["object"] == object_, "truth"] = truth
        # Return the dataframe containing the initial truths
        return initial_truths

    def update_weight(self,df,X,W):
        """
        This function updates the weights (step 1).

                Parameters:
                        df (dataframe): Dataframe containing the entries
                        X (dataframe): Dataframe containing the truths
                        W (dataframe): Dataframe containing the weights

                Returns:
                        W (dataframe): Dataframe containing the updated weights
        """
        # Initialize the distance array for categorical values
        cat_distances = np.zeros(len(W.index),dtype=float)
        # Initialize the distance array for continuous values
        con_distances = np.zeros(len(W.index),dtype=float)
        # Initialize the distance array for string values
        str_distances = np.zeros(len(W.index),dtype=float)
        # Initialize the count array for categorical values
        cat_count = np.zeros(len(W.index),dtype=float)
        # Initialize the count array for continuous values
        con_count = np.zeros(len(W.index),dtype=float)
        # Initialize the count array for string values
        str_count = np.zeros(len(W.index),dtype=float)
        # Iterate through the facts
        for i, row in df.iterrows():
            # Get the index of the source of the fact
            source_index = (W.loc[W["source"] == row["source"]]).index[0]
            # Get the truth for the object of the entry
            truth = (X.loc[X["object"] == row["object"]])["truth"].values[0]
            # Check the datatype of the entry
            if row["datatype"] == "categorical":
                # Increment the categorical distances using the specific loss function
                cat_distances[source_index] = cat_distances[source_index] +\
                        self.categorical_loss_function(truth,row["fact"])
                # Increment the count for the specific source by 1
                cat_count[source_index] += 1
            elif row["datatype"] == "continuous":
                # Get the entries related to the object
                entries = (df.loc[df["object"] == row["object"]])
                # Get the continuous entries
                c_entries = (entries.loc[df["datatype"] == "continuous"])
                # Map the list of values to floats
                values = list(map(float, c_entries["fact"].values))
                # Increment the continuous distances using the specific loss function
                con_distances[source_index] = con_distances[source_index] +\
                        self.continuous_loss_function(truth,row["fact"],values)
                # Increment the count for the specific source by 1
                con_count[source_index] += 1
            elif row["datatype"] == "string":
                # Increment the categorical distances using the specific loss function
                str_distances[source_index] = str_distances[source_index] +\
                        self.string_loss_function(truth,row["fact"])
                # Increment the count for the specific source by 1
                str_count[source_index] += 1
        # Divide the distances by the respective counts element-wise
        cat_distances = np.divide(cat_distances,cat_count,\
                                  out=np.zeros_like(cat_distances), where=cat_count!=0)
        # Check if sum of distances is greater than 0
        if(sum(cat_distances) >0):
            # Divide the distances by the sum of the distances
            cat_distances = cat_distances/sum(cat_distances)
        # Divide the distances by the respective counts element-wise
        con_distances = np.divide(con_distances,con_count,\
                                  out=np.zeros_like(con_distances), where=con_count!=0)
        # Check if sum of distances is greater than 0
        if(sum(con_distances) >0):
            # Divide the distances by the sum of the distances
            con_distances = con_distances/sum(con_distances)
        # Divide the distances by the respective counts element-wise
        str_distances = np.divide(str_distances,str_count,\
                                  out=np.zeros_like(str_distances), where=str_count!=0)
        # Check if sum of distances is greater than 0
        if(sum(str_distances) >0):
            # Divide the distances by the sum of the distances
            str_distances = str_distances/sum(str_distances)
        # Join the categorical and continuous vectors
        distances = cat_distances + con_distances + str_distances
        # Normalize the distances
        if max(distances) > 0:
            distances = distances/max(distances)
        # Avoid infinite values in log function by adding a small value
        distances = distances + 0.1
        # Calculate the weights for all sources (Eq. 5)
        weights = abs(-np.log(distances))
        # Iterate the calculated weights
        for i, weight in enumerate(weights):
            # Update the weight in W
            W.at[i, "weight"] = float(weight)
        # Return the updated dataframe
        return W

    def update_truth(self,df,X,W):
        """
        This function updates the truths (step 2).

                Parameters:
                        df (dataframe): Dataframe containing the entries
                        X (dataframe): Dataframe containing the truths
                        W (dataframe): Dataframe containing the weights

                Returns:
                        X (dataframe): Dataframe containing the updated truths
        """
        # Iterate each entry in truths dataframe
        for o, entry in X.iterrows():
            # Get indices for the entries related to the object
            indices = df["object"] == entry["object"]
            # Get entries in df related to the object
            object_entries = df.loc[indices]
            # Get the list of observations
            observations = object_entries["fact"].values
            # Get the list of unique observations
            unique_observations = list(set(observations))
            # Get the datatype for the object
            datatype = object_entries.iloc[0]["datatype"]
            # Initialize the weights array
            w = []
            # Iterate entries related to the object
            for i, row in object_entries.iterrows():
                # Collect the weight of the source of the entry
                w.append((W.loc[W["source"] == row["source"]])["weight"].values[0])
            # If the object datatype is categorical (Eq. 13)
            if datatype == "categorical":
                # Initialize the weighed occurences array
                weighted_occurences = []
                # Iterate each unique observation
                for u, unique in enumerate(unique_observations):
                    # Multiply the result of strcmp by the respective weights element-wise
                    r = np.multiply(self.strcmp(observations,unique_observations[u]),w)
                    # Replace nan values with 0
                    r[np.isnan(r)] = 0
                    # Append the sum of r to the weighted_occurences list
                    weighted_occurences.append(sum(r))
                # Get the unique observation using the index of the max value of weighted_occurences
                truth = unique_observations[np.argmax(weighted_occurences)]
            # If the object datatype is continuous (Eq. 20)
            elif datatype == "continuous":
                # Map the list of observations to float
                observations = list(map(float, observations))
                # Calculate the optimal value (Eq. 20)
                truth = sum(np.multiply(w,observations))/sum(w)
            # If the object datatype is string (edit distance)
            elif datatype == "string":
                # Initialize the weighed occurences array
                weighted_occurences = []
                # Iterate each unique observation
                for u, unique in enumerate(unique_observations):
                    # Initialize list
                    l = []
                    for o, observation in enumerate(observations):
                        l.append(self.string_loss_function(observation,unique_observations[u]))
                    # Multiply the result of strcmp by the respective weights element-wise
                    r = np.subtract(l,w)
                    # Replace nan values with 0
                    r[np.isnan(r)] = 0
                    # Append the sum of r to the weighted_occurences list
                    weighted_occurences.append(sum(r))
                # Get the unique observation using the index of the max value of weighted_occurences
                truth = unique_observations[np.argmin(weighted_occurences)]
            # Update the truth dataframe with the new value
            X.loc[X["object"] == entry["object"], "truth"] = truth
        # Return the updated dataframe
        return X

    def iterate(self,df,X,W):
        """
        This function executes an iteration of the algorithm.

                Parameters:
                        df (dataframe): Dataframe containing the entries
                        X (dataframe): Dataframe containing the truths
                        W (dataframe): Dataframe containing the weights

                Returns:
                        X (dataframe): Dataframe containing the truths
                        W (dataframe): Dataframe containing the truweightsths
        """
        # Step 1: update the weights
        W = self.update_weight(df,X,W)
        # Step: 2: update the truths
        X = self.update_truth(df,X,W)
        # Return the truths(X) and weights(W)
        return X, W

    def run(self,dataframe,max_iterations=3,threshold=1e-6):
        """
        This functions executes the CRH algorithm.

                Parameters:
                        dataframe (dataframe): Dataframe containing the entries
                        max_iterations (int): Maximum number of iterations

                Returns:
                        X (dataframe): Dataframe containing the truths
                        W (dataframe): Dataframe containing the truweightsths
        """
        # Pandas and numpy options
        #pd.set_option('display.float_format', lambda x: '%.5f' % x)
        np.set_printoptions(suppress=True)
        # Prepare data
        N = dataframe['object'].nunique() # Number of objects
        K = dataframe['source'].nunique() # Number of sources
        # Initialize the weights dataframe (W)
        W = pd.DataFrame(
            list(zip(dataframe["source"].unique(),np.ones(K, dtype=int) * (1/K))),
            columns=["source", "weight"]
        )
        # Calculate the initial truths
        X = self.calculate_initial_truths(dataframe,W)
        # Loop until max_iterations or below threshold
        for i in range(0,max_iterations):
            # Get a snapshot of W
            w_snap = W["weight"].tolist()
            # Perform an iteration
            X, W = self.iterate(dataframe,X,W)
            # Calculate cosine similarity
            change = self.calculate_change(w_snap, W["weight"].tolist())
            # Check if difference is below threshold
            if change < threshold:
                # Return the truths and weights
                return X,W
        # Return the truths and weights
        return X,W

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
    Consume the input dataset file and use CRH.
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
            crh = CRH()
            # Run the CRH algorithm
            df, _ = crh.run(dataframe)
            # Extract the truth
            result = df['truth'][0]
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
        "algorithm": "CRH",
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
        print("Usage: python crh.py <datatype> <input_file> <output_file>")
        print("Example: python crh.py testbed truth/gold.txt output.json")
        sys.exit(1)