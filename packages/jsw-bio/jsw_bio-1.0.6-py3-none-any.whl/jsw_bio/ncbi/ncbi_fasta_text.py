import requests


def ncbi_fasta_text(**kwargs):
    id = kwargs.get('id')
    res = requests.get(
        f'https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id={id}&report=fasta')
    if res.status_code == 200:
        return res.text
    return None
