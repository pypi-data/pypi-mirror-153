import requests
from bs4 import BeautifulSoup
from .settings import *

QUERY_KEY = '[name="EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.QueryKey"]'


def ncbi_download_accids(**kwargs):
    term = kwargs.get('term')
    filename = kwargs.get('filename', f'{term}.list')
    chunk_size = kwargs.get('chunk_size', 1024)
    res1 = requests.get(f'{BASE_URL}/protein/?term={term}')
    soup = BeautifulSoup(res1.text, 'html.parser')
    query_key_el = soup.select_one(QUERY_KEY)
    query_key = query_key_el.attrs['value']
    res2 = requests.get(f'{BASE_URL}/sviewer/viewer.cgi?db=protein&report=accnlist&query_key={query_key}',
                        stream=True,
                        cookies=res1.cookies)

    with open(filename, "wb") as f:
        for chunk in res2.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                f.flush()
