import json

import numpy as np

from .xmlparser import parse_tree_branch


class cziArray:
    _dim_trans = {"X": "x", "Y": "y", "M": "tile", "C": "channel", "S": "z"}

    def __init__(self, czifile):
        self._czi = czifile

    def __getitem__(self, *args):
        sec = {}
        for d, v in zip(list(self._czi.dims), args[0]):
            if d in ["X", "Y"]:  # X and Y are special and read_image returns full tiles
                continue
            sec[d] = v
        try:
            img = self._czi.read_image(**sec)[0]
        except:  # PylibCZI_CDimCoordinatesOverspecifiedException
            return np.zeros(self.chunks, self.dtype)
        return img.astype(self.dtype)

    @property
    def shape(self):
        return self._czi.size

    @property
    def dtype(self):
        return "uint16"

    @property
    def ndim(self):
        return len(self.shape)

    @property
    def dimensions(self):
        dim = {}
        dims_shape = self._czi.get_dims_shape()[0]
        for item in list(self._czi.dims):
            name = self._dim_trans[item]
            shape = dims_shape[item]
            dim[name] = range(shape[0], shape[1])
        return dim

    @property
    def chunks(self):
        return (1,) * len(self.shape[:-2]) + self.shape[-2:]

    def _boundingboxes(self):
        """
        Return the X,Y position of all the tiles inside a
        czi file as a dict
        """

        dims = self._czi.get_dims_shape()[0]

        bbs = {}

        for i_t in range(dims["M"][1]):  # tile
            temp_dict = {}
            for i_c in range(dims["C"][1]):  # channel
                bb = self._czi.get_mosaic_tile_bounding_box(C=i_c, M=i_t, S=0)
                temp_dict[i_c] = {"x": bb.x, "y": bb.y, "w": bb.w, "h": bb.h}
            bbs[i_t] = temp_dict

        return bbs

    @property
    def metadata(self):

        raw_meta = parse_tree_branch(self._czi.meta[0])

        dims = self._czi.get_dims_shape()[0]
        n_tiles = dims["M"][1]
        n_channels = dims["C"][1]

        bbs = self._boundingboxes()
        x0 = []
        y0 = []
        xs = []
        ys = []
        # we use dims['x'] instead of actual size
        # because we pad
        for i_t in range(n_tiles):
            for i_c in range(n_channels):
                x0.append(bbs[i_t][i_c]["x"])
                xs.append(dims["X"][1])
                y0.append(bbs[i_t][i_c]["y"])
                ys.append(dims["Y"][1])

        raw_meta["tile_start_x"] = x0
        raw_meta["tile_start_y"] = y0
        raw_meta["tile_size_x"] = xs
        raw_meta["tile_size_y"] = ys

        raw_meta["Metadata"] = json.dumps(raw_meta["Metadata"])
        return raw_meta
