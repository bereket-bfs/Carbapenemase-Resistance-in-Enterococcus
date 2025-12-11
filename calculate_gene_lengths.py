fasta_file = "TODO: Specify input file"

for record in SeqIO.parse(fasta_file, "fasta"):
    print(record.id, len(record.seq))
