#!/usr/bin/env python3
import os
import re
from Bio import Entrez, SeqIO
import sys

def create_output_dir(output_dir):
    """Create output directory for genomes"""
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def parse_species_from_fasta(fasta_file):
    """Extract unique species names from FASTA headers"""
    species_set = set()
    with open(fasta_file) as f:
        for line in f:
            if line.startswith(">"):
                match = re.match(r'>([A-Za-z]+)_([A-Za-z]+)', line)
                if match:
                    species_set.add(f"{match.group(1)} {match.group(2)}")
    return sorted(species_set)

def download_genome(species, genome_dir):
    """Download genome if not already exists"""
    species_underscore = species.replace(" ", "_")
    genome_file = os.path.join(genome_dir, f"{species_underscore}_genome.fna.gz")
    
    if os.path.exists(genome_file) or os.path.exists(genome_file[:-3]):
        print(f"Genome exists for {species}, skipping download")
        return genome_file
    
    Entrez.email = "ibirchl@ncsu.edu"
    print(f"Searching for {species} reference genome...")
    
    try:
        # First try with reference genome filter
        handle = Entrez.esearch(db="assembly", 
                              term=f'"{species}"[Organism] AND latest[filter] AND "reference genome"[filter]',
                              retmax=1)
        record = Entrez.read(handle)
        handle.close()
        
        # If no reference genome, try with less restrictive filter
        if not record["IdList"]:
            handle = Entrez.esearch(db="assembly", 
                                  term=f'"{species}"[Organism] AND latest[filter]',
                                  retmax=1)
            record = Entrez.read(handle)
            handle.close()
        
        if not record["IdList"]:
            print(f"No genome found for {species}")
            return None
        
        assembly_id = record["IdList"][0]
        handle = Entrez.esummary(db="assembly", id=assembly_id)
        summary = Entrez.read(handle)
        handle.close()
        
        doc_summary = summary['DocumentSummarySet']['DocumentSummary'][0]
        ftp_path = doc_summary.get('FtpPath_RefSeq', '')
        
        if not ftp_path:
            ftp_path = doc_summary.get('FtpPath_GenBank', '')
            if not ftp_path:
                print(f"No FTP path for {species}")
                return None
        
        basename = os.path.basename(ftp_path)
        gbff_url = f"{ftp_path}/{basename}_genomic.fna.gz"
        
        print(f"Downloading from {gbff_url}")
        if os.system(f"wget -q {gbff_url} -O {genome_file}") != 0:
            print(f"Download failed for {species}")
            return None
            
        return genome_file
        
    except Exception as e:
        print(f"Error downloading genome for {species}: {str(e)}")
        return None

def main(fasta_file, output_dir):
    genome_dir = create_output_dir(output_dir)
    species_list = parse_species_from_fasta(fasta_file)
    print(f"Found species: {', '.join(species_list)}")
    
    for species in species_list:
        print(f"\nProcessing {species}")
        genome_file = download_genome(species, genome_dir)
        if genome_file:
            print(f"Successfully downloaded genome for {species}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python download_genomes.py <input.fasta> <output_dir>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])