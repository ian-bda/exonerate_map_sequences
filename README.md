# exonerate_map_sequences

A workflow for mapping and analyzing FASTA sequences against reference genomes using `exonerate`, filtering results, and performing phylogenetic analysis.

---

## Overview

This project automates the process of:
- Mapping sequences from FASTA files to species specific reference genomes
- Analyzing overlapping exonerate results
- Filtering to select representative sequences per cluster per species
- Performing multiple sequence alignment and phylogenetic analysis

---

## Workflow Steps

### 1. Prepare Reference Genomes
Download all necessary reference genome files and organize them in a directory.

```
python download_genomes.py <input.fasta> <output_dir>
```

### 2. Convert Excel Sheets to FASTA
Use a script to convert your Excel-based sequence data into FASTA format.

```
python csv_to_fasta_converter.py -i "Arteodactyl_CD300 - Ensembl.csv" "Arteodactyl_CD300 - NCBI.csv" -o combined_sequences.fasta
```

### 3. Deduplicate FASTA
Remove duplicate sequences from the FASTA file to ensure only unique entries are used in downstream analysis.

```
python remove_duplicate.py input_fasta output_fasta
```
### 4. Run Exonerate
Use `exonerate.py` to align your de-duplicated FASTA sequences to the reference genomes.

- The script automatically creates temporary protein FASTA files for each species and removes them after processing
- If a genome file is missing for a species, the script will skip that species and continue with the others
- Progress is reported to standard output
- Failed jobs are reported with error messages

## Input Requirements

1. **Protein Sequences**: 
   - Must be in FASTA format
   - Headers should follow the format: `Genus_species_identifier`
   - Example: `>Phocoena_sinus_ENSPSNT00000033221.1`

2. **Genome Files**:
   - Must be named as `Genus_species_genome.fna`
   - Should be placed in the genomes directory
   - Example: `Phocoena_sinus_genome.fna`

### Command-line Arguments

- `--proteins`: (Required) Path to the input multi-FASTA file containing protein sequences
- `--genomes_dir`: (Optional) Directory containing reference genomes (default: 'genomes')
- `--output_dir`: (Optional) Output directory for Exonerate results (default: 'exonerate_results')
- `--exonerate_path`: (Optional) Path to the Exonerate executable (default: 'exonerate')
- `--max_workers`: (Optional) Maximum number of parallel Exonerate jobs (default: 4)

### Example

```bash
python exonerate_parallel.py \
    --proteins cetacean_proteins.fasta \
    --genomes_dir ./whale_genomes \
    --output_dir ./exonerate_output \
    --max_workers 8
```

### 5. Run Exonerate overlap analysis
tells you which sequences are overlapping
```
python overlap_exonerate_analysis.py <directory_of_out_files> <cluster.txt>
```

### 6. Filter out overlappign sequences
- Takes one cluster summary file (as you provided)
- Takes one FASTA file (containing all sequences from all species)
- Outputs one filtered FASTA file with one representative per cluster per species (the longest sequence)

```
python filter_fasta.py <cluster.txt> <input_fasta> <output_fasta>
```

