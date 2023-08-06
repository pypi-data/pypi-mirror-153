def ncbi_serialize_fasta(fasta):
    if fasta:
        seqs = fasta.split('\n')[1:]
        return ''.join(seqs)
    return None
