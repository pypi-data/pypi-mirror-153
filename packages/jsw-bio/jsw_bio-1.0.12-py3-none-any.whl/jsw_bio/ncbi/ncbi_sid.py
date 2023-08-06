import requests
from .settings import *


def ncbi_sid(**kwargs):
    term = kwargs.get('term', 'cas15')
    res = requests.head(f'{BASE_URL}/protein/?term={term}')
    return res.headers['NCBI-SID']
