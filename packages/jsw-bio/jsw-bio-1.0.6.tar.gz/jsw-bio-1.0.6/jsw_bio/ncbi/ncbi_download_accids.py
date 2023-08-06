import requests
from bs4 import BeautifulSoup

QUERY_KEY = '[name="EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.QueryKey"]'


def ncbi_download_accids(**kwargs):
    term = kwargs.get('term')
    res1 = requests.get(f'https://www.ncbi.nlm.nih.gov/protein/?term={term}')
    soup = BeautifulSoup(res1.text, 'html.parser')
    query_key_el = soup.select_one(QUERY_KEY)
    query_key = query_key_el.attrs['value']
    res2 = requests.get(
        f'https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?db=protein&report=accnlist&query_key={query_key}',
        cookies=res1.cookies)

    result = []
    for acc in res2.text.split('\n'):
        if acc:
            result.append(acc)
    return result
