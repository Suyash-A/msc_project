import pandas as pd
import os
import re
import copy
import numpy as np
import argparse
from sklearn import metrics

def evaluate_label(tar, pred, ignore_nan=False):
    """
    Return precision, recall, f1, and prevalence for a single label.
    """
    
    if ignore_nan:
        idx = ~(np.isnan(tar) | np.isnan(pred))
        pred = pred[idx]
        tar = tar[idx]
    
    results = {
        'precision': np.nan,
        'recall': np.nan,
        'f1': np.nan,
        'positives': int(tar.sum())
    }
    
    if results['positives'] == 0:
        # return NaN if no positive labels
        return results
    
    results['precision'] = metrics.precision_score(tar, pred, zero_division=0)
    results['recall'] = metrics.recall_score(tar, pred)
    if results['precision'] + results['recall'] == 0:
        results['f1'] = 0.0
    else:
        results['f1'] = 2 * (results['precision'] * results['recall']) / (results['precision'] + results['recall'])

    
    return results
    

def get_scores(target, prediction, categories, ignore_nan=False):
    
    
    results = {}
    for i, c in enumerate(categories):
        results[c] = evaluate_label(target[:, i], prediction[:, i])
    
    # convert to dataframe
    df = pd.DataFrame.from_dict(results, orient='index')
    
    return df

def evaluate_labels(df_truth, df_label, method='mention'):
    categories = list(df_truth.columns)
    
    # create the matrix of 0s and 1s
    preds = copy.copy(df_label.values)
    targets = copy.copy(df_truth.values)
    
    if method == 'mention':
        # any mention is a 1
        preds[np.isin(preds, [-1, 0, 1])] = 1
        targets[np.isin(targets, [-1, 0, 1])] = 1

        # no mention is a 0
        preds[np.isnan(preds)] = 0
        targets[np.isnan(targets)] = 0
        
        # do not ignore NaN (which we have set to 0 anyway)
        ignore_nan=False
    elif method == 'absence':
        # successful prediction of absence
        idxNonZero = preds != 0
        idxZero = preds == 0
        preds[idxNonZero] = 0
        preds[idxZero] = 1
        
        idxNonZero = targets != 0
        idxZero = targets == 0
        targets[idxNonZero] = 0
        targets[idxZero] = 1
        
        # ignore NaN values
        ignore_nan=True
    elif method == 'presence':
        # successful prediction of presence
        idxZero = preds != 1
        idxNonZero = preds == 1
        preds[idxZero] = 0
        preds[idxNonZero] = 1

        idxZero = targets != 1
        idxNonZero = targets == 1
        targets[idxZero] = 0
        targets[idxNonZero] = 1

        # ignore NaN values
        ignore_nan=True
    elif method == 'uncertain':
        # any non-uncertain prediction is 0
        preds[preds!= -1] = 0
        targets[targets != -1] = 0
        
        # any uncertain prediction is 1
        preds[preds == -1] = 1
        targets[targets == -1] = 1
        
        # ignore NaN
        ignore_nan=True
    else:
        raise ValueError(f'Unrecognized method {method}')
        
    df = get_scores(targets, preds, categories, ignore_nan=ignore_nan)
    
    return df, preds, targets

def compute_chexbert_f1_scores(true_labels_path, pred_labels_dir, test_report_path):
    
    # Define the list of classes/labels
    categories = [
        'No Finding', 'Enlarged Cardiomediastinum', 'Cardiomegaly', 'Lung Lesion', 
        'Lung Opacity', 'Edema', 'Consolidation', 'Pneumonia', 'Atelectasis', 
        'Pneumothorax', 'Pleural Effusion', 'Pleural Other', 'Fracture', 'Support Devices'
    ]

    # Test set reports
    test_reports_df = pd.read_csv(test_report_path, header=None)
    test_reports_df.columns = ['id', 'text']
    
    # Initialize lists to store F1 scores for averaging later
    micro_f1_scores = []
    macro_f1_scores = []
    weighted_f1_scores = []

    # Process each prediction file in the directory
    for file_name in os.listdir(pred_labels_dir):
        if file_name.startswith("chexbert_labeled_") and file_name.endswith(".csv"):
            print("#" * 80)
            print(f"Processing {file_name}...")
            print("#" * 80)
            chexbert_df = pd.read_csv(os.path.join(pred_labels_dir, file_name))

            chexbert_df = chexbert_df.merge(
                test_reports_df, how='inner', left_on='Report Impression', right_on='text'
            )

            chexbert_df.drop_duplicates(inplace=True)

            chexbert_df['id'] = chexbert_df['id'].astype(str).str.lstrip('s')
            chexbert_df.set_index('id', inplace=True)
            chexbert_df.rename(columns={'Airspace Opacity': 'Lung Opacity'}, inplace=True)
            chexbert_df = chexbert_df[categories]

            # Load the true labels dataframe
            true_df = pd.read_csv(true_labels_path, header=0, index_col=0)
            true_df.index.name = 'id'
            true_df.rename(columns={'Airspace Opacity': 'Lung Opacity'}, inplace=True)
            true_df = true_df[categories]

            # Align the columns of the true_df to match the order of labels
            true_df.sort_index(inplace=True)
            true_df.index = true_df.index.astype(str)
            common_ids = true_df.index.intersection(chexbert_df.index)
            true_df = true_df.loc[common_ids]
            chexbert_df = chexbert_df.loc[common_ids]

            print('CheXbert: Mention')
            df, preds, targets = evaluate_labels(true_df, chexbert_df, method='mention')

            for c in df.columns:
                if 'float' in str(df.dtypes[c]):
                    df[c] = np.round(df[c], 3)
            print(df)
            print()
            total_mentions = np.sum(targets)

            print('CheXbert: Uncertain')
            df, preds, targets = evaluate_labels(true_df, chexbert_df, method='uncertain')
            df.columns = pd.MultiIndex.from_tuples([('CheXbert', c) for c in df.columns])
            df.columns = df.columns.reorder_levels([1, 0])
            df = df[['precision', 'recall', 'f1', 'positives']]

            for c in df.columns:
                if 'float' in str(df.dtypes[c]):
                    df[c] = np.round(df[c], 3)

            df.index.name = 'Uncertain'
            print(df)
            print()

            # Calculate micro, macro, and weighted F1 scores
            micro_f1 = metrics.f1_score(targets, preds, average='micro', zero_division=0) * (np.sum(targets) / total_mentions)
            macro_f1 = metrics.f1_score(targets, preds, average='macro', zero_division=0) * (np.sum(targets) / total_mentions)
            weighted_f1 = metrics.f1_score(targets, preds, average='weighted', zero_division=0) * (np.sum(targets) / total_mentions)

            print('CheXbert: Absence')
            df, preds, targets = evaluate_labels(true_df, chexbert_df, method='absence')
            df.columns = pd.MultiIndex.from_tuples([('CheXbert', c) for c in df.columns])
            df.columns = df.columns.reorder_levels([1, 0])
            df = df[['precision', 'recall', 'f1', 'positives']]
            for c in df.columns:
                if 'float' in str(df.dtypes[c]):
                    df[c] = np.round(df[c], 3)

            df.index.name = 'Absence'
            print(df)
            print()

            micro_f1 += metrics.f1_score(targets, preds, average='micro', zero_division=0) * (np.sum(targets) / total_mentions)
            macro_f1 += metrics.f1_score(targets, preds, average='macro', zero_division=0) * (np.sum(targets) / total_mentions)
            weighted_f1 += metrics.f1_score(targets, preds, average='weighted', zero_division=0) * (np.sum(targets) / total_mentions)

            print('CheXbert: Presence')
            df, preds, targets = evaluate_labels(true_df, chexbert_df, method='presence')
            df.columns = pd.MultiIndex.from_tuples([('CheXbert', c) for c in df.columns])
            df.columns = df.columns.reorder_levels([1, 0])
            df = df[['precision', 'recall', 'f1', 'positives']]
            for c in df.columns:
                if 'float' in str(df.dtypes[c]):
                    df[c] = np.round(df[c], 3)

            df.index.name = 'Presence'
            print(df)
            print()

            micro_f1 += metrics.f1_score(targets, preds, average='micro', zero_division=0) * (np.sum(targets) / total_mentions)
            macro_f1 += metrics.f1_score(targets, preds, average='macro', zero_division=0) * (np.sum(targets) / total_mentions)
            weighted_f1 += metrics.f1_score(targets, preds, average='weighted', zero_division=0) * (np.sum(targets) / total_mentions)

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
    parser = argparse.ArgumentParser(description="Process CheXbert predictions and compute F1 scores.")
    parser.add_argument('--true_labels', type=str, required=True, help="Path to the true labels CSV file")
    parser.add_argument('--pred_labels_dir', type=str, required=True, help="Directory containing prediction CSV files")
    parser.add_argument('--test_report_path', type=str, required=True, help="Path to the test set reports CSV file")
    
    args = parser.parse_args()

    compute_chexbert_f1_scores(args.true_labels, args.pred_labels_dir, args.test_report_path)
