import requests


def ncbi_sid(**kwargs):
    term = kwargs.get('term', 'cas15')
    res = requests.head(f'https://www.ncbi.nlm.nih.gov/protein/?term={term}')
    return res.headers['NCBI-SID']
