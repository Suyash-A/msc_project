import sys
import os
import argparse
import csv
from pathlib import Path

from tqdm import tqdm

# local folder import
import section_parser as sp

parser = argparse.ArgumentParser()
parser.add_argument('--reports_path',
                    required=True,
                    help=('Path to file with radiology reports,'
                          ' e.g. /data/mimic-cxr/files'))
parser.add_argument('--output_path',
                    required=True,
                    help='Path to output CSV files.')
parser.add_argument('--no_split', action='store_true',
                    help='Do not output batched CSV files.')
parser.add_argument('--study_list',
                    required=True,
                    help='Path to the CSV file containing the list of studies to process.')

def list_rindex(l, s):
    """Helper function: *last* matching element in a list"""
    return len(l) - l[-1::-1].index(s) - 1

def main(args):
    args = parser.parse_args(args)

    reports_path = Path(args.reports_path)
    output_path = Path(args.output_path)
    study_list_path = Path(args.study_list)

    if not output_path.exists():
        output_path.mkdir()

    # not all reports can be automatically sectioned
    # we load in some dictionaries which have manually determined sections
    custom_section_names, custom_indices = sp.custom_mimic_cxr_rules()

    # Read the study list CSV
    study_list = {}
    with open(study_list_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            study_list[row['path']] = row

    # study_ids will hold only the study IDs
    study_ids = []

    # Iterate over the study list
    for path, study_info in tqdm(study_list.items()):
        report_path = reports_path / Path(path)

        # Load in the free-text report
        with open(report_path, 'r') as fp:
            text = ''.join(fp.readlines())

        # Get study string name without the txt extension and remove the first character
        s_stem = report_path.stem[1:]

        # Custom rules for some poorly formatted reports
        if s_stem in custom_indices:
            idx = custom_indices[s_stem]
            study_ids.append([s_stem])
            continue

        # Split text into sections
        sections, section_names, section_idx = sp.section_text(text)

        # Check to see if this has mis-named sections
        # e.g. sometimes the impression is in the comparison section
        if s_stem in custom_section_names:
            sn = custom_section_names[s_stem]
            idx = list_rindex(section_names, sn)
            study_ids.append([s_stem])
            continue

        # Grab the *last* section with the given title
        # prioritizes impression > findings, etc.
        idx = -1
        for sn in ('impression', 'findings', 'last_paragraph', 'comparison'):
            if sn in section_names:
                idx = list_rindex(section_names, sn)
                break

        if idx == -1:
            # We didn't find any sections we can use :(
            study_ids.append([s_stem])
            print(f'no impression/findings: {report_path}')
        else:
            # Store the study ID
            study_ids.append([s_stem])

    # Write distinct files to facilitate modular processing
    if len(study_ids) > 0:
        if args.no_split:
            # Write all the reports out to a single file
            with open(output_path / f'ordered_test_ids.csv', 'w') as fp:
                csvwriter = csv.writer(fp)
                csvwriter.writerow(['study_id'])  # Add the column name
                for row in study_ids:
                    csvwriter.writerow(row)
        else:
            # Write ~22 files with ~10k reports each
            n = 0
            jmp = 10000

            while n < len(study_ids):
                n_fn = n // jmp
                with open(output_path / f'mimic_cxr_{n_fn:02d}.csv', 'w') as fp:
                    csvwriter = csv.writer(fp)
                    csvwriter.writerow(['study_id'])  # Add the column name
                    for row in study_ids[n:n+jmp]:
                        csvwriter.writerow(row)
                n += jmp

if __name__ == '__main__':
    main(sys.argv[1:])
