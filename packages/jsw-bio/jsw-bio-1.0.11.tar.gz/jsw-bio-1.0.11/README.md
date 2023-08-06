# jsw-bio
> Jsw for biography.

## installation
```shell
pip install jsw-bio -U
```

## usage
```python
import jsw_bio as bio

## common methods
# get fasta/genbank url
bio.url('7EU9_A', 'fasta')
bio.url('7EU9_A', 'gb')
bio.ncbi_download_accids(term='cas12') # ['VEJ66715.1', 'SUY72866.1', 'SUY81473.1', ...
```
