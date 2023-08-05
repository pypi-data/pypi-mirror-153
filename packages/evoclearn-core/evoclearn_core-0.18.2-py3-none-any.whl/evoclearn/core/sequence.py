# -*- coding: utf-8 -*-

import os
import io
import bz2
from glob import glob
from typing import Iterable, Optional

import numpy as np
import pandas as pd
import xarray as xr

from . utils import standard_param_order


class Sequence(pd.DataFrame):
    """A Dataframe which has a well-defined multi-index and ordered
    columns representing VTL and qTA parameters"""
    IDX_NAMES = ("idx", "lab")

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        assert self.index.names == self.IDX_NAMES
        #assert all(((e, f) for e, f in zip(self.columns, standard_param_order(self.columns))))

    @property
    def _constructor(self):
        return self.__class__

    @classmethod
    def from_json(cls, s: str, dtype=None) -> "Sequence":
        df = pd.read_json(s, orient="table")
        if dtype is not None:
            df = df.astype(dtype, copy=False)
        return cls(df)

    @classmethod
    def from_file(cls, f, dtype=None) -> "Sequence":
        if type(f) is str:
            io_lib = bz2 if f.endswith(".bz2") else io
            with io_lib.open(f, "rt") as infh:
                return cls.from_json(infh.read(), dtype=dtype)
        else:
            return cls.from_json(f.read(), dtype=dtype)

    @classmethod
    def from_xarray(cls, xar: xr.Dataset) -> "Sequence":
        df = xar.to_dataframe()
        mi = map(lambda x: (int(x[0]), x[1]), (l.split("*") for l in df.index))
        df.index = pd.MultiIndex.from_tuples(mi, names=cls.IDX_NAMES)
        return cls(df)

    @classmethod
    def from_spec(cls, params, labels=None, fill_value=np.nan) -> "Sequence":
        assert len(params) == len(set(params))
        labels = labels if labels is not None else ["_"]
        df = pd.DataFrame(fill_value,
                          index=pd.MultiIndex.from_tuples(enumerate(labels), names=cls.IDX_NAMES),
                          columns=standard_param_order(params))
        return cls(df)

    def to_json(self) -> str:
        """No newlines in JSON string"""
        return super(self.__class__, self).to_json(orient="table")

    def to_file(self, f) -> "Sequence":
        if type(f) is str:
            io_lib = bz2 if f.endswith(".bz2") else io
            with io_lib.open(f, "wt") as outfh:
                outfh.write(self.to_json())
        else:
            f.write(self.to_json())
        return self

    def to_xarray(self) -> xr.Dataset:
        df = pd.DataFrame(self).copy()
        df.index = ["*".join(map(str, i)) for i in df.index]
        return df.to_xarray()


class Sequences(object):
    IDX_NAMES = ("seqidx",) + Sequence.IDX_NAMES

    def __init__(self,
                 df: pd.DataFrame=None,
                 xar: xr.Dataset=None,
                 it: Iterable[Sequence]=None):
        """A Sequences instance can be backed by:
        1. An in-memory pd.DataFrame,
        2. An on-disk xr.Dataset (in NetCDF format, could be either a single file or dir)
        3. An iterator yielding Sequence instances

        For the first two cases random access via __getitem__ is implemented
        """
        non_null_args = sum([int(arg is not None) for arg in [df, xar, it]])
        if non_null_args != 1:
            raise Exception("Invalid input to Sequences constructor...")
        if df is not None:
            assert df.index.names == self.IDX_NAMES
            df = df.reindex(sorted(df.index, key=lambda x:x[:2]))
        self.df = df
        self._xar = xar
        self._it = it

    def __iter__(self) -> Iterable[Sequence]:
        if self.df is not None:
            return self._df_iter(self.df)
        elif self._xar is not None:
            return self._xr_iter(self._xar)
        else:
            return self._it

    def __len__(self) -> Optional[int]:
        if self.df is not None:
            return len(set(self.df.index.get_level_values(self.IDX_NAMES[0])))
        elif self._xar is not None:
            return self._xar.dims[self.IDX_NAMES[0]]
        else:
            raise Exception("This instance of Sequences does not support len()...")

    def __getitem__(self, i):
        if not type(i) is int:
            raise TypeError("Only supports integer indices...")
        i = (len(self) + i) if i < 0 else i
        if self.df is not None:
            return Sequence(self.df.loc[i])
        elif self._xar is not None:
            df = self._xar.sel({self.IDX_NAMES[0]: i}).to_dataframe()
            return Sequence(Sequences._unpack_multiindex(df))
        else:
            raise Exception("This instance of Sequences does not support random access...")

    @classmethod
    def from_iter(cls,
                  seqs: Iterable[Sequence],
                  slurp: bool=False) -> "Sequences":
        if slurp:
            df = xr.concat((s.to_xarray() for s in seqs),
                           dim=cls.IDX_NAMES[0]).to_dataframe()
            return cls(df=cls._unpack_multiindex(df))
        else:
            return cls(it=seqs)

    @classmethod
    def from_xarray(cls,
                    xar: xr.Dataset,
                    slurp: bool=False) -> "Sequences":
        if slurp:
            xar.load()
            df = xar.to_dataframe()
            return cls(df=cls._unpack_multiindex(df))
        else:
            return cls(xar=xar)

    @classmethod
    def from_netcdf(cls, path: str, slurp: bool=False) -> "Sequences":
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
    def from_disk(cls, path: str, slurp: bool=False) -> "Tracks":
        if path.endswith(".nc"):
            return cls.from_netcdf(path, slurp)
        elif path.endswith(".h5"):
            return cls.from_hdf5(path, slurp)
        else:
            raise NotImplementedError

    @staticmethod
    def df_to_xarray(df) -> xr.Dataset:
        df = df.reindex(sorted(df.index, key=lambda x:x[:2]))
        df.index = ["*".join(map(str, i[1:])) for i in df.index]
        datasets = {}
        segset = None
        for var in df.columns:
            ser = df[var]
            if segset is None:
                segset = sorted(set(ser.index), key=lambda x:int(x.split("*")[0]))
            arr = ser.to_numpy().reshape((-1, len(segset)))
            datasets[var] = xr.DataArray(arr,
                                         dims=[Sequences.IDX_NAMES[0], "index"],
                                         coords={"index": segset})
        xar = xr.Dataset(datasets)
        return xar

    def to_netcdf(self, path: str) -> "Sequences":
        if self.df is not None:
            xar = self.df_to_xarray(self.df).to_netcdf(path)
        else:
            abspath = os.path.abspath(path)
            os.makedirs(abspath)
            for i, seq in enumerate(self):
                filepath = os.path.join(abspath, str(i))
                seq.to_xarray().to_netcdf(filepath)
        return self

    def to_disk(self, path: str, **kwargs):
        if path.endswith(".nc"):
            self.to_netcdf(path)
        elif path.endswith(".h5"):
            raise NotImplementedError
        else:
            raise NotImplementedError

    def to_jsonlines(self) -> Iterable[str]:
        for seq in self:
            yield seq.to_json() + "\n"

    @classmethod
    def _df_iter(cls, df: pd.DataFrame) -> Iterable[Sequence]:
        # Ensure seqidx is level 0:
        df.index.swaplevel(0, cls.IDX_NAMES[0])
        for i in sorted(set(df.index.get_level_values(0))):
            yield Sequence(df.loc[i])

    @classmethod
    def _xr_iter(cls, xar: xr.Dataset) -> Iterable[Sequence]:
        for i in range(xar.dims[cls.IDX_NAMES[0]]):
            df = xar.sel({cls.IDX_NAMES[0]: i}).to_dataframe()
            yield Sequence(Sequences._unpack_multiindex(df))

    @classmethod
    def _unpack_multiindex(cls, df: pd.DataFrame) -> pd.DataFrame:
        if len(df.index.names) == 2:
            df.index = df.reorder_levels([cls.IDX_NAMES[0], "index"]).index
            mi = [(seqidx, int(ilab.split("*")[0]), ilab.split("*")[1])
                  for seqidx, ilab
                  in df.index]
            df.index = pd.MultiIndex.from_tuples(mi, names=cls.IDX_NAMES)
            return df
        elif len(df.index.names) == 1:
            mi = [(int(ilab.split("*")[0]), ilab.split("*")[1])
                  for ilab
                  in df.index]
            df.index = pd.MultiIndex.from_tuples(mi, names=cls.IDX_NAMES[1:])
            return df
        else:
            raise Exception("Wrong index names: {}".format(df.index.names))
