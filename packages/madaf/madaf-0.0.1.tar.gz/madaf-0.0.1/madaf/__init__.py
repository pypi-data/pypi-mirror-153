from os import PathLike
from typing import Any
import lmdb
import msgpack


class Madaf:
    def __init__(self, path: PathLike):
        self.db = lmdb.open(path)

    def __setitem__(self, key: str, value: Any):
        with self.db.begin(write=True) as txn:
            txn.put(key.encode("utf-8"), msgpack.packb(value))

    def __getitem__(self, key: str):
        with self.db.begin() as txn:
            value = txn.get(key.encode("utf-8"))
        if value is None:
            raise KeyError(key)
        return msgpack.unpackb(value)
