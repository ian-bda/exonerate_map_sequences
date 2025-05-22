import os
import re

def parse_gene_regions(file_path):
    regions = []
    with open(file_path) as f:
        for line in f:
            if line.startswith("#") or line.strip() == "":
                continue
            if re.search(r'\tgene\t', line):
                fields = line.strip().split('\t')
                seqname = fields[0]
                start = int(fields[3])
                end = int(fields[4])
                strand = fields[6]
                attributes = fields[8]
                match = re.search(r'sequence\s+(\S+)', attributes)
                seq_id = match.group(1) if match else "unknown"
                regions.append((seq_id, seqname, start, end, strand))
    return regions

def regions_overlap(r1, r2):
    return r1[1] == r2[1] and not (r1[3] < r2[2] or r2[3] < r1[2])

def cluster_regions(regions):
    clusters = []
    for region in regions:
        placed = False
        for cluster in clusters:
            if any(regions_overlap(region, member) for member in cluster):
                cluster.append(region)
                placed = True
                break
        if not placed:
            clusters.append([region])
    return clusters

def main(input_directory, output_file):
    with open(output_file, 'w') as out:
        for filename in sorted(os.listdir(input_directory)):
            if not filename.endswith(".out"):
                continue
            filepath = os.path.join(input_directory, filename)
            regions = parse_gene_regions(filepath)
            clusters = cluster_regions(regions)
            
            out.write(f"\n=== File: {filename} ===\n")
            for i, cluster in enumerate(clusters):
                out.write(f"  Cluster {i+1}:\n")
                for r in cluster:
                    out.write(f"    {r[0]} ({r[1]}:{r[2]}-{r[3]}, strand {r[4]})\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python overlap_exonerate_analysis.py <directory_of_out_files> <output_file.txt>")
    else:
        input_dir = sys.argv[1]
        output_txt = sys.argv[2]
        main(input_dir, output_txt)
