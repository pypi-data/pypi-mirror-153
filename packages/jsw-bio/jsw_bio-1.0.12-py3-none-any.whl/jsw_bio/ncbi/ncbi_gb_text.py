import requests
import jsw_nx as nx
from .settings import *


def ncbi_gb_text(**kwargs):
    id = kwargs.get('id')
    qs = nx.param({'id': id, 'db': 'protein', 'report': 'genpept', 'retmode': 'text'})
    res = requests.get(f'{BASE_URL}/sviewer/viewer.fcgi?{qs}')
    if res.status_code == 200:
        return res.text
    return None
