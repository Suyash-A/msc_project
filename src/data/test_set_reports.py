import sys
import os
import argparse
import csv
from pathlib import Path
from tqdm import tqdm
import section_parser as sp

parser = argparse.ArgumentParser()
parser.add_argument('--reports_path',
                    required=True,
                    help=('Path to file with radiology reports,'
                          ' e.g. /data/mimic-cxr/files'))
parser.add_argument('--output_path',
                    required=True,
                    help='Path to output CSV files.')
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

    custom_section_names, custom_indices = sp.custom_mimic_cxr_rules()

    # Read the study list CSV
    study_list = {}
    with open(study_list_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            study_list[row['path']] = row

    # Collect patient studies and their sections
    patient_studies = []
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
        if s_stem in custom_section_names:
            sn = custom_section_names[s_stem]
            idx = list_rindex(section_names, sn)
            patient_studies.append([s_stem, sections[idx].strip()])
            continue

        # Grab the *last* section with the given title
        idx = -1
        for sn in ('impression', 'findings', 'last_paragraph', 'comparison'):
            if sn in section_names:
                idx = list_rindex(section_names, sn)
                break

        if idx == -1:
            patient_studies.append([s_stem, ''])
            print(f'no impression/findings: {report_path}')
        else:
            patient_studies.append([s_stem, sections[idx].strip()])

        study_sectioned = [s_stem]
        for sn in ('impression', 'findings', 'last_paragraph', 'comparison'):
            if sn in section_names:
                idx = list_rindex(section_names, sn)
                study_sectioned.append(sections[idx].strip())
            else:
                study_sectioned.append(None)
        study_sections.append(study_sectioned)

    # Write out a single CSV with the sections
    if len(patient_studies) > 0:
        with open(output_path / 'test_set_reports.csv', 'w') as fp:
            csvwriter = csv.writer(fp)
            csvwriter.writerow(['study', 'impression', 'findings',
                                'last_paragraph', 'comparison'])
            for row in study_sections:
                csvwriter.writerow(row)

if __name__ == '__main__':
    main(sys.argv[1:])
