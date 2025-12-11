import csv
from Bio import Entrez, SeqIO

Entrez.email = "TODO: Enter your email"

INPUT_FILE = "TODO: Specify input file"      # Enter the name of your input metadata file with columns
OUTPUT_FASTA = "TODO: Specify output directory" # Enter the name of the output FASTA file

def fetch_fasta(accession):
    try:
        handle = Entrez.efetch(db="nucleotide", id=accession,
                               rettype="fasta", retmode="text")
        return handle.read()
    except Exception as e:
        print(f"Error fetching {accession}: {e}")
        return None

def main():
    with open(INPUT_FILE) as infile, open(OUTPUT_FASTA, "w") as outfile:
        reader = csv.DictReader(infile)

        for row in reader:
            allele = row["#Allele"].strip('"')
            accession = row["RefSeq nucleotide"].strip('"')

            print(f"Fetching {allele} ({accession}) ...")

            fasta = fetch_fasta(accession)
            if fasta:
                lines = fasta.strip().split("\n")
                header = f">{allele}"
                sequence = "".join(lines[1:])
                outfile.write(f"{header}\n{sequence}\n")

    print(f"Done! Output written to {OUTPUT_FASTA}")

if __name__ == "__main__":
    main()
