# Carbapenemase-Resistance-in-Enterococcus

## Pipeline Summary

This repository contains four scripts that must be executed sequentially:

1. **get_gene_fastas.py**  
   Reads a CSV file listing resistant genes and obtains the corresponding FASTA sequences.

2. **calculate_gene_lengths.py**  
   Parses each FASTA generated in Step 1 and prints out the nucleotide lengths for checking.

3. **rename_genes.py**  
   Renames sequences and FASTA headers using the format "GENEID_ALLELE".

4. **blast_genes_against_genomes.py**  
   BLASTs each renamed gene sequence against a local collection of bacterial genomes.

## Input Requirements

Users must edit the following fields:

- **Email address** — required for Entrez queries.
- **Input files** — Folder with subfolders containing FNA files of genomes and CSV file with a series of meta data from resistant genes.

  For example:
  
  #Allele,Gene family,Product name,Scope,Type,Subtype,Class,Subclass,RefSeq protein,RefSeq nucleotide,GenBank protein,GenBank nucleotide,Curated RefSeq start,Links
,"blaOXA/blaLRA13","bifunctional class C beta-lactamase/class D beta-lactamase fusion protein LRA-13","core","AMR","AMR","BETA-LACTAM","BETA-LACTAM","WP_063839877.1","NG_047216.1","ACH58991.1","EU408352.1","No",0
"blaOXA-1000","blaOXA","OXA-213 family carbapenem-hydrolyzing class D beta-lactamase OXA-1000","core","AMR","AMR","BETA-LACTAM","CARBAPENEM","WP_231869625.1","NG_078021.1","QWA20199.1","MZ265752.1","No",0

- **Output directories / filenames** — specify where results should be written.

Each script has placeholders marked with:
    # TODO: Enter your email
    # TODO: Specify input file
    # TODO: Specify output from previous script
    # TODO: Specify output directory
