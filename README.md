
http://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/average_template/
http://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/ara_nissl/


## Uncompress and read data
Check header by
```sh
head -n 12 data/ara_nissl_10.nrrd
```
and ensure that `encoding` is `gzip`. Then decompress into file with
```sh
tail -n +14 ara_nissl_10.nrrd | gzip -d - > decompressed.b
```
This decompressed file can now be read directly into a `numpy` `ndarray` by
```python
a = np.fromfile('data/decompressed.b', dtype='f4')
a = np.reshape(a, (1140, 800, 1320)).T
```
where the `dtype` is found by the `type` field in the header and mapped by [the lookup table from `pynrrd`](https://github.com/mhe/pynrrd/blob/master/nrrd/reader.py#L44-L86), and the sizes are read from the `sizes` field in the header.

> Note the ordering of the sizes; the `nrrd` file format uses Fortran-style indexing, while NumPy uses C-style indexing, hence requiring reversing the order. This is strictly necessary. However, we can switch between the two by transposing the data array -- hence the (optional) `.T` and the end of the line.

First decompressing and then afterwards reading the raw, uncompressed data, seems to significantly faster, and for some reason uses much less memory (actually making reading feasible on my machine).

