import sys
import os
import argparse
import csv
import re
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

def clean_csv(file_name, pattern_str):
    # Compile the pattern to remove
    pattern = re.compile(pattern_str)

    # Read the input CSV file into memory
    with open(file_name, 'r') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    # Process the rows
    cleaned_rows = [['Report Impression']]
    for row in rows:
        # Combine the row into a single string and remove the pattern
        cleaned_text = re.sub(pattern, '', ','.join(row))
        cleaned_rows.append([cleaned_text])

    # Write the cleaned rows back to the same file
    with open(file_name, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(cleaned_rows)

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

    # patient_studies will hold the text for use in NLP labeling
    patient_studies = []

    # study_sections will have an element for each study
    # this element will be a list, each element having text for a specific section
    study_sections = []

    # Iterate over the study list
    for path, study_info in tqdm(study_list.items()):
        report_path = reports_path / Path(path)

        # Load in the free-text report
        with open(report_path, 'r') as fp:
            text = ''.join(fp.readlines())

        # Get study string name without the txt extension
        s_stem = report_path.stem

        # Custom rules for some poorly formatted reports
        if s_stem in custom_indices:
            idx = custom_indices[s_stem]
            patient_studies.append([s_stem, text[idx[0]:idx[1]]])
            continue

        # Split text into sections
        sections, section_names, section_idx = sp.section_text(text)

        # Check to see if this has mis-named sections
        # e.g. sometimes the impression is in the comparison section
        if s_stem in custom_section_names:
            sn = custom_section_names[s_stem]
            idx = list_rindex(section_names, sn)
            patient_studies.append([s_stem, sections[idx].strip()])
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
            patient_studies.append([s_stem, ''])
            print(f'no impression/findings: {report_path}')
        else:
            # Store the text of the conclusion section
            patient_studies.append([s_stem, sections[idx].strip()])

        study_sectioned = [s_stem]
        for sn in ('impression', 'findings', 'last_paragraph', 'comparison'):
            if sn in section_names:
                idx = list_rindex(section_names, sn)
                study_sectioned.append(sections[idx].strip())
            else:
                study_sectioned.append(None)
        study_sections.append(study_sectioned)

    # Write distinct files to facilitate modular processing
    if len(patient_studies) > 0:
        # Write out a single CSV with the sections
        # with open(output_path / 'mimic_cxr_sectioned.csv', 'w') as fp:
        #     csvwriter = csv.writer(fp)
        #     # Write header
        #     csvwriter.writerow(['study', 'impression', 'findings',
        #                         'last_paragraph', 'comparison'])
        #     for row in study_sections:
        #         csvwriter.writerow(row)

        # if args.no_split:
        #     # Write all the reports out to a single file
        #     with open(output_path / f'input_visualchexbert.csv', 'w') as fp:
        #         csvwriter = csv.writer(fp)
        #         for row in patient_studies:
        #             csvwriter.writerow(row)

        if args.no_split:
                # Write all the reports out to a single file
                output_file = output_path / 'input_visualchexbert.csv'
                with open(output_file, 'w', newline='') as fp:
                    csvwriter = csv.writer(fp)
                    for row in patient_studies:
                        csvwriter.writerow(row)

                # Clean the output CSV file
                clean_csv(output_file, r'^s\d+,')

        else:
            # Write ~22 files with ~10k reports each
            n = 0
            jmp = 10000

            while n < len(patient_studies):
                n_fn = n // jmp
                with open(output_path / f'mimic_cxr_{n_fn:02d}.csv', 'w') as fp:
                    csvwriter = csv.writer(fp)
                    for row in patient_studies[n:n+jmp]:
                        csvwriter.writerow(row)
                n += jmp


if __name__ == '__main__':
    main(sys.argv[1:])

