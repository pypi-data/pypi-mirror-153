import jsw_nx as nx


def url(in_id, in_report, **kwargs):
    ext_opts = dict(kwargs)
    opts = nx.mix({'db': 'protein', 'retmode': 'text', 'report': in_report}, ext_opts)
    param = nx.param(opts)
    return f'https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id={in_id}&{param}'
