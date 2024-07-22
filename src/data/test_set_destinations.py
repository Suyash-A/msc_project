import pandas as pd
import argparse

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Filter study list based on labeled test set")
    parser.add_argument('--labeled_file', required=True, help="Path to the labeled test set CSV file")
    parser.add_argument('--study_list_file', required=True, help="Path to the study list CSV file")
    parser.add_argument('--output_file', required=True, help="Path to the output CSV file")

    # Parse the arguments
    args = parser.parse_args()

    # Load the labeled test set and the study list
    labeled_df = pd.read_csv(args.labeled_file)
    list_df = pd.read_csv(args.study_list_file)

    # Filter the study list to include only rows with study_id present in the labeled test set
    filtered_list_df = list_df[list_df['study_id'].isin(labeled_df['study_id'])]

    # Save the filtered dataframe to a CSV file
    filtered_list_df.to_csv(args.output_file, index=False)

    print(f"Filtered test-set report locations have been saved to {args.output_file}.")

if __name__ == "__main__":
    main()

