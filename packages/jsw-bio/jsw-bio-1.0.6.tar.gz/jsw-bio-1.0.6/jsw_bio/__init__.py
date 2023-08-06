import pkg_resources

version = pkg_resources.get_distribution('jsw-bio').version
__version__ = version

# next base
from jsw_bio.base.url import url
from jsw_bio.base.keyword import keyword
from jsw_bio.ncbi.ncbi_download_accids import ncbi_download_accids
from jsw_bio.ncbi.ncbi_fasta_text import ncbi_fasta_text
from jsw_bio.ncbi.ncbi_gb_text import ncbi_gb_text
from jsw_bio.ncbi.ncbi_search_ids import ncbi_search_ids
from jsw_bio.ncbi.ncbi_sid import ncbi_sid
