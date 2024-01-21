# topsis_aman_102103043/102103043.py

import sys
import pandas as pd
import numpy as np

def read_csv(input_file):
    try:
        df = pd.read_csv(input_file)
        return df
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: File '{input_file}' is empty.")
        sys.exit(1)
    except pd.errors.ParserError:
        print(f"Error: Unable to parse CSV file '{input_file}'. Ensure it is a valid CSV file.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV '{input_file}': {str(e)}")
        sys.exit(1)

def validate_inputs(weights, impacts, num_columns):
    if not (len(weights) == len(impacts) == num_columns - 1):
        print("Error: Number of weights, impacts, and columns must be the same.")
        sys.exit(1)

    if not all(w.replace('.', '').isdigit() or (w[1:].replace('.', '').isdigit() and w[0] == '-') for w in weights):
        print("Error: Weights must be numeric values separated by commas.")
        sys.exit(1)

    if not all(i in ['+', '-'] for i in impacts):
        print("Error: Impacts must be either '+' or '-'.")
        sys.exit(1)

def normalize_matrix(matrix):
    norm_matrix = np.copy(matrix)
    for i in range(matrix.shape[1]):
        norm_matrix[:, i] /= np.linalg.norm(matrix[:, i])
    return norm_matrix

def calculate_weighted_normalized_matrix(norm_matrix, weights):
    weighted_norm_matrix = np.copy(norm_matrix)
    for i in range(norm_matrix.shape[1]):
        weighted_norm_matrix[:, i] *= float(weights[i])
    return weighted_norm_matrix

def calculate_ideal_and_anti_ideal(weighted_norm_matrix, is_maximize):
    ideal_solution = np.max(weighted_norm_matrix, axis=0) if is_maximize else np.min(weighted_norm_matrix, axis=0)
    anti_ideal_solution = np.min(weighted_norm_matrix, axis=0) if is_maximize else np.max(weighted_norm_matrix, axis=0)
    return ideal_solution, anti_ideal_solution

def calculate_euclidean_distances(weighted_norm_matrix, ideal_solution, anti_ideal_solution):
    dist_ideal = np.linalg.norm(weighted_norm_matrix - ideal_solution, axis=1)
    dist_anti_ideal = np.linalg.norm(weighted_norm_matrix - anti_ideal_solution, axis=1)
    return dist_ideal, dist_anti_ideal

def calculate_topsis_score(dist_ideal, dist_anti_ideal):
    topsis_score = dist_anti_ideal / (dist_ideal + dist_anti_ideal)
    return topsis_score

def topsis(matrix, weights, impacts):
    norm_matrix = normalize_matrix(matrix)
    weighted_norm_matrix = calculate_weighted_normalized_matrix(norm_matrix, weights)
    is_maximize = [i == '+' for i in impacts]
    ideal_solution, anti_ideal_solution = calculate_ideal_and_anti_ideal(weighted_norm_matrix, is_maximize)
    dist_ideal, dist_anti_ideal = calculate_euclidean_distances(weighted_norm_matrix, ideal_solution, anti_ideal_solution)
    topsis_score = calculate_topsis_score(dist_ideal, dist_anti_ideal)
    
    return topsis_score

def main():
    if len(sys.argv) != 5:
        print("Usage: python 102103043.py input_file.csv weights impacts output_file.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    weights = sys.argv[2].split(',')
    impacts = sys.argv[3].split(',')
    output_file = sys.argv[4]

    input_df = read_csv(input_file)

    try:
        num_columns = len(input_df.columns)
        validate_inputs(weights, impacts, num_columns)
        decision_matrix = input_df.iloc[:, 1:].values.astype(float)
        topsis_scores = topsis(decision_matrix, weights, impacts)

        input_df['Topsis Score'] = topsis_scores
        input_df['Rank'] = np.argsort(topsis_scores)[::-1] + 1

        
        print("Results:")
        print(input_df)

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
