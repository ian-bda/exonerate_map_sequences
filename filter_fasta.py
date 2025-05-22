import sys

def parse_clusters(cluster_filename):
    """
    Parse the cluster file, returning a dict:
    {species: [[seqid1, seqid2, ...], [seqid3, ...], ...]}
    Each inner list is a cluster's sequence IDs.
    """
    clusters = {}
    current_species = None
    current_cluster = None
    with open(cluster_filename) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('=== File:'):
                current_species = line.split('=== File: ')[1].split('_exonerate.out')[0]
                clusters[current_species] = []
                current_cluster = None
            elif line.strip().startswith('Cluster'):
                current_cluster = []
                clusters[current_species].append(current_cluster)
            elif current_species and line.strip().startswith(current_species):
                seqid = line.strip().split()[0]
                if current_cluster is not None:
                    current_cluster.append(seqid)
            elif line.strip() == "":
                current_cluster = None  # End of cluster
    return clusters

def parse_fasta(fasta_filename):
    """
    Parse a FASTA file into a dict {seqid: sequence}
    """
    seqs = {}
    with open(fasta_filename) as f:
        seqid = None
        seq = []
        for line in f:
            if line.startswith('>'):
                if seqid:
                    seqs[seqid] = ''.join(seq)
                seqid = line[1:].split()[0]
                seq = []
            else:
                seq.append(line.strip())
        if seqid:
            seqs[seqid] = ''.join(seq)
    return seqs

def write_fasta(seqs, seqids, outfilename):
    """
    Write selected seqids from seqs dict to a FASTA file.
    """
    with open(outfilename, 'w') as out:
        for seqid in seqids:
            if seqid in seqs:
                out.write(f'>{seqid}\n')
                for i in range(0, len(seqs[seqid]), 60):
                    out.write(seqs[seqid][i:i+60] + '\n')
            else:
                print(f'WARNING: {seqid} not found in FASTA!', file=sys.stderr)

def main(cluster_txt, fasta_file, output_fasta):
    clusters = parse_clusters(cluster_txt)
    seqs = parse_fasta(fasta_file)
    selected_seqids = []
    for species in clusters:
        for cluster in clusters[species]:
            # Select the longest sequence in the cluster
            longest_seqid = None
            max_len = -1
            for seqid in cluster:
                if seqid in seqs:
                    seqlen = len(seqs[seqid])
                    if seqlen > max_len:
                        max_len = seqlen
                        longest_seqid = seqid
            if longest_seqid:
                selected_seqids.append(longest_seqid)
    write_fasta(seqs, selected_seqids, output_fasta)
    print(f'Wrote {len(selected_seqids)} sequences to {output_fasta}')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python filter_fasta.py <cluster_txt> <input_fasta> <output_fasta>")
        sys.exit(1)
    cluster_txt = sys.argv[1]
    fasta_file = sys.argv[2]
    output_fasta = sys.argv[3]
    main(cluster_txt, fasta_file, output_fasta)
