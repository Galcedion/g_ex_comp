# !!! NOT intended for production. NO warranty for any data lost. !!!

## g_ex_comp

### About

This is a learning exercise for me. This is an experimental lossless compression algorithm for text-based files. Compression is done by creating a map / dictionary and replacing the main text accordingly.

### How to use

Call the file with python3 from console.
```bash
python3 g_ex_comp.py
```
Available parameters:
- c - compression mode; following parameter must be the file to compress; compression type must be specified (n, f, ff)
- d - decompression mode; following parameter must be the file to decompress
- o - output file; following parameter must be the file to write
- n - normal compression mode; fullstring compression
- f - fast compression mode; word-phrase based compression
- ff - very fast compression mode; single-word based compression
- q - quiet; suppress informative output

# !!! NOT intended for production. NO warranty for any data lost. !!!