#!/usr/bin/env python3

import csv
import argparse
from pathlib import Path

def convert_csv_to_fasta(input_files, output_fasta):
    """
    Convert CSV files containing sequence data to FASTA format.
    
    Args:
        input_files (list): List of input CSV file paths
        output_fasta (str): Output FASTA file path
    """
    entries = []

    for filename in input_files:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                subject_id = row.get('subject_id', '').strip()
                protein_seq = row.get('Protein Sequence', '').strip()
                # Skip rows with missing data
                if subject_id and protein_seq:
                    entries.append((subject_id, protein_seq))

    # Create output directory if it doesn't exist
    output_path = Path(output_fasta)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as fasta:
        for subject_id, protein_seq in entries:
            fasta.write(f'>{subject_id}\n{protein_seq}\n')

    print(f'FASTA file written to {output_fasta}')
    print(f'Total sequences processed: {len(entries)}')

def main():
    parser = argparse.ArgumentParser(
        description='Convert CSV files containing sequence data to FASTA format'
    )
    parser.add_argument(
        '-i', '--input',
        nargs='+',
        required=True,
        help='Input CSV file(s). Multiple files can be specified.'
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output FASTA file path'
    )

    args = parser.parse_args()
    convert_csv_to_fasta(args.input, args.output)

if __name__ == '__main__':
    main()
