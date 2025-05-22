from Bio import SeqIO
import sys

def remove_duplicate_sequences(input_fasta, output_fasta):
    """Remove duplicate sequences while preserving full headers."""
    seen_sequences = set()
    unique_records = []

    for record in SeqIO.parse(input_fasta, "fasta"):
        sequence = str(record.seq)
        if sequence not in seen_sequences:
            seen_sequences.add(sequence)
            # Preserve the original header (description line)
            unique_records.append(record)

    # Write output while keeping full headers
    with open(output_fasta, "w") as out_handle:
        for record in unique_records:
            out_handle.write(f">{record.description}\n{record.seq}\n")

    print(f"Removed duplicates. Kept {len(unique_records)} unique sequences out of {sum(1 for _ in SeqIO.parse(input_fasta, 'fasta'))} total.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python remove_duplicates.py input.fasta output.fasta")
        sys.exit(1)
    remove_duplicate_sequences(sys.argv[1], sys.argv[2])