import requests
from bs4 import BeautifulSoup

NCBI_BASE_URL = 'https://www.ncbi.nlm.nih.gov'
QUERY_KEY = '[name="EntrezSystem2.PEntrez.Protein.Sequence_ResultsPanel.Sequence_DisplayBar.QueryKey"]'


def ncbi_download_accids(**kwargs):
    keyword = kwargs.get('keyword')
    res1 = requests.get(f'{NCBI_BASE_URL}/protein/?term={keyword}')
    soup = BeautifulSoup(res1.text, 'html.parser')
    query_key_el = soup.select_one(QUERY_KEY)
    query_key = query_key_el.attrs['value']
    res2 = requests.get(f'{NCBI_BASE_URL}/sviewer/viewer.cgi?db=protein&report=accnlist&query_key={query_key}',
                        cookies=res1.cookies)

    result = []
    for acc in res2.text.split('\n'):
        if acc:
            result.append(acc)
    return result
