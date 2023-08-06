# AXIO to Zarr converter


Convert AXIOSCAN dataset to Zarr.

NOTE: only those AXIOSCAN datasets with SCMYX dimensions where S=1 are supported at the moment.

## Install

```
pip install axio2zarr
```

### Requirements

* aicspylibczi
* click
* dask
* numpy
* xarray
* zarray
## Usage

### From Python script

```
from axio2zarr import axio2zarr

axio2zarr(input_path, output_path)
```

### From command line

```
axio2zarr input_path output_path