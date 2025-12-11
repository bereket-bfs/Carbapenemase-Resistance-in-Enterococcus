import csv
from Bio import Entrez, SeqIO

# REQUIRED: put your email for NCBI Entrez
Entrez.email = "bereketalemayehu93@gmail.com"

INPUT_FILE = "TODO: Enter your email"
OUTPUT_CSV = "TODO: Specify input file" #Specify the CSV file with resistant gene metadata

def fetch_metadata(accession):
    try:
        handle = Entrez.efetch(db="nucleotide", id=accession,
                               rettype="gb", retmode="text")
        record = SeqIO.read(handle, "genbank")
        handle.close()
        
        organism = record.annotations.get("organism", "")
        
        country = ""
        for feature in record.features:
            if feature.type == "source":
                country = feature.qualifiers.get("country", [""])[0]
                break
        
        collection_date = ""
        for feature in record.features:
            if feature.type == "source":
                collection_date = feature.qualifiers.get("collection_date", [""])[0]
                break
        
        return {
            "organism": organism,
            "country": country,
            "collection_date": collection_date
        }
    
    except Exception as e:
        print(f"Error fetching metadata for {accession}: {e}")
        return {
            "organism": "",
            "country": "",
            "collection_date": ""
        }

def main():
    with open(INPUT_FILE) as infile, open(OUTPUT_CSV, "w", newline="") as outfile:
        reader = csv.DictReader(infile)
        
        fieldnames = ["allele", "accession", "organism", "country", "collection_date"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for idx, row in enumerate(reader, 1):
            allele = row["#Allele"].strip('"')
            accession = row["RefSeq nucleotide"].strip('"')
            
            print(f"[{idx}] Fetching metadata for {allele} ({accession}) ...")
            
            metadata = fetch_metadata(accession)
            
            writer.writerow({
                "allele": allele,
                "accession": accession,
                "organism": metadata["organism"] if metadata["organism"] else "Missing",
                "country": metadata["country"] if metadata["country"] else "Missing",
                "collection_date": metadata["collection_date"] if metadata["collection_date"] else "Missing"
            })
            

    
    print(f"\nDone! Metadata written to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
