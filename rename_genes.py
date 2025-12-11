from Bio import SeqIO

new_fasta = "TODO: Specify output directory"

with open(new_fasta, "w") as out_f:
    for i, record in enumerate(SeqIO.parse("TODO: Spefify output from **get_gene_fastas.py**", "fasta"), 1):
        new_id = f"ndm_allele_{i}|{record.id}"
        out_f.write(f">{new_id}\n{record.seq}\n")
