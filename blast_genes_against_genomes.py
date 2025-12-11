import os
os.environ['PATH'] = r'TODO: Specify input file' + os.pathsep + os.environ['PATH'] # Prepend the directory for Blast+ installation

from Bio.Blast.Applications import NcbiblastnCommandline, NcbimakeblastdbCommandline
from Bio.Blast import NCBIXML
from Bio import SeqIO
import csv
from datetime import datetime

DATA_DIR = "TODO: Specify input file"  #Enter the name of the file with all the subfolders containing the FNA files
NDM_FASTA = "TODO: Specify output from *rename_genes.py*" 
OUTPUT_CSV = "TODO: Specify output directory"
IDENTITY_THRESHOLD = 99


genome_folders = [f for f in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, f))]
total_genomes = len(genome_folders)

print(f"Found {total_genomes} genome folders")
print(f"Loaded NDM alleles from {NDM_FASTA}\n")

with open(OUTPUT_CSV, "w", newline="") as csvfile:
    fieldnames = ["genome_folder", "fna_file", "ndm_allele", "match_start", "match_end", "identity", "alignment_length"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for genome_idx, genome_folder in enumerate(genome_folders, 1):
        folder_path = os.path.join(DATA_DIR, genome_folder)
        
        fna_files = [f for f in os.listdir(folder_path) if f.endswith(".fna")]
        if not fna_files:
            print(f"[{genome_idx}/{total_genomes}] No FNA file in {genome_folder}")
            continue

        fna_path = os.path.join(folder_path, fna_files[0])
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [{genome_idx}/{total_genomes}] Processing {genome_folder}")
        
        db_name = os.path.join(folder_path, "temp_db")
        makedb_cline = NcbimakeblastdbCommandline(
            dbtype="nucl",
            input_file=fna_path,
            out=db_name
        )
        makedb_cline()
        
        blast_output = os.path.join(folder_path, "blast_results.xml")
        blastn_cline = NcbiblastnCommandline(
            query=NDM_FASTA,
            db=db_name,
            evalue=1e-10,
            outfmt=5,
            out=blast_output,
            num_threads=4,
            perc_identity=IDENTITY_THRESHOLD
        )
        blastn_cline()
        
        with open(blast_output) as result_handle:
            blast_records = NCBIXML.parse(result_handle)
            
            for blast_record in blast_records:
                allele_id = blast_record.query
                
                if blast_record.alignments:
                    print(f"  ✓ {allele_id}: {len(blast_record.alignments)} hit(s)")
                    
                    for alignment in blast_record.alignments:
                        for hsp in alignment.hsps:
                            identity_pct = 100 * hsp.identities / hsp.align_length
                            
                            if identity_pct >= IDENTITY_THRESHOLD:
                                writer.writerow({
                                    "genome_folder": genome_folder,
                                    "fna_file": fna_files[0],
                                    "ndm_allele": allele_id,
                                    "match_start": hsp.sbjct_start,
                                    "match_end": hsp.sbjct_end,
                                    "identity": round(identity_pct, 2),
                                    "alignment_length": hsp.align_length
                                })

print("\n✓ Search complete!")
