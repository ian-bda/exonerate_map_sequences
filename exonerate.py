#!/usr/bin/env python3
import os
import subprocess
from Bio import SeqIO
import argparse
import concurrent.futures

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run Exonerate to map protein sequences to reference genomes in parallel.")
    parser.add_argument("--proteins", required=True, help="Input multi-FASTA file containing protein sequences.")
    parser.add_argument("--genomes_dir", default="genomes", help="Directory containing reference genomes (default: 'genomes').")
    parser.add_argument("--output_dir", default="exonerate_results", help="Output directory for Exonerate results (default: 'exonerate_results').")
    parser.add_argument("--exonerate_path", default="exonerate", help="Path to the Exonerate executable (default: 'exonerate').")
    parser.add_argument("--max_workers", type=int, default=4, help="Maximum number of parallel Exonerate jobs (default: 4).")
    return parser.parse_args()

def extract_species_id(header):
    """Extract 'Genus_species' from header (e.g., 'Phocoena_sinus_ENSPSNT00000033221.1' -> 'Phocoena_sinus')."""
    parts = header.split("_")
    return f"{parts[0]}_{parts[1]}"

def run_exonerate_for_species(args):
    species_id, protein_records, genomes_dir, output_dir, exonerate_path = args
    genome_file = os.path.join(genomes_dir, f"{species_id}_genome.fna")
    if not os.path.exists(genome_file):
        print(f"Warning: Genome file {genome_file} not found. Skipping {species_id}.")
        return
    temp_protein_file = os.path.join(output_dir, f"{species_id}_proteins.fasta")
    SeqIO.write(protein_records, temp_protein_file, "fasta")
    output_file = os.path.join(output_dir, f"{species_id}_exonerate.out")
    cmd = [
        exonerate_path,
        "--model", "protein2genome",
        "--query", temp_protein_file,
        "--target", genome_file,
        "--showtargetgff", "true",
        "--verbose", "0",
        "--bestn", "1"
    ]
    print(f"Running Exonerate for {species_id}...")
    try:
        with open(output_file, "w") as out_fh:
            subprocess.run(cmd, stdout=out_fh, check=True)
        print(f"Results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running Exonerate for {species_id}: {e}")
    finally:
        if os.path.exists(temp_protein_file):
            os.remove(temp_protein_file)

def run_exonerate(protein_file, genomes_dir, output_dir, exonerate_path, max_workers):
    os.makedirs(output_dir, exist_ok=True)
    species_to_proteins = {}
    for record in SeqIO.parse(protein_file, "fasta"):
        species_id = extract_species_id(record.id)
        species_to_proteins.setdefault(species_id, []).append(record)
    # Prepare arguments for each species
    args_list = [
        (species_id, protein_records, genomes_dir, output_dir, exonerate_path)
        for species_id, protein_records in species_to_proteins.items()
    ]
    # Parallel execution
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(run_exonerate_for_species, args_list)

if __name__ == "__main__":
    args = parse_arguments()
    run_exonerate(
        protein_file=args.proteins,
        genomes_dir=args.genomes_dir,
        output_dir=args.output_dir,
        exonerate_path=args.exonerate_path,
        max_workers=args.max_workers
    )
