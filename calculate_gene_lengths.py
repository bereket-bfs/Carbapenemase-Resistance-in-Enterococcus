fasta_file = "TODO: Specify output from *get_genes_fastas.py*"

for record in SeqIO.parse(fasta_file, "fasta"):
    print(record.id, len(record.seq))
