import requests
from .settings import *
from .ncbi_serialize_fasta import ncbi_serialize_fasta


def ncbi_fasta_text(**kwargs):
    id = kwargs.get('id')
    serialize = kwargs.get('serialize', False)
    res = requests.get(f'{BASE_URL}/sviewer/viewer.fcgi?id={id}&report=fasta')
    seq = None

    if res.status_code == 200:
        seq = res.text

    return ncbi_serialize_fasta(seq) if serialize else seq
