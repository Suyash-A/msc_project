import pandas as pd
import os
import argparse
from sklearn.metrics import f1_score

def process_and_compute_f1_scores(true_labels_path, pred_labels_dir, ordered_test_ids_path):
    # Load the true labels dataframe
    true_df = pd.read_csv(true_labels_path)
    ordered_test_ids_df = pd.read_csv(ordered_test_ids_path)

    # Define the list of classes/labels
    labels = [
        'No Finding', 'Enlarged Cardiomediastinum', 'Cardiomegaly', 'Lung Lesion', 
        'Airspace Opacity', 'Edema', 'Consolidation', 'Pneumonia', 'Atelectasis', 
        'Pneumothorax', 'Pleural Effusion', 'Pleural Other', 'Fracture', 'Support Devices'
    ]

    # Initialize lists to store F1 scores for averaging later
    micro_f1_scores = []
    macro_f1_scores = []
    weighted_f1_scores = []

    # Process each prediction file in the directory
    for file_name in os.listdir(pred_labels_dir):
        if file_name.startswith("visualchexbert_labeled_") and file_name.endswith(".csv"):
            visual_chexbert_df = pd.read_csv(os.path.join(pred_labels_dir, file_name))

            # Drop the 'Reports' column
            visual_chexbert_df = visual_chexbert_df.drop(columns=['Report Impression'])

            # Rename the 'Lung Opacity' column to 'Airspace Opacity'
            visual_chexbert_df = visual_chexbert_df.rename(columns={'Lung Opacity': 'Airspace Opacity'})

            # Concatenate the ordered_test_ids with the chexbert dataframe (excluding the 'Reports' column)
            result_df = pd.concat([ordered_test_ids_df, visual_chexbert_df], axis=1)

            # Filter true_df to only include rows with study_id present in result_df
            filtered_true_df = true_df[true_df['study_id'].isin(result_df['study_id'])]

            # Ensure both dataframes have the same study_id order
            result_df = result_df.sort_values('study_id').reset_index(drop=True)
            filtered_true_df = filtered_true_df.sort_values('study_id').reset_index(drop=True)

            # Align the columns of result_df to match the order of labels
            result_df = result_df[['study_id'] + labels]

            # Calculate micro, macro, and weighted F1 scores
            y_true_all = filtered_true_df[labels].fillna(0).astype(int).values.flatten()
            y_pred_all = result_df[labels].fillna(0).astype(int).values.flatten()

            micro_f1 = f1_score(y_true_all, y_pred_all, average='micro', zero_division=0)
            macro_f1 = f1_score(y_true_all, y_pred_all, average='macro', zero_division=0)
            weighted_f1 = f1_score(y_true_all, y_pred_all, average='weighted', zero_division=0)

            # Append the scores to the lists
            micro_f1_scores.append(micro_f1)
            macro_f1_scores.append(macro_f1)
            weighted_f1_scores.append(weighted_f1)

            # Optionally print the F1 scores for each file
            print(f"F1 Scores for {file_name}:")
            print(f"Micro F1 Score: {micro_f1}")
            print(f"Macro F1 Score: {macro_f1}")
            print(f"Weighted F1 Score: {weighted_f1}")
            print()

    # Compute and print the average F1 scores
    avg_micro_f1 = sum(micro_f1_scores) / len(micro_f1_scores)
    avg_macro_f1 = sum(macro_f1_scores) / len(macro_f1_scores)
    avg_weighted_f1 = sum(weighted_f1_scores) / len(weighted_f1_scores)

    print("Average F1 Scores across all files:")
    print(f"Average Micro F1 Score: {avg_micro_f1}")
    print(f"Average Macro F1 Score: {avg_macro_f1}")
    print(f"Average Weighted F1 Score: {avg_weighted_f1}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process VisualCheXbert predictions and compute F1 scores.")
    parser.add_argument('--true_labels', type=str, required=True, help="Path to the true labels CSV file")
    parser.add_argument('--pred_labels_dir', type=str, required=True, help="Directory containing prediction CSV files")
    parser.add_argument('--ordered_test_ids', type=str, required=True, help="Path to the ordered test IDs CSV file")
    
    args = parser.parse_args()

    process_and_compute_f1_scores(args.true_labels, args.pred_labels_dir, args.ordered_test_ids)
