# -*- coding: utf-8 -*-

from typing import Optional, Iterable, Tuple, Union
from glob import glob
import os
import io
import bz2
from itertools import cycle, islice, product
from functools import partial
from collections import namedtuple

import numpy as np
import pandas as pd
import xarray as xr
import h5py as h5

from . import log


LOGGER = log.getLogger("evl.core.track")


class Track(pd.DataFrame):
    """A Dataframe which has an index representing ordered absolute
    time instants for each observation"""
    IDX_NAME = "t"

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        assert self.index.dtype == np.dtype("float")
        assert self.index.is_monotonic_increasing
        self.index.rename(self.IDX_NAME, inplace=True)
        self.columns = list(map(str, self.columns))

    @property
    def _constructor(self):
        return self.__class__

    @classmethod
    def from_json(cls, s: str, dtype=None) -> "Track":
        df = pd.read_json(s, orient="split")
        if dtype is not None:
            df = df.astype(dtype, copy=False)
        return cls(df)

    @classmethod
    def from_file(cls, f, dtype=None) -> "Track":
        if type(f) is str:
            io_lib = bz2 if f.endswith(".bz2") else io
            with io_lib.open(f, "rt") as infh:
                return cls.from_json(infh.read(), dtype=dtype)
        else:
            return cls.from_json(f.read(), dtype=dtype)

    @classmethod
    def from_xarray(cls, xar: xr.Dataset) -> "Track":
        return cls(xar.to_dataframe())

    def to_json(self) -> str:
        """No newlines in JSON string"""
        return super(self.__class__, self).to_json(orient="split")

    def to_file(self, f) -> "Track":
        if type(f) is str:
            io_lib = bz2 if f.endswith(".bz2") else io
            with io_lib.open(f, "wt") as outfh:
                outfh.write(self.to_json())
        else:
            f.write(self.to_json())
        return self

    def to_xarray(self) -> xr.Dataset:
        df = pd.DataFrame(self).copy()
        return df.to_xarray()

    def index_near(self, time: float, method: str="nearest") -> int:
        """Returns the index of the sample nearest to time `t`"""
        try:
            method = {"before": "ffill",
                      "after": "bfill"}[method]
        except KeyError:
            pass
        return self.index.get_loc(time, method=method)

    def reset_times(self) -> "Track":
        """Mutates the instance..."""
        self.index = self.index - self.index[0]
        return self

    @property
    def frameperiod(self) -> Optional[float]:
        diffs = np.diff(self.index)
        if np.all(np.isclose(diffs[0], diffs)):
            return diffs[0]


    @classmethod
    def pad(cls,
            trk: "Track",
            n: int,
            repeat_n: Optional[int]=None,
            location: str="back",
            padding: Optional[Union[np.ndarray, "Track"]]=None) -> "Track":
        """Return a new track with length `n` by repeating the first/last
        `repeat_n` frames of the `padding` (if None, the input track
        is used as padding).

        Conditions:
        - `padding` must be at least of length `repeat_n`.
        - The input should be no longer than `n` and have constant framerate.
        """
        frameperiod = trk.frameperiod
        if frameperiod is None:
            raise ValueError("Cannot pad track; not constant framerate...")
        #
        if padding is None:
            padding = trk.to_numpy()
        else:
            assert type(padding) in (np.ndarray, cls)
            padding = padding if isinstance(padding, np.ndarray) else padding.to_numpy()
            assert len(padding.shape) == 2, ValueError(f'Pad shape is {padding.shape}!')
            assert trk.values.shape[1] == padding.shape[1]
        #
        framediff = n - len(trk)
        if framediff < 0:
            raise ValueError("Cannot pad track; track longer than target length...")
        elif framediff == 0:
            return trk.copy()
        if repeat_n is None:
            repeat_n = min(framediff, len(padding))
        if repeat_n > len(padding):
            raise ValueError("Cannot pad track; pad length longer than padding...")
        #
        if location == "both":
            a_length = len(trk) + int(framediff / 2)
            t = cls.pad(trk, a_length, repeat_n, location="front", padding=padding)
            t = cls.pad(t, n, repeat_n, location="back", padding=padding)
            return t
        else:
            new_index = np.zeros(len(trk) + framediff, dtype=np.float)
            values = trk.to_numpy()
            if location == "back":
                new_index[:len(trk)] = trk.index
                new_times = np.arange(1, 1+framediff, dtype=np.float)
                new_times *= frameperiod
                new_times += trk.index[-1]
                new_index[len(trk):] = new_times
                #
                if repeat_n == framediff:
                    pad_values = padding[-framediff:]
                else:
                    src_idxs = (len(trk) - 1) - np.array(list(islice(cycle(reversed(range(repeat_n))),
                                                                     framediff)))
                    pad_values = padding[src_idxs]
                new_values = np.concatenate((values, pad_values))
            elif location == "front":
                new_index[-len(trk):] = trk.index
                new_times = np.arange(-framediff, 0, dtype=np.float) * frameperiod
                new_index[:len(new_times)] = new_times
                #
                if repeat_n == framediff:
                    pad_values = padding[:framediff]
                else:
                    src_idxs = list(islice(cycle(list(range(repeat_n))), framediff))
                    pad_values = padding[src_idxs]
                new_values = np.concatenate((pad_values, values))
            else:
                raise NotImplementedError(f"location={location}")
            return cls(new_values, index=new_index)


    def slice_ranges(self, ranges: Iterable[Tuple[float, float]]) -> "Track":
        """Return new Track from multiple time ranges, endpoints are inclusive"""
        new_track = None
        for starttime, endtime in ranges:
            if new_track is None:
                new_track = self.loc[starttime:endtime]
            else:
                new_track = pd.concat((new_track, self.loc[starttime:endtime]))
        return new_track


ValueColumnsIndex = namedtuple("ValueColumnsIndex", ["values", "columns", "index"])

class Tracks(object):
    """Known limitation: While a Track index just needs to be
    monotonically increasing, duplicate time indices are not supported
    in Tracks (imposed by the use of Pandas multi-index)

    """
    IDX_NAMES = ("trkidx", Track.IDX_NAME)

    def __init__(self,
                 df: pd.DataFrame=None,
                 vci: ValueColumnsIndex=None,
                 xar: xr.Dataset=None,
                 h5f: h5.File=None,
                 it: Iterable[Track]=None):
        """A Tracks instance can be backed by:
        1. An in-memory pd.DataFrame,
        2. An in-memory set of objects,
        3. An on-disk xr.Dataset (in NetCDF format, could be either a single file or dir)
        4. An on-disk h5.File (with datasets describing homogeneous Tracks in HDF5 format)
        5. An iterator yielding Track instances
        """
        non_null_args = sum([int(arg is not None) for arg in [df, xar, it, h5f, vci]])
        if non_null_args != 1:
            raise Exception("Invalid input to Tracks constructor...")
        if h5f is not None:
            raise NotImplementedError
        if df is not None:
            assert df.index.names == self.IDX_NAMES
            df = df.reindex(sorted(df.index))
        if vci is not None:
            assert len(vci.values.shape) == 3
        self.vci = vci
        self.df = df
        self._xar = xar
        self._it = it

    def __iter__(self) -> Iterable[Track]:
        if self.df is not None:
            return self._df_iter(self.df)
        if self.vci is not None:
            return self._vci_iter()
        elif self._xar is not None:
            return self._xr_iter(self._xar)
        else:
            return self._it

    def __len__(self) -> Optional[int]:
        if self.df is not None:
            return len(set(self.df.index.get_level_values(self.IDX_NAMES[0])))
        elif self.vci is not None:
            return len(self.vci.values)
        elif self._xar is not None:
            return self._xar.dims[self.IDX_NAMES[0]]
        else:
            raise Exception("This instance of Tracks does not support len()...")

    def __getitem__(self, i):
        if not type(i) is int:
            raise TypeError("Only supports integer indices...")
        i = (len(self) + i) if i < 0 else i
        if self.df is not None:
            return Track(self.df.loc[i])
        if self.vci is not None:
            return Track(self.vci.values[i],
                         index=self.vci.index,
                         columns=self.vci.columns)
        elif self._xar is not None:
            df = self._xar.sel({self.IDX_NAMES[0]: i}).to_dataframe()
            # return Track(Tracks._unpack_multiindex(df))
            return Track(df)
        else:
            raise Exception("This instance of Tracks does not support random access...")

    @classmethod
    def from_iter(cls,
                  trks: Iterable[Track],
                  slurp: bool=False) -> "Tracks":
        if slurp:
            df = xr.concat((s.to_xarray() for s in trks),
                           dim=cls.IDX_NAMES[0]).to_dataframe()
            return cls(df=cls._unpack_multiindex(df))
        else:
            return cls(it=trks)

    @classmethod
    def from_xarray(cls,
                    xar: xr.Dataset,
                    slurp: bool=False) -> "Tracks":
        if slurp:
            xar.load()
            df = xar.to_dataframe()
            return cls(df=cls._unpack_multiindex(df))
        else:
            return cls(xar=xar)

    @classmethod
    def from_netcdf(cls, path: str, slurp: bool=False) -> "Tracks":
        if os.path.isdir(path):
            glb = sorted(glob(os.path.join(path, "*")),
                         key=lambda x:int(os.path.basename(x)))
            xar = xr.open_mfdataset(glb,
                                    combine="nested",
                                    concat_dim=cls.IDX_NAMES[0])
            return cls.from_xarray(xar, slurp)
        else:
            return cls.from_xarray(xr.open_dataset(path), slurp)

    @classmethod
    def from_hdf5(cls, path: str, slurp: bool=False) -> "Tracks":
        if slurp:
            with h5.File(path, "r") as h5f:
                columns = h5f["columns"][:]
                shared_index = h5f["index"][:]
                dset = h5f["values"]
                values = np.zeros_like(dset)
                dset.read_direct(values)
            return cls(vci=ValueColumnsIndex(values,
                                             [col.decode("ascii") for col in columns],
                                             shared_index))
        else:
            raise NotImplementedError

    @classmethod
    def from_disk(cls, path: str, slurp: bool=False) -> "Tracks":
        if path.endswith(".nc"):
            return cls.from_netcdf(path, slurp)
        elif path.endswith(".h5"):
            return cls.from_hdf5(path, slurp)
        else:
            raise NotImplementedError

    @classmethod
    def df_to_xarray(cls, df) -> xr.Dataset:
        df = df.reindex(sorted(df.index))
        df.index = [i[1] for i in df.index]
        datasets = {}
        idxset = None
        for var in df.columns:
            ser = df[var]
            if idxset is None:
                idxset = sorted(set(ser.index))
            arr = ser.to_numpy().reshape((-1, len(idxset)))
            datasets[var] = xr.DataArray(arr,
                                         dims=[cls.IDX_NAMES[0], "index"],
                                         coords={"index": idxset})
        xar = xr.Dataset(datasets)
        return xar

    def to_netcdf(self, path: str) -> "Tracks":
        if self.df is not None:
            self.df_to_xarray(self.df).to_netcdf(path)
        else:
            abspath = os.path.abspath(path)
            os.makedirs(abspath)
            for i, trk in enumerate(self):
                filepath = os.path.join(abspath, str(i))
                trk.to_xarray().to_netcdf(filepath)
        return self

    @staticmethod
    def _create_hdf5_datasets(h5f: h5.File,
                              proto_trk: Track,
                              fillvalue: float,
                              resize_length: int,
                              create_dataset_kwargs: dict):
        idxs = np.array(proto_trk.index)
        cols = np.array(proto_trk.columns, dtype=bytes)
        index = h5f.create_dataset("index",
                                   (proto_trk.shape[0],),
                                   dtype=idxs.dtype)
        index[:] = idxs
        columns = h5f.create_dataset("columns",
                                     (proto_trk.shape[1],),
                                     dtype=cols.dtype)
        columns[:] = cols
        ###
        if "dtype" in create_dataset_kwargs:
            dtype = create_dataset_kwargs.pop("dtype")
        else:
            dtype = proto_trk.to_numpy().dtype
        maxshape = (None, *proto_trk.shape)
        if "chunks" in create_dataset_kwargs:
            chunks = create_dataset_kwargs.pop("chunks")
        else:
            num_tracks_in_chunk = int((1024 * 1024 * 16) #16MB
                                      / dtype.itemsize
                                      / (proto_trk.shape[0] * proto_trk.shape[1]))
            chunks = (num_tracks_in_chunk, *proto_trk.shape)
        values = h5f.create_dataset("values",
                                    (resize_length, *proto_trk.shape),
                                    maxshape=maxshape,
                                    fillvalue=fillvalue,
                                    dtype=dtype,
                                    chunks=chunks,
                                    **create_dataset_kwargs)
        return values

    def to_hdf5(self,
                path: str,
                resize_length: Optional[int]=None,
                **create_dataset_kwargs) -> "Tracks":
        fillvalue = np.nan
        try:
            resize_length = resize_length or len(self)
        except:
            resize_length = 1

        if self.df is not None:
            LOGGER.debug("Tracks.to_hdf5() from df...")
            trk = self[0]
            with h5.File(path, "w") as h5f:
                values = Tracks._create_hdf5_datasets(h5f, trk, fillvalue, len(self), create_dataset_kwargs)
                data = np.array(self.df.to_numpy().reshape(values.shape), order="C")
                values.write_direct(data)
        else:
            LOGGER.debug("Tracks.to_hdf5() from iterable (resize_length=%s)...", resize_length)
            with h5.File(path, "w") as h5f:
                for i, trk in enumerate(self):
                    if (i + 1) % 1000 == 0:
                        LOGGER.debug("Tracks.to_hdf5() written %s tracks, chunks=%s...", i + 1, values.chunks)
                    if i == 0:
                        values = Tracks._create_hdf5_datasets(h5f, trk, fillvalue, resize_length, create_dataset_kwargs)
                    if i > (values.shape[0] - 1):
                        LOGGER.debug("Tracks.to_hdf5() resizing...")
                        values.resize(values.shape[0] + resize_length, 0)
                    values[i] = trk.to_numpy()
                values.resize(i + 1, 0)
        return self

    def to_disk(self, path: str, **kwargs):
        if path.endswith(".nc"):
            self.to_netcdf(path)
        elif path.endswith(".h5"):
            self.to_hdf5(path, **kwargs)
        else:
            raise NotImplementedError

    def to_jsonlines(self) -> Iterable[str]:
        for trk in self:
            yield trk.to_json() + "\n"

    @classmethod
    def _df_iter(cls, df: pd.DataFrame) -> Iterable[Track]:
        # Ensure seqidx is level 0:
        df.index.swaplevel(0, cls.IDX_NAMES[0])
        for i in sorted(set(df.index.get_level_values(0))):
            yield Track(df.loc[i])

    def _vci_iter(self) -> Iterable[Track]:
        for i in range(len(self)):
            yield self[i]

    @classmethod
    def _xr_iter(cls, xar: xr.Dataset) -> Iterable[Track]:
        for i in range(xar.dims[cls.IDX_NAMES[0]]):
            df = xar.sel({cls.IDX_NAMES[0]: i}).to_dataframe()
            yield Track(df)

    @classmethod
    def _unpack_multiindex(cls, df: pd.DataFrame) -> pd.DataFrame:
        if set(df.index.names) == set(cls.IDX_NAMES):
            df.index = df.reorder_levels(cls.IDX_NAMES).index
            return df
        elif set(df.index.names) == set([cls.IDX_NAMES[0], "index"]):
            df.index = df.reorder_levels([cls.IDX_NAMES[0], "index"]).index
            df.index = pd.MultiIndex.from_tuples(df.index, names=cls.IDX_NAMES)
            return df
        else:
            raise Exception("Wrong index names: {}".format(df.index.names))


    def mean_sq_euc_dist(self, t: Track):
        if self.df is None:
            from . import mappings
            objf = partial(mappings.objective,
                           reference=t,
                           aggf=lambda x: np.mean(np.square(x)),
                           max_frames_diff=0)
            def iter_func():
                for tt in self:
                    yield objf(tt)
            return iter_func()
        else:
            a = self.df.to_numpy().reshape((-1, *self[0].shape))
            b = np.zeros_like(a)
            b[:] = t.to_numpy()
            d = ((a - b) ** 2).sum(2).mean(1)
        return d
