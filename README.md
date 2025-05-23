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



### 3. Deduplicate FASTA
Remove duplicate sequences from the FASTA file to ensure only unique entries are used in downstream analysis.

### 4. Run Exonerate
Use `exonerate.py` to align your FASTA sequences to the reference genomes.

```bash
sbatch run_exonerate_python_script.sh
