from Bio import Entrez

Entrez.email = "A.N.Other@example.com"  # Always tell NCBI who you are


def ncbi_search_ids(**kwargs):
    handle = Entrez.esearch(db="protein", retmax=1000000, **kwargs)
    record = Entrez.read(handle)
    return record["IdList"]
